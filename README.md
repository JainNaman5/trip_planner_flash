# Trip Planner India — Smart Travel & Multi-Day Itinerary Planner

An AI & Machine Learning powered travel planning platform built with **Flask**, **Scikit-Learn**, and **Leaflet.js**. Plan personalized multi-day circuits across **100+ Indian cities**, explore local must-visit attractions, calculate estimated travel duration and costs, compare curated stays, and visualize routes on interactive maps.

---

## ✨ Features

- 🧠 **ML-Driven Recommendations**: Uses **K-Nearest Neighbors (KNN)** and **K-Means Regional Clustering** to suggest optimal nearby destinations based on geographical proximity, popularity, travel style, and budget.
- 📍 **Local City Exploration (Day 1)**: Highlights must-visit sights, spiritual landmarks, and heritage attractions within the starting city (e.g., Ujjain, Jaipur, Delhi) before routing onwards.
- 🗓️ **Customizable Multi-Day Itineraries**: Plan flexible **1, 2, 3, 4, 5, or 7-day** routes that adapt day-by-day stops, inter-city distances, and travel times.
- 🗺️ **Interactive Route Mapping**: Dynamic **Leaflet.js** map rendering custom day markers, route polylines, and popups for each destination.
- 🚗 **Transport & Stay Estimates**: Compare modes of transport (Car, Bus, Train, Flight) with cost and duration estimates, alongside curated budget, mid-range, and luxury stays.
- 🎨 **Modern Aesthetics & Dark Mode**: Sleek glassmorphic UI design with light/dark theme toggle, micro-animations, and responsive layout.

---

## 🛠️ Tech Stack

- **Backend**: Python 3, Flask (RESTful routing & Jinja2 server-side rendering)
- **Machine Learning**: Scikit-Learn (`NearestNeighbors`, `KMeans`, `StandardScaler`), NumPy, Pandas
- **Database**: SQLite3 (`trip_planner.db` with 100 cities, 420+ attractions, 19,000+ transport routes, and stays)
- **Frontend**: HTML5, Vanilla CSS3 (Custom design system), JavaScript (ES6+), Leaflet.js OpenStreetMap
- **Typography & Icons**: Google Fonts (*Plus Jakarta Sans*), Google Material Symbols

---

## 📁 Project Structure

```text
trip-planner-india/
├── app.py                  # Flask application entry point & route controllers
├── ml_model.py             # Machine learning recommendation & itinerary engine
├── seed_from_data_txt.py   # Database seeder script (generates trip_planner.db)
├── trip_planner.db         # SQLite database
├── data___.txt             # Source dataset reference
├── requirements.txt        # Python package dependencies
├── .gitignore              # Git ignore configuration
├── README.md               # Project documentation
├── static/
│   ├── css/
│   │   └── style.css       # Complete stylesheet (responsive, dark mode)
│   └── js/
│       └── main.js         # Theme toggle, search validation & UI helpers
└── templates/
    ├── base.html           # Base layout template (Navbar, Footer, Leaflet)
    ├── index.html          # Hero homepage with travel search form
    ├── explore.html        # Destination feed & "Must-Visit Places" section
    ├── planner.html        # Multi-day itinerary planner with interactive Leaflet map
    └── stays.html          # Transport comparison & hotel booking recommendations
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9 or higher
- Git

### 2. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/trip-planner-india.git
cd trip-planner-india
```

### 3. (Recommended) Create a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. (Optional) Initialize / Seed the Database
```bash
python seed_from_data_txt.py
```

### 6. Run the Application
```bash
python app.py
```

Open your browser and navigate to:
👉 **`http://localhost:5000`**

---

## 🤖 How the Recommendation Engine Works

1. **Geographic Proximity (KNN)**:
   - Coordinates (`lat`, `lng`) are normalized using `StandardScaler`.
   - `NearestNeighbors` calculates Haversine distances to discover proximate tourist hubs within a 500 km radius.
2. **Regional Clustering (K-Means)**:
   - Cities are categorized into regional clusters (e.g., *Heritage & Culture*, *Spiritual & Pilgrimage*, *Nature & Wildlife*).
3. **Multi-Factor Scoring**:
   - Computes a weighted match score based on distance, visitor popularity, ratings, entrance fees, and preferred travel style (*Spiritual*, *Heritage*, *Adventure*).
4. **Day-by-Day Circuit Synthesis**:
   - Day 1 prioritizes local sightseeing in the origin hub.
   - Subsequent days map the shortest connected path along top destinations with real-world road and train travel metrics.

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
