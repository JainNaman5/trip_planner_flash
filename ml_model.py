"""
ml_model.py - Machine Learning recommendation engine for Trip Planner India.
Uses KNN for nearest-city lookup and K-Means for regional clustering.
"""
import sqlite3, math, os
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trip_planner.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance in km between two lat/lng points."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return R * 2 * math.asin(math.sqrt(a))


class TripRecommender:
    """ML-powered trip recommendation engine."""

    CLUSTER_THEMES = {
        0: "Heritage & Culture",
        1: "Beaches & Coastal",
        2: "Mountains & Adventure",
        3: "Spiritual & Pilgrimage",
        4: "Nature & Wildlife",
    }

    def __init__(self):
        self.knn_model = None
        self.kmeans_model = None
        self.scaler = StandardScaler()
        self.cities = []
        self.city_coords = None

    def fit(self):
        """Train ML models on city data from the database using Haversine spherical distance."""
        conn = get_db()
        rows = conn.execute("SELECT id, name, state, lat, lng FROM cities").fetchall()
        conn.close()

        self.cities = [dict(r) for r in rows]
        coords = np.array([[c["lat"], c["lng"]] for c in self.cities])
        self.city_coords = coords

        # Standardise coordinates for KMeans clustering
        scaled = self.scaler.fit_transform(coords)

        # KNN model on true spherical Haversine metric in radians
        rad_coords = np.radians(coords)
        k = min(len(self.cities), len(self.cities))
        self.knn_model = NearestNeighbors(n_neighbors=k, metric="haversine")
        self.knn_model.fit(rad_coords)

        # K-Means clustering — group cities into regional clusters
        n_clusters = min(5, len(self.cities))
        self.kmeans_model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.kmeans_model.fit(scaled)

        # Assign cluster labels
        labels = self.kmeans_model.labels_
        for i, city in enumerate(self.cities):
            city["cluster"] = int(labels[i])

        print(f"[ML] Trained KNN (Haversine) and KMeans ({n_clusters} clusters) on {len(self.cities)} cities")

    def _find_city(self, name):
        """Lookup city by name (case-insensitive)."""
        name_lower = name.lower().strip()
        for c in self.cities:
            if c["name"].lower() == name_lower:
                return c
        # Partial match fallback
        for c in self.cities:
            if name_lower in c["name"].lower() or c["name"].lower() in name_lower:
                return c
        return None

    def get_nearby_cities(self, lat, lng, k=10):
        """Use KNN Haversine metric to find the closest cities to a coordinate in exact distance order."""
        point_rad = np.radians([[lat, lng]])
        distances, indices = self.knn_model.kneighbors(point_rad, n_neighbors=len(self.cities))
        results = []
        for dist_rad, idx in zip(distances[0], indices[0]):
            city = self.cities[idx]
            dist_km = round(dist_rad * 6371.0)
            if 15 <= dist_km <= 500:  # Exclude self/origin, include within 500km travel corridor
                results.append({**city, "distance_km": dist_km})
        results.sort(key=lambda x: x["distance_km"])
        return results[:k]

    def get_recommendations(self, city_name, budget="medium", trip_type="balanced"):
        """Full recommendation pipeline prioritizing true geographic proximity and local relevance."""
        origin = self._find_city(city_name)
        if not origin:
            return None

        # 1. KNN Haversine — find the true closest cities in increasing distance order
        nearby = self.get_nearby_cities(origin["lat"], origin["lng"], k=10)

        # 2. Get attractions for nearby cities
        conn = get_db()
        nearby_ids = [c["id"] for c in nearby]
        if not nearby_ids:
            conn.close()
            return {"origin": origin, "nearby": [], "cluster_id": 0, "cluster_theme": "General"}

        placeholders = ",".join("?" * len(nearby_ids))
        attractions = conn.execute(
            f"SELECT * FROM attractions WHERE city_id IN ({placeholders}) ORDER BY popularity DESC",
            nearby_ids
        ).fetchall()
        attractions = [dict(a) for a in attractions]

        # 3. Build scored nearby list with proximity as the dominant driver
        scored = []
        for city in nearby:
            city_attractions = [a for a in attractions if a["city_id"] == city["id"]]
            avg_pop = (sum(a["popularity"] for a in city_attractions) / len(city_attractions)) if city_attractions else 5.0
            avg_rating = (sum(a.get("google_rating", 4.0) for a in city_attractions) / len(city_attractions)) if city_attractions else 4.0
            num_attractions = len(city_attractions)

            # Proximity is the primary ranking factor:
            # 50 km -> ~92%, 100 km -> ~84%, 150 km -> ~77%, 200 km -> ~70%, 300 km -> ~55%
            dist_score = max(25.0, 100.0 - (city["distance_km"] * 0.15))

            # Quality and theme fine-tuning (+/- 2 to 8%)
            pop_boost = min(avg_pop * 0.5, 4.0)
            rating_boost = max(0.0, (avg_rating - 3.5) * 4.0)

            sig_types = [a.get("significance", "") for a in city_attractions]
            theme_boost = 0.0
            if trip_type == "nearby":
                theme_boost = sum(1.5 for s in sig_types if s in ("Adventure", "Nature", "Wildlife", "Scenic"))
            elif trip_type == "popular":
                theme_boost = sum(1.5 for s in sig_types if s in ("Historical", "Architectural", "Cultural"))
            else:
                theme_boost = sum(1.5 for s in sig_types if s in ("Religious", "Spiritual"))
            theme_boost = min(theme_boost, 6.0)

            # Budget fine-tuning
            budget_adj = 0.0
            if budget == "low":
                avg_fee = sum(a.get("entrance_fee", 0) for a in city_attractions) / max(len(city_attractions), 1)
                if avg_fee > 200:
                    budget_adj = -3.0
            elif budget == "high":
                budget_adj = 2.0

            match_score = int(round(dist_score + pop_boost + rating_boost + theme_boost + budget_adj))
            match_score = max(30, min(match_score, 98))

            # Transport options
            transport = conn.execute(
                "SELECT mode, price_inr, duration_hrs FROM transport WHERE from_city_id=? AND to_city_id=?",
                (origin["id"], city["id"])
            ).fetchall()

            # Get stay options
            stays = conn.execute(
                "SELECT name, type, price_per_night, rating FROM stays WHERE city_id=? ORDER BY price_per_night",
                (city["id"],)
            ).fetchall()

            scored.append({
                "city": city["name"],
                "state": city["state"],
                "lat": city["lat"],
                "lng": city["lng"],
                "distance_km": city["distance_km"],
                "match_score": match_score,
                "attractions": [{"name": a["name"], "category": a.get("type", ""),
                                 "popularity": a["popularity"], "description": a.get("description", "")}
                                for a in city_attractions[:5]],
                "transport": [{"mode": dict(t)["mode"],
                               "price_inr": dict(t)["price_inr"],
                               "duration_hrs": dict(t)["duration_hrs"]}
                              for t in transport],
                "stays": [{"name": dict(s)["name"], "type": dict(s)["type"],
                           "price_per_night": dict(s)["price_per_night"],
                           "rating": dict(s)["rating"]}
                          for s in stays],
            })

        # 4. Fetch origin city attractions and stays
        origin_attractions = conn.execute(
            "SELECT * FROM attractions WHERE city_id=? ORDER BY popularity DESC",
            (origin["id"],)
        ).fetchall()
        origin_stays = conn.execute(
            "SELECT name, type, price_per_night, rating FROM stays WHERE city_id=? ORDER BY price_per_night",
            (origin["id"],)
        ).fetchall()

        conn.close()

        # Sort primarily by proximity (distance_km ascending) with secondary match_score ranking
        # This guarantees closest destinations like Indore (51km), Mandu (101km), Omkareshwar (110km) are shown first!
        scored.sort(key=lambda x: (x["distance_km"], -x["match_score"]))

        cluster_id = origin.get("cluster", 0)
        return {
            "origin": origin,
            "origin_attractions": [dict(a) for a in origin_attractions],
            "origin_stays": [dict(s) for s in origin_stays],
            "nearby": scored,
            "cluster_id": cluster_id,
            "cluster_theme": self.CLUSTER_THEMES.get(cluster_id, "General"),
        }

    def generate_itinerary(self, origin_name, dest_name="", budget="medium", trip_type="balanced", days=3):
        """Generate a complete multi-day travel plan starting with origin city's places, then nearby destinations."""
        rec = self.get_recommendations(origin_name, budget, trip_type)
        if not rec:
            return None

        origin = rec["origin"]
        origin_attrs = rec["origin_attractions"]
        origin_stays = rec["origin_stays"]
        nearby = rec["nearby"]

        num_days = max(1, min(int(days), 7))
        itinerary = []
        total_dist = 0

        # Day 1: Exploring Origin City (e.g. Ujjain)
        top_origin_names = [a["name"] for a in origin_attrs[:2]]
        day1_highlight = " & ".join(top_origin_names) if top_origin_names else f"Explore {origin['name']}"
        day1_hotel = f"Stay: {origin_stays[0]['name']} (₹{origin_stays[0]['price_per_night']}/night)" if origin_stays else "Starting Hub"

        itinerary.append({
            "day": 1,
            "city": origin["name"],
            "state": origin["state"],
            "is_origin": True,
            "highlight": day1_highlight,
            "tagline": f"Local Sightseeing in {origin['name']}",
            "places_to_visit": origin_attrs[:4],
            "transit": "Starting Point • Local City Exploration",
            "distance_from_prev": 0,
            "hotel": day1_hotel,
            "stay_options": origin_stays,
            "coordinates": [origin["lat"], origin["lng"]],
        })

        if num_days > 1:
            # Build ordered list of destinations: selected dest first, then closest high-match
            ordered_dests = []
            if dest_name:
                matched_dest = next((c for c in nearby if c["city"].lower() == dest_name.lower()), None)
                if not matched_dest:
                    # Look up from entire db if not in top 10
                    dest_obj = self._find_city(dest_name)
                    if dest_obj and dest_obj["name"].lower() != origin["name"].lower():
                        conn = get_db()
                        d_attrs = conn.execute("SELECT * FROM attractions WHERE city_id=?", (dest_obj["id"],)).fetchall()
                        d_stays = conn.execute("SELECT * FROM stays WHERE city_id=?", (dest_obj["id"],)).fetchall()
                        conn.close()
                        dist = round(haversine(origin["lat"], origin["lng"], dest_obj["lat"], dest_obj["lng"]))
                        matched_dest = {
                            "city": dest_obj["name"], "state": dest_obj["state"],
                            "lat": dest_obj["lat"], "lng": dest_obj["lng"],
                            "distance_km": dist, "match_score": 90,
                            "attractions": [dict(a) for a in d_attrs],
                            "stays": [dict(s) for s in d_stays],
                            "transport": [{"mode": "Car", "price_inr": max(500, dist * 8), "duration_hrs": max(1, round(dist / 50, 1))}]
                        }
                if matched_dest:
                    ordered_dests.append(matched_dest)

            for c in nearby:
                if c["city"].lower() != origin["name"].lower() and (not dest_name or c["city"].lower() != dest_name.lower()):
                    ordered_dests.append(c)

            # Assign subsequent days
            prev_lat, prev_lng = origin["lat"], origin["lng"]
            prev_city = origin["name"]

            for day_idx in range(2, num_days + 1):
                dest_idx = day_idx - 2
                if dest_idx < len(ordered_dests):
                    target = ordered_dests[dest_idx]
                else:
                    # Wrap or stop if no more cities
                    break

                leg_dist = round(haversine(prev_lat, prev_lng, target["lat"], target["lng"]))
                total_dist += leg_dist
                dur_hrs = max(1.0, round(leg_dist / 50.0, 1))

                city_attrs = target.get("attractions", [])
                top_names = [a["name"] for a in city_attrs[:2]]
                hl = " & ".join(top_names) if top_names else f"Explore {target['city']}"

                # Match stay by budget
                target_stays = target.get("stays", [])
                hotel_str = ""
                if target_stays:
                    stay_pick = target_stays[0]
                    if budget == "high" and len(target_stays) >= 3:
                        stay_pick = target_stays[2]
                    elif budget == "medium" and len(target_stays) >= 2:
                        stay_pick = target_stays[1]
                    hotel_str = f"Stay: {stay_pick['name']} (₹{stay_pick['price_per_night']}/night)"

                itinerary.append({
                    "day": day_idx,
                    "city": target["city"],
                    "state": target["state"],
                    "is_origin": False,
                    "highlight": hl,
                    "tagline": f"Journey to {target['city']}",
                    "places_to_visit": city_attrs[:4],
                    "transit": f"From {prev_city} • {leg_dist} km ({dur_hrs} hrs)",
                    "distance_from_prev": leg_dist,
                    "duration_hrs": dur_hrs,
                    "hotel": hotel_str,
                    "stay_options": target_stays,
                    "coordinates": [target["lat"], target["lng"]],
                })

                prev_lat, prev_lng = target["lat"], target["lng"]
                prev_city = target["city"]

        center_lat = sum(i["coordinates"][0] for i in itinerary) / len(itinerary)
        center_lng = sum(i["coordinates"][1] for i in itinerary) / len(itinerary)

        return {
            "origin": origin,
            "origin_attractions": origin_attrs,
            "dest_name": dest_name,
            "days": num_days,
            "budget": budget,
            "trip_type": trip_type,
            "cluster_theme": rec["cluster_theme"],
            "itinerary": itinerary,
            "total_distance_km": total_dist,
            "center_lat": center_lat,
            "center_lng": center_lng,
        }

    def get_all_city_names(self):
        """Return list of all city names for autocomplete."""
        conn = get_db()
        cities = conn.execute("SELECT name, state FROM cities ORDER BY name").fetchall()
        states = conn.execute("SELECT DISTINCT state FROM cities ORDER BY state").fetchall()
        conn.close()
        options = []
        for c in cities:
            options.append({"value": c["name"], "label": f"{c['name']}, {c['state']}", "type": "city"})
        for s in states:
            options.append({"value": s["state"], "label": s["state"], "type": "state"})
        return options

