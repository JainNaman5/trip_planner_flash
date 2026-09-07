"""
app.py - Flask backend for Trip Planner India.
Serves Jinja2 templates and uses ML model for recommendations.
"""
from flask import Flask, render_template, request, jsonify
import os, json
from ml_model import TripRecommender

app = Flask(__name__)
recommender = TripRecommender()

# Verified Unsplash curated images for all Indian destinations
IMAGES = {
    "Agartala": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Agra": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80",
    "Ahmedabad": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80",
    "Aizawl": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Alappuzha": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
    "Amritsar": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Aurangabad": "https://images.unsplash.com/photo-1628155930542-3c7a64e2c833?auto=format&fit=crop&w=800&q=80",
    "Ayodhya": "/static/images/ram_mandir_ayodhya.jpg",
    "Bangalore": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=800&q=80",
    "Bengaluru": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=800&q=80",
    "Bhopal": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
    "Bhubaneswar": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Bilaspur": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
    "Chandigarh": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=800&q=80",
    "Chennai": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Cherrapunji": "https://images.unsplash.com/photo-1519999482648-25049ddd37b1?auto=format&fit=crop&w=800&q=80",
    "Coimbatore": "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=800&q=80",
    "Coorg": "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=800&q=80",
    "Darjeeling": "https://images.unsplash.com/photo-1519999482648-25049ddd37b1?auto=format&fit=crop&w=800&q=80",
    "Dehradun": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Delhi": "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=800&q=80",
    "Dhanbad": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
    "Dharamshala": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80",
    "Dimapur": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Faridabad": "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=800&q=80",
    "Gangtok": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Gaya": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Goa": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80",
    "Gurugram": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=800&q=80",
    "Guwahati": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=800&q=80",
    "Gwalior": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80",
    "Hampi": "https://images.unsplash.com/photo-1589182373726-e4f658ab50f0?auto=format&fit=crop&w=800&q=80",
    "Haridwar": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Hyderabad": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Imphal": "https://images.unsplash.com/photo-1519999482648-25049ddd37b1?auto=format&fit=crop&w=800&q=80",
    "Indore": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=800&q=80",
    "Itanagar": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Jabalpur": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Jagdalpur": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
    "Jaipur": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80",
    "Jaisalmer": "https://images.unsplash.com/photo-1598091383021-15ddea10925d?auto=format&fit=crop&w=800&q=80",
    "Jammu": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80",
    "Jamshedpur": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=800&q=80",
    "Jodhpur": "https://images.unsplash.com/photo-1598091383021-15ddea10925d?auto=format&fit=crop&w=800&q=80",
    "Jorhat": "https://images.unsplash.com/photo-1519999482648-25049ddd37b1?auto=format&fit=crop&w=800&q=80",
    "Kanyakumari": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Khajuraho": "https://images.unsplash.com/photo-1628155930542-3c7a64e2c833?auto=format&fit=crop&w=800&q=80",
    "Kochi": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
    "Kodaikanal": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Kohima": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Kolkata": "https://images.unsplash.com/photo-1558431382-27e303142255?auto=format&fit=crop&w=800&q=80",
    "Konark": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800&q=80",
    "Kurnool": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800&q=80",
    "Kurukshetra": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Leh": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80",
    "Lucknow": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800&q=80",
    "Ludhiana": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=800&q=80",
    "Madurai": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Maheshwar": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=800&q=80",
    "Manali": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Mandu": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800&q=80",
    "Mangi Tungi": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Mangaluru": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
    "Margao": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80",
    "Mathura": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Moodbidri": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Mount Abu": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Mumbai": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=800&q=80",
    "Munnar": "https://images.unsplash.com/photo-1519999482648-25049ddd37b1?auto=format&fit=crop&w=800&q=80",
    "Mysore": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Mysuru": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Nagpur": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=800&q=80",
    "Nainital": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Nalanda": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800&q=80",
    "Nashik": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "New Delhi": "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=800&q=80",
    "Omkareshwar": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=800&q=80",
    "Orchha": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80",
    "Ooty": "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=800&q=80",
    "Pachmarhi": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Palitana": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800&q=80",
    "Panaji": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80",
    "Panchkula": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Patiala": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80",
    "Patna": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=800&q=80",
    "Pawapuri": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=800&q=80",
    "Pelling": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80",
    "Port Blair": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
    "Prayagraj": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=800&q=80",
    "Puducherry": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80",
    "Pune": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=800&q=80",
    "Puri": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80",
    "Raipur": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
    "Rajkot": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80",
    "Rameswaram": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Ranakpur": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80",
    "Ranchi": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
    "Rishikesh": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Shankheshwar": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Shikharji": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Shillong": "https://images.unsplash.com/photo-1519999482648-25049ddd37b1?auto=format&fit=crop&w=800&q=80",
    "Shimla": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80",
    "Shravanabelagola": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Siliguri": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Sonagiri": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Kundalpur": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Hastinapur": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Srinagar": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80",
    "Surat": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80",
    "Tawang": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80",
    "Tezpur": "https://images.unsplash.com/photo-1519999482648-25049ddd37b1?auto=format&fit=crop&w=800&q=80",
    "Thiruvananthapuram": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
    "Tiruchirappalli": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Tirupati": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Udaipur": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=800&q=80",
    "Ujjain": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Vadodara": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80",
    "Varanasi": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=800&q=80",
    "Vijayawada": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Visakhapatnam": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
    "Warangal": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800&q=80",
    "Ziro": "https://images.unsplash.com/photo-1519999482648-25049ddd37b1?auto=format&fit=crop&w=800&q=80",
}

# Fallback images by significance/type
TYPE_IMAGES = {
    "Religious": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Historical": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800&q=80",
    "Nature": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Scenic": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80",
    "Wildlife": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Adventure": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Recreational": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80",
}

FALLBACK_IMAGES = [
    "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=800&q=80", # Taj Mahal / India
    "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80", # Fort
    "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=800&q=80", # Ghats
    "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=800&q=80", # Heritage India Gate
    "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80", # Temple Architecture
    "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80", # Hill Station
    "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80", # Coastal & Nature
    "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800&q=80", # Ancient Architecture
    "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=800&q=80", # Royal Palace
    "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=800&q=80", # Lake Palace
]
DEFAULT_IMG = FALLBACK_IMAGES[0]

ATTRACTION_ICONS = {
    "Religious": "temple_hindu",
    "Historical": "account_balance",
    "Nature": "park",
    "Scenic": "landscape",
    "Adventure": "hiking",
    "Wildlife": "pets",
    "Recreational": "attractions"
}

ATTRACTION_IMAGES = {
    "Mahakaleshwar Jyotirlinga": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Ram Mandir": "/static/images/ram_mandir_ayodhya.jpg",
    "Ram Mandir Ayodhya": "/static/images/ram_mandir_ayodhya.jpg",
    "Ram Ghat": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=800&q=80",
    "Kal Bhairav Temple": "https://images.unsplash.com/photo-1544717305-2782549b5136?auto=format&fit=crop&w=800&q=80",
    "Harsiddhi Temple": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Vedh Shala": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=800&q=80",
    "Mangalnath Temple": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Sandipani Ashram": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80",
    "Rajwada Palace": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=800&q=80",
    "Lal Bagh Palace": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80",
    "Sarafa Bazaar": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=80",
    "Omkareshwar Jyotirlinga": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=800&q=80",
    "Jahaz Mahal": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800&q=80",
    "Ahilya Fort": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80",
    "Taj Mahal": "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=800&q=80",
    "India Gate": "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=800&q=80",
    "Hawa Mahal": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80",
    "Gateway of India": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=800&q=80",
    "Golden Temple": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Howrah Bridge": "https://images.unsplash.com/photo-1558431382-27e303142255?auto=format&fit=crop&w=800&q=80",
    # Top Jain Mandirs & Tirths
    "Shatrunjaya": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800&q=80",
    "Adishwar": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800&q=80",
    "Sammed Shikharji": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Parasnath": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Gommateshwara": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Bahubali": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Dilwara": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Ranakpur": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80",
    "Sonagiri": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Kundalpur": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Bade Baba": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Jal Mandir": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=800&q=80",
    "Pavapuri": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=800&q=80",
    "Jambudweep": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Hastinapur": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Hutheesing": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80",
    "Kanch Mandir": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=800&q=80",
    "Gomatgiri": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Mahavir Tapobhumi": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Gopachal": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80",
    "Siddhachal": "https://images.unsplash.com/photo-1628155930542-3c7a64e2c833?auto=format&fit=crop&w=800&q=80",
    "Thousand Pillar": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Savira Kambada": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Mangi Tungi": "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?auto=format&fit=crop&w=800&q=80",
    "Lal Mandir": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Ahinsa Sthal": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Padampura": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Sanganer": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80",
    "Kesariyaji": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Girnar": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800&q=80",
    "Shankheshwar": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
}

def place_img(name, city, significance=None):
    if name:
        for k, v in ATTRACTION_IMAGES.items():
            if k.lower() in name.lower() or name.lower() in k.lower():
                return v
    return img(city, significance)

def img(city, significance=None):
    if city and city in IMAGES and IMAGES[city]:
        return IMAGES[city]
    if significance and significance in TYPE_IMAGES and TYPE_IMAGES[significance]:
        return TYPE_IMAGES[significance]
    # Deterministic dummy fallback so every destination has an attractive unique image
    idx = abs(hash(city or "India")) % len(FALLBACK_IMAGES)
    return FALLBACK_IMAGES[idx]

MODE_ICONS = {"Car":"directions_car","Bus":"directions_bus","Train":"train","Flight":"flight"}
BUDGET_LABELS = {"low":"Budget","medium":"Standard","high":"Luxury"}
TRIP_LABELS = {"popular":"Heritage","balanced":"Spiritual","nearby":"Adventure"}

def build_query(location, budget="medium", trip_type="balanced", days=3, dest=""):
    """Build query string to pass between pages."""
    q = f"location={location}&budget={budget}&trip_type={trip_type}&days={days}"
    if dest:
        q += f"&dest={dest}"
    return q

@app.route("/")
def index():
    locations = recommender.get_all_city_names()
    error = request.args.get("error", "")
    return render_template("index.html", active_page="home", locations=locations, error=error)

@app.route("/explore")
def explore():
    location = request.args.get("location", "Ujjain")
    budget = request.args.get("budget", "medium")
    trip_type = request.args.get("trip_type", "balanced")
    days = request.args.get("days", 3, type=int)
    query = build_query(location, budget, trip_type, days)

    result = recommender.get_recommendations(location, budget, trip_type)
    if result is None:
        locations = recommender.get_all_city_names()
        return render_template("index.html", active_page="home", locations=locations,
                               error=f"City '{location}' not found. Try Ujjain, Indore, Delhi, Mumbai, or Jaipur.")

    # Format origin attractions with photos, icons and badges
    origin_places = []
    for idx, a in enumerate(result.get("origin_attractions", [])):
        ptype = a.get("type", "Religious")
        origin_places.append({
            **a,
            "image": place_img(a["name"], location, ptype),
            "icon": ATTRACTION_ICONS.get(ptype, "place"),
            "is_top_pick": idx < 2,
        })

    nearby = []
    for p in result["nearby"][:8]:
        top_attr = p["attractions"][0] if p["attractions"] else None
        sig = top_attr.get("category","") if top_attr else ""
        transport_list = []
        for t in p["transport"]:
            transport_list.append({
                "mode": t["mode"], "icon": MODE_ICONS.get(t["mode"],"directions_car"),
                "price_display": f"\u20b9{t['price_inr']:,}", "duration": f"{t['duration_hrs']}h"
            })
        nearby.append({
            **p, "image": img(p["city"], sig),
            "description": top_attr["description"] if top_attr else f"Explore {p['city']}",
            "transport": transport_list,
        })

    return render_template("explore.html", active_page="explore",
        origin=result["origin"], origin_places=origin_places, nearby=nearby,
        budget=budget, trip_type=trip_type, days=days,
        budget_label=BUDGET_LABELS.get(budget,"Standard"),
        trip_type_label=TRIP_LABELS.get(trip_type,"Spiritual"),
        cluster_theme=result["cluster_theme"], query=query,
        origin_image=img(location))

@app.route("/stays")
def stays():
    location = request.args.get("location", "Ujjain")
    dest = request.args.get("dest", "")
    budget = request.args.get("budget", "medium")
    trip_type = request.args.get("trip_type", "balanced")
    days = request.args.get("days", 3, type=int)
    query = build_query(location, budget, trip_type, days, dest)

    result = recommender.get_recommendations(location, budget, trip_type)
    if result is None:
        return render_template("index.html", active_page="home",
                               locations=recommender.get_all_city_names(),
                               error=f"City '{location}' not found.")

    target = None
    for p in result["nearby"]:
        if p["city"].lower() == dest.lower():
            target = p
            break
    if not target and result["nearby"]:
        target = result["nearby"][0]

    transport = []
    stays_list = []
    dest_city = dest_state = ""
    if target:
        dest_city = target["city"]
        dest_state = target["state"]
        for t in target["transport"]:
            transport.append({
                "mode": t["mode"], "icon": MODE_ICONS.get(t["mode"],"directions_car"),
                "price_display": f"\u20b9{t['price_inr']:,}", "duration": f"{t['duration_hrs']}h"
            })
        stays_list = target["stays"]

    return render_template("stays.html", active_page="stays",
        origin=location, dest_city=dest_city, dest_state=dest_state,
        dest_image=img(dest_city), transport=transport, stays=stays_list,
        cluster_theme=result["cluster_theme"], query=query, days=days)

@app.route("/planner")
def planner():
    location = request.args.get("location", "Ujjain")
    dest = request.args.get("dest", "")
    budget = request.args.get("budget", "medium")
    trip_type = request.args.get("trip_type", "balanced")
    days = request.args.get("days", 3, type=int)
    query = build_query(location, budget, trip_type, days, dest)

    plan = recommender.generate_itinerary(location, dest_name=dest, budget=budget, trip_type=trip_type, days=days)
    if plan is None:
        return render_template("index.html", active_page="home",
                               locations=recommender.get_all_city_names(),
                               error=f"City '{location}' not found.")

    itinerary = plan["itinerary"]
    for item in itinerary:
        item["image"] = img(item["city"])

    trip_title = f"{location} → {dest} Circuit ({days} Days)" if dest else f"{location} & Regional Circuit ({days} Days)"

    return render_template("planner.html", active_page="planner",
        origin=location, dest=dest, trip_name=trip_title,
        itinerary=itinerary, itinerary_json=json.dumps(itinerary),
        center_lat=plan["center_lat"], center_lng=plan["center_lng"],
        total_distance=plan["total_distance_km"], days=days,
        budget=budget, trip_type=trip_type, query=query)

@app.route("/api/locations")
def api_locations():
    return jsonify({"options": recommender.get_all_city_names()})

# Train ML model on startup
recommender.fit()

if __name__ == "__main__":
    print("=" * 50)
    print("  Trip Planner India")
    print("  Flask + Machine Learning Backend")
    print("=" * 50)
    print(f"\n  Open http://localhost:5000\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
