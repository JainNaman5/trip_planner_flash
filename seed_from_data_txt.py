"""
seed_from_data_txt.py - Rebuilds trip_planner.db from data___.txt places
Run once: python seed_from_data_txt.py
"""
import sqlite3, os, math, random

random.seed(42)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trip_planner.db")

INDIA_CITY_TOURIST_PLACES = {
    "Andhra Pradesh": {
        "Visakhapatnam": ["RK Beach","Submarine Museum","Kailasagiri","Borra Caves","Rushikonda Beach"],
        "Vijayawada": ["Kanaka Durga Temple","Undavalli Caves","Prakasam Barrage","Bhavani Island"],
        "Tirupati": ["Sri Venkateswara Swamy Temple","Kapila Theertham","Chandragiri Fort"],
        "Kurnool": ["Belum Caves","Konda Reddy Fort","Oravakallu Rock Garden"],
    },
    "Arunachal Pradesh": {
        "Itanagar": ["Ita Fort","Ganga Lake","Gompa Buddhist Temple","Jawaharlal Nehru State Museum"],
        "Tawang": ["Tawang Monastery","Sela Pass","Madhuri Lake","Nuranang Falls"],
        "Ziro": ["Talley Valley Wildlife Sanctuary","Meghna Cave Temple","Kardo Shiva Lingam"],
    },
    "Assam": {
        "Guwahati": ["Kamakhya Temple","Umananda Island","Assam State Museum","Deepor Beel","Brahmaputra Riverfront"],
        "Tezpur": ["Agnigarh","Cole Park","Bamuni Hills"],
        "Jorhat": ["Majuli Island","Hoollongapar Gibbon Sanctuary","Gymkhana Club"],
    },
    "Bihar": {
        "Patna": ["Golghar","Patna Sahib Gurudwara","Bihar Museum","Kumhrar Ruins","Sanjay Gandhi Biological Park"],
        "Gaya": ["Mahabodhi Temple","Great Buddha Statue","Vishnupad Temple","Dungeshwari Cave"],
        "Nalanda": ["Nalanda University Ruins","Vishwa Shanti Stupa","Venu Vana","Griddhakuta Peak","Rajgir 5 Hills Jain Temples"],
        "Pawapuri": ["Jal Mandir Pavapuri (Mahavira Swami Nirvana Sthal)","Samosharan Mandir","Gaon Mandir Pavapuri","Maniyar Math"],
    },
    "Chhattisgarh": {
        "Raipur": ["Swami Vivekananda Sarovar","Nandan Van Zoo","Marine Drive Raipur","Mahant Ghasidas Museum"],
        "Bilaspur": ["Kanan Pendari Zoo","Ratanpur Mahamaya Temple","Khutaghat Dam"],
        "Jagdalpur": ["Chitrakote Waterfalls","Tirathgarh Falls","Kanger Valley National Park"],
    },
    "Goa": {
        "Panaji": ["Basilica of Bom Jesus","Se Cathedral","Miramar Beach","Fort Aguada","Church of Immaculate Conception"],
        "Margao": ["Colva Beach","Benaulim Beach","Holy Spirit Church","Monte Hill"],
    },
    "Gujarat": {
        "Ahmedabad": ["Sabarmati Ashram","Hutheesing Jain Temple","Adalaj Stepwell","Sidi Saiyyed Mosque","Kankaria Lake","Science City"],
        "Palitana": ["Shatrunjaya Tirth Hill (Adinath Bhagwan)","Shri Adishwar Jain Temple","Chaumukha Mandir","Hastagiri Jain Tirth","Gheeti Tirth"],
        "Surat": ["Dumas Beach","Surat Castle","Dutch Garden","Gopi Talav"],
        "Vadodara": ["Laxmi Vilas Palace","Sayaji Baug","Baroda Museum","Champaner-Pavagadh Jain Temples"],
        "Rajkot": ["Watson Museum","Kaba Gandhi No Delo","Pradhyuman Zoological Park"],
        "Junagadh": ["Girnar Jain Tirth (Neminatha Nirvana Sthal)","Uparkot Fort","Mahabat Maqbara","Gir National Park Safari"],
        "Shankheshwar": ["Shankheshwar Parshwanath Jain Tirth","Padmavati Mata Mandir","Jain Museum Shankheshwar"],
    },
    "Haryana": {
        "Gurugram": ["Kingdom of Dreams","Cyber Hub","Sultanpur National Park","Vintage Camera Museum"],
        "Faridabad": ["Badkhal Lake","Surajkund Lake","Raja Nahar Singh Palace"],
        "Kurukshetra": ["Brahma Sarovar","Jyotisar","Panorama and Science Centre","Sannihit Sarovar"],
        "Panchkula": ["Pinjore Gardens","Cactus Garden","Morni Hills","Nada Sahib Gurudwara"],
    },
    "Himachal Pradesh": {
        "Shimla": ["The Ridge","Mall Road","Jakhoo Temple","Kalka-Shimla Toy Train","Christ Church"],
        "Manali": ["Solang Valley","Rohtang Pass","Hadimba Temple","Old Manali","Jogini Falls"],
        "Dharamshala": ["Tsuglagkhang Complex","Bhagsunag Waterfall","Namgyal Monastery","HPCA Stadium"],
    },
    "Jharkhand": {
        "Shikharji": ["Shri Sammed Shikharji (20 Tirthankara Nirvana Sthal)","Parasnath Hill Holy Tonks","Madhuban Jain Temples","Gandharva Nala Tirth","Digambar Jain Teerth Kshetra"],
        "Ranchi": ["Hundru Falls","Jonha Falls","Dassam Falls","Pahari Mandir","Tagore Hill"],
        "Jamshedpur": ["Jubilee Park","Dimna Lake","Dalma Wildlife Sanctuary","Tata Steel Zoological Park"],
        "Dhanbad": ["Maithon Dam","Panchet Dam","Topchanchi Lake","Shakti Mandir"],
    },
    "Karnataka": {
        "Bengaluru": ["Lalbagh Botanical Garden","Cubbon Park","Bangalore Palace","Bannerghatta National Park","Tipu Sultan Summer Palace"],
        "Shravanabelagola": ["Gommateshwara Bahubali Statue (57 ft)","Vindhyagiri Hill Tirth","Chandragiri Hill Basadis","Odegal Basadi","Bhandari Basadi"],
        "Moodbidri": ["Moodbidri Thousand Pillar Jain Temple (Savira Kambada Basadi)","Guru Basadi","Tribhangi Parshwanatha Temple","Karkala Gommateshwara Statue"],
        "Mysuru": ["Mysore Palace","Chamundi Hill","Brindavan Gardens","Mysore Zoo","St Philomenas Cathedral"],
        "Hampi": ["Virupaksha Temple","Vijaya Vittala Temple","Lotus Mahal","Elephant Stables","Matanga Hill"],
        "Mangaluru": ["Panambur Beach","Kadri Manjunath Temple","St Aloysius Chapel","Tannirbhavi Beach"],
    },
    "Kerala": {
        "Thiruvananthapuram": ["Padmanabhaswamy Temple","Kovalam Beach","Napier Museum","Shangumugham Beach"],
        "Kochi": ["Fort Kochi","Chinese Fishing Nets","Mattancherry Palace","Marine Drive Kochi","Santa Cruz Basilica"],
        "Munnar": ["Tea Museum","Eravikulam National Park","Mattupetty Dam","Anamudi Peak","Top Station"],
        "Alappuzha": ["Alappuzha Beach","Vembanad Lake","Marari Beach","Pathiramanal Island"],
    },
    "Madhya Pradesh": {
        "Ujjain": ["Mahakaleshwar Jyotirlinga","Mahavir Tapobhumi Jain Tirth","Digambar Jain Siddhakshetra (Jaisinghpura)","Shri Avanti Parshwanath Jain Shwetambar Tirth","Ram Ghat","Kal Bhairav Temple","Harsiddhi Temple","Vedh Shala","Mangalnath Temple"],
        "Indore": ["Kanch Mandir (Glass Jain Temple)","Gomatgiri Jain Tirth (Bahubali Colossus)","Rajwada Palace","Lal Bagh Palace","Sarafa Bazaar","Chappan Dukan"],
        "Sonagiri": ["Sonagiri Golden Peak Jain Tirth (108 White Temples)","Bhagwan Chandraprabhu Temple","Panch Balyati Tirth","Sheetalnath Bhagwan Temple"],
        "Kundalpur": ["Kundalpur Bade Baba Digambar Jain Mandir","Kundalpur Giri Parvat","Vardhman Sagar Lake","Rukmini Kund Tirth"],
        "Gwalior": ["Gwalior Fort","Gopachal Parvat Jain Rock Colossi","Siddhachal Jain Caves","Jai Vilas Palace","Sun Temple Gwalior"],
        "Khajuraho": ["Parshvanatha Jain Temple","Shantinatha Jain Temple","Ghantai Jain Temple","Kandariya Mahadeva Temple","Lakshmana Temple"],
        "Omkareshwar": ["Omkareshwar Jyotirlinga","Mamleshwar Temple","Narmada Ghats","Siddhanath Temple"],
        "Mandu": ["Jahaz Mahal","Suparshvanath Jain Mandir Mandu","Hindola Mahal","Rani Roopmati Pavilion","Baz Bahadur Palace"],
        "Maheshwar": ["Ahilya Fort","Maheshwar Ghats","Ahilyabai Holkar Temple","Narmada Riverfront"],
        "Bhopal": ["Manua Bhan Ki Tekri Jain Tirth","Upper Lake Bhojtal","Van Vihar National Park","Bharat Bhavan","Taj-ul-Masajid"],
        "Pachmarhi": ["Bee Falls","Jata Shankar Cave","Dhoopgarh","Pandava Caves"],
        "Orchha": ["Orchha Fort Complex","Ram Raja Temple","Chaturbhuj Temple","Jahangir Mahal"],
        "Jabalpur": ["Bhedaghat Marble Rocks","Dhuandhar Falls","Pisanhari Ki Madiya Jain Tirth","Chausath Yogini Temple"],
    },
    "Maharashtra": {
        "Mumbai": ["Gateway of India","Babu Amichand Panalal Jain Temple (Walkeshwar)","Godiji Parshwanath Jain Mandir","Marine Drive","Elephanta Caves","Siddhivinayak Temple"],
        "Pune": ["Katraj Jain Temple (Aagam Mandir)","Shaniwar Wada","Aga Khan Palace","Sinhagad Fort","Dagdusheth Ganapati Temple"],
        "Mangi Tungi": ["Mangi Tungi Siddhakshetra (108 ft Rishabhdeva Statue)","Ram-Sita Guha","Krishna Balaram Samadhi Tirth"],
        "Nagpur": ["Deekshabhoomi","Futala Lake","Ambazari Lake","Sitabuldi Fort"],
        "Nashik": ["Gajpantha Jain Siddhakshetra (Mhasrul)","Trimbakeshwar Shiva Temple","Pandavleni Caves","Panchavati"],
        "Aurangabad": ["Ellora Caves Jain Cave Group (Indra Sabha)","Ajanta Caves","Bibi Ka Maqbara","Daulatabad Fort"],
    },
    "Manipur": {
        "Imphal": ["Loktak Lake","Kangla Fort","INA War Museum","Keibul Lamjao National Park","Ima Keithel Mothers Market"],
    },
    "Meghalaya": {
        "Shillong": ["Umiam Lake","Elephant Falls","Shillong Peak","Wards Lake","Don Bosco Museum"],
        "Cherrapunji": ["Nohkalikai Falls","Double Decker Living Root Bridge","Mawsmai Cave","Seven Sisters Falls"],
    },
    "Mizoram": {
        "Aizawl": ["Solomons Temple","Durtlang Hills","Mizoram State Museum","Reiek Heritage Village","KV Paradise"],
    },
    "Nagaland": {
        "Kohima": ["Kohima War Cemetery","Kisama Heritage Village","Dzukou Valley","Nagaland State Museum"],
        "Dimapur": ["Kachari Ruins","Triple Falls","Diezephe Craft Village"],
    },
    "Odisha": {
        "Bhubaneswar": ["Lingaraj Temple","Udayagiri Khandagiri Jain Caves","Nandankanan Zoological Park","Mukteshwar Temple"],
        "Puri": ["Jagannath Temple","Puri Beach","Chilika Lake","Gundicha Temple"],
        "Konark": ["Konark Sun Temple","Chandrabhaga Beach","Ramachandi Temple"],
    },
    "Punjab": {
        "Amritsar": ["Golden Temple Harmandir Sahib","Jallianwala Bagh","Wagah Border","Gobindgarh Fort"],
        "Ludhiana": ["Lodhi Fort","Nehru Rose Garden","Punjab Agricultural University Museum"],
        "Patiala": ["Qila Mubarak","Sheesh Mahal","Baradari Garden","Gurdwara Dukh Niwaran Sahib"],
    },
    "Rajasthan": {
        "Mount Abu": ["Dilwara Jain Temples (Vimal & Luna Vasahi)","Achalgarh Jain Temple","Nakki Lake","Guru Shikhar Peak","Sunset Point"],
        "Ranakpur": ["Ranakpur Jain Temple (1444 Carved Pillars)","Chaumukha Mandir Ranakpur","Surya Narayan Temple","Suparshvanatha Mandir"],
        "Jaipur": ["Shri Padampura Digambar Jain Tirth","Sanganer Digambar Jain Mandir","Amber Fort","Hawa Mahal","City Palace Jaipur","Nahargarh Fort"],
        "Udaipur": ["Kesariyaji Rishabhdeo Jain Tirth","City Palace Udaipur","Lake Pichola","Jag Mandir","Saheliyon-ki-Bari"],
        "Jodhpur": ["Osian Jain Temples","Mehrangarh Fort","Umaid Bhawan Palace","Jaswant Thada","Mandore Gardens"],
        "Jaisalmer": ["Jaisalmer Fort Jain Temples (Chandraprabhu)","Lodurva Parshwanath Jain Tirth","Sam Sand Dunes","Patwon Ki Haveli"],
    },
    "Sikkim": {
        "Gangtok": ["Tsomgo Lake","Rumtek Monastery","Nathula Pass","Ban Jhakri Falls","MG Marg"],
        "Pelling": ["Pemayangtse Monastery","Rabdentse Ruins","Skywalk Pelling","Kanchenjunga Falls"],
    },
    "Tamil Nadu": {
        "Chennai": ["Marina Beach","Kapaleeshwarar Temple","Fort St George","San Thome Basilica","Guindy National Park"],
        "Madurai": ["Meenakshi Amman Temple","Thirumalai Nayakkar Mahal","Gandhi Memorial Museum","Alagar Koyil"],
        "Coimbatore": ["Adiyogi Shiva Statue","Marudhamalai Murugan Temple","VOC Park","Siruvani Waterfalls"],
        "Tiruchirappalli": ["Rockfort Temple","Sri Ranganathaswamy Temple Srirangam","Jambukeswarar Temple"],
    },
    "Telangana": {
        "Hyderabad": ["Charminar","Golconda Fort","Kulpakji Jain Tirth (Kolanupaka)","Ramoji Film City","Salar Jung Museum"],
        "Warangal": ["Warangal Fort","Thousand Pillar Temple","Bhadrakali Temple","Ramappa Temple"],
    },
    "Tripura": {
        "Agartala": ["Ujjayanta Palace","Neermahal Water Palace","Tripura Sundari Temple","Heritage Park Agartala"],
    },
    "Uttar Pradesh": {
        "Ayodhya": ["Shri Ram Mandir","Ayodhya Jain Tirth (Birthplace of 5 Tirthankaras)","Badi Murti Digambar Jain Mandir","Hanuman Garhi","Kanak Bhawan","Saryu Ghat"],
        "Hastinapur": ["Jambudweep Jain Tirth","Shantinath Digambar Jain Temple","Kailash Parvat Jain Rachna","Ashtapad Jain Tirth"],
        "Agra": ["Taj Mahal","Agra Fort","Fatehpur Sikri","Mehtab Bagh","Akbar Tomb Sikandra"],
        "Varanasi": ["Bhelupur Jain Tirth (Parshvanatha Janmabhumi)","Chandrawati Jain Tirth","Kashi Vishwanath Temple","Dashashwamedh Ghat","Sarnath"],
        "Lucknow": ["Bara Imambara","Chota Imambara","Rumi Darwaza","Ambedkar Memorial Park","The Residency"],
        "Mathura": ["Chaurasi Digambar Jain Mandir Mathura","Krishna Janmasthan Temple","Banke Bihari Temple","Prem Mandir"],
        "Prayagraj": ["Prabhasgiri Jain Tirth (Padmaprabhu)","Triveni Sangam","Allahabad Fort","Anand Bhavan"],
    },
    "Uttarakhand": {
        "Dehradun": ["Robbers Cave Guchhupani","Sahastradhara","Tapkeshwar Temple","Forest Research Institute"],
        "Rishikesh": ["Laxman Jhula","Ram Jhula","Triveni Ghat","Parmarth Niketan","Beatles Ashram"],
        "Haridwar": ["Har Ki Pauri","Mansa Devi Temple","Chandi Devi Temple","Maya Devi Temple"],
        "Nainital": ["Naini Lake","Naina Devi Temple","Snow View Point","Tiffin Top"],
    },
    "West Bengal": {
        "Kolkata": ["Pareshnath Jain Temple (Calcutta Jain Temple)","Victoria Memorial","Howrah Bridge","Dakshineswar Kali Temple","Indian Museum"],
        "Darjeeling": ["Tiger Hill","Batasia Loop","Darjeeling Himalayan Railway Toy Train","Peace Pagoda","Rock Garden"],
        "Siliguri": ["Bengal Safari","Salugara Monastery","Mahananda Wildlife Sanctuary"],
    },
    "Delhi": {
        "Delhi": ["Shri Digambar Jain Lal Mandir (Chandni Chowk)","Ahinsa Sthal (Mehrauli Mahavira Statue)","Red Fort","Qutub Minar","India Gate","Lotus Temple","Akshardham Temple"],
    },
    "Chandigarh": {
        "Chandigarh": ["Rock Garden Chandigarh","Sukhna Lake","Rose Garden","Sector 17 Plaza"],
    },
    "Puducherry": {
        "Puducherry": ["Promenade Beach","Auroville","Sri Aurobindo Ashram","Paradise Beach","French Quarter"],
    },
    "Jammu and Kashmir": {
        "Srinagar": ["Dal Lake","Shalimar Bagh","Nishat Bagh","Shankaracharya Temple","Hazratbal Shrine"],
        "Jammu": ["Vaishno Devi Temple Katra","Raghunath Temple","Amar Mahal Palace Museum","Bahu Fort"],
    },
    "Ladakh": {
        "Leh": ["Pangong Tso","Khardung La","Leh Palace","Shanti Stupa","Thiksey Monastery"],
    },
    "Andaman and Nicobar": {
        "Port Blair": ["Cellular Jail","Ross Island","Radhanagar Beach Havelock","Corbyns Cove Beach"],
    },
}

CITY_COORDS = {
    "Delhi":(28.6139,77.2090),"Mumbai":(19.0760,72.8777),"Jaipur":(26.9124,75.7873),
    "Agra":(27.1767,78.0081),"Varanasi":(25.3176,82.9739),"Udaipur":(24.5854,73.7125),
    "Shimla":(31.1048,77.1734),"Manali":(32.2396,77.1887),"Rishikesh":(30.0869,78.2676),
    "Amritsar":(31.6340,74.8723),"Bengaluru":(12.9716,77.5946),"Chennai":(13.0827,80.2707),
    "Hyderabad":(17.3850,78.4867),"Kochi":(9.9312,76.2673),"Mysuru":(12.2958,76.6394),
    "Munnar":(10.0889,77.0595),"Kolkata":(22.5726,88.3639),"Darjeeling":(27.0360,88.2627),
    "Gangtok":(27.3389,88.6065),"Puri":(19.8135,85.8312),"Bhopal":(23.2599,77.4126),
    "Jodhpur":(26.2389,73.0243),"Pune":(18.5204,73.8567),"Ahmedabad":(23.0225,72.5714),
    "Leh":(34.1526,77.5771),"Alappuzha":(9.4981,76.3388),"Hampi":(15.3350,76.4600),
    "Lucknow":(26.8467,80.9462),"Chandigarh":(30.7333,76.7794),"Srinagar":(34.0837,74.7973),
    "Haridwar":(29.9457,78.1642),"Nainital":(29.3803,79.4636),"Dehradun":(30.3165,78.0322),
    "Mathura":(27.4924,77.6737),"Jaisalmer":(26.9157,70.9083),"Nashik":(20.0112,73.7903),
    "Madurai":(9.9252,78.1198),"Coimbatore":(11.0168,76.9558),"Visakhapatnam":(17.6868,83.2185),
    "Vijayawada":(16.5062,80.6480),"Tirupati":(13.6288,79.4192),"Mangaluru":(12.9141,74.8560),
    "Guwahati":(26.1445,91.7362),"Ranchi":(23.3441,85.3096),"Patna":(25.6093,85.1376),
    "Indore":(22.7196,75.8577),"Gwalior":(26.2183,78.1828),"Ujjain":(23.1765,75.7885),
    "Omkareshwar":(22.2435,76.1500),"Mandu":(22.3660,75.3429),"Maheshwar":(22.1764,75.5843),
    "Khajuraho":(24.8318,79.9199),"Orchha":(25.3512,78.6416),"Pachmarhi":(22.4674,78.4346),
    "Jabalpur":(23.1815,79.9864),"Jammu":(32.7266,74.8570),"Kurnool":(15.8281,78.0373),
    "Itanagar":(27.0844,93.6053),"Tawang":(27.5860,91.8596),"Ziro":(27.5418,93.8259),
    "Tezpur":(26.6338,92.7936),"Jorhat":(26.7465,94.2026),"Gaya":(24.7964,84.9940),
    "Nalanda":(25.1359,85.4438),"Raipur":(21.2514,81.6296),"Bilaspur":(22.0796,82.1391),
    "Jagdalpur":(19.0829,82.0167),"Panaji":(15.4909,73.8278),"Margao":(15.2736,73.9600),
    "Surat":(21.1702,72.8311),"Vadodara":(22.3072,73.1812),"Rajkot":(22.3039,70.8022),
    "Gurugram":(28.4595,77.0266),"Faridabad":(28.4089,77.3178),"Kurukshetra":(29.9695,76.8783),
    "Panchkula":(30.6942,76.8606),"Dharamshala":(32.2190,76.3234),"Jamshedpur":(22.8046,86.2029),
    "Dhanbad":(23.7957,86.4304),"Nagpur":(21.1458,79.0882),"Aurangabad":(19.8762,75.3433),
    "Imphal":(24.8170,93.9368),"Shillong":(25.5788,91.8933),"Cherrapunji":(25.2841,91.7263),
    "Aizawl":(23.7271,92.7176),"Kohima":(25.6747,94.1086),"Dimapur":(25.9044,93.7239),
    "Bhubaneswar":(20.2961,85.8245),"Konark":(19.8876,86.0945),"Ludhiana":(30.9010,75.8573),
    "Patiala":(30.3398,76.3869),"Pelling":(27.2989,88.2318),"Tiruchirappalli":(10.7905,78.7047),
    "Warangal":(17.9689,79.5941),"Agartala":(23.8315,91.2868),"Prayagraj":(25.4358,81.8463),
    "Siliguri":(26.7271,88.3953),"Thiruvananthapuram":(8.5241,76.9366),"Port Blair":(11.6234,92.7265),
    "Puducherry":(11.9416,79.8083),
    # Top Jain Tirth Kshetra coordinates
    "Palitana": (21.5222, 71.8290),
    "Shikharji": (23.9628, 86.1364),
    "Mount Abu": (24.5926, 72.7156),
    "Ranakpur": (25.1166, 73.4735),
    "Shravanabelagola": (12.8574, 76.4862),
    "Sonagiri": (25.7000, 78.3300),
    "Kundalpur": (24.0300, 79.5800),
    "Pawapuri": (25.0933, 85.5264),
    "Hastinapur": (29.1700, 78.0200),
    "Ayodhya": (26.7922, 82.1998),
    "Moodbidri": (13.0700, 74.9900),
    "Mangi Tungi": (20.8400, 74.0700),
    "Junagadh": (21.5222, 70.4579),
    "Shankheshwar": (23.5000, 71.7800),
}

STATE_COORDS = {
    "Andhra Pradesh":(15.9129,79.7400),"Arunachal Pradesh":(28.2180,94.7278),
    "Assam":(26.2006,92.9376),"Bihar":(25.0961,85.3131),"Chhattisgarh":(21.2787,81.8661),
    "Goa":(15.2993,73.9512),"Gujarat":(22.2587,71.1924),"Haryana":(29.0588,76.0856),
    "Himachal Pradesh":(31.1048,77.1734),"Jharkhand":(23.6102,85.2799),
    "Karnataka":(15.3173,75.7139),"Kerala":(10.8505,76.2711),"Madhya Pradesh":(22.9734,78.6569),
    "Maharashtra":(19.7515,75.7139),"Manipur":(24.6637,93.9063),"Meghalaya":(25.4670,91.3662),
    "Mizoram":(23.1645,92.9376),"Nagaland":(26.1584,94.5624),"Odisha":(20.9517,85.0985),
    "Punjab":(31.1471,75.3412),"Rajasthan":(27.0238,74.2179),"Sikkim":(27.5330,88.5122),
    "Tamil Nadu":(11.1271,78.6569),"Telangana":(18.1124,79.0193),"Tripura":(23.9408,91.9882),
    "Uttar Pradesh":(26.8467,80.9462),"Uttarakhand":(30.0668,79.0193),"West Bengal":(22.9868,87.8550),
    "Delhi":(28.6139,77.2090),"Chandigarh":(30.7333,76.7794),"Puducherry":(11.9416,79.8083),
    "Jammu and Kashmir":(33.7782,76.5762),"Ladakh":(34.1526,77.5771),
    "Andaman and Nicobar":(11.7401,92.6586),
}

RELIGIOUS_KW=["temple","mandir","masjid","mosque","church","gurudwara","shrine","ghat","monastery",
              "stupa","ashram","jyotirlinga","basilica","cathedral","pagoda","sahib","gurdwara",
              "jain","tirth","derasar","basadi","shikharji","shatrunjaya","bahubali","tirthankara","tapobhumi","siddhakshetra"]
HISTORICAL_KW=["fort","palace","mahal","ruins","museum","tomb","gate","memorial","jail","minar",
               "qila","haveli","arch","terminus"]
NATURE_KW=["lake","falls","waterfall","valley","beach","garden","park","forest","wildlife",
           "sanctuary","dam","river","cave","hill","peak","pass","island","zoo","botanical",
           "beel","tso","safari"]
ADVENTURE_KW=["solang","rohtang","skywalk","khardung la","trek"]

def guess_type(name):
    n=name.lower()
    if any(k in n for k in RELIGIOUS_KW): return("Religious","Religious")
    if any(k in n for k in HISTORICAL_KW): return("Historical","Historical")
    if any(k in n for k in ADVENTURE_KW): return("Adventure","Adventure")
    if any(k in n for k in NATURE_KW): return("Nature","Nature")
    return("Scenic","Scenic")

def get_coords(city,state=""):
    if city in CITY_COORDS: return CITY_COORDS[city]
    cl=city.lower()
    for k,v in CITY_COORDS.items():
        if cl in k.lower() or k.lower() in cl: return v
    if state in STATE_COORDS:
        slat,slng=STATE_COORDS[state]
        return(slat+random.uniform(-0.5,0.5),slng+random.uniform(-0.5,0.5))
    return(22.0+random.uniform(-3,3),78.0+random.uniform(-5,5))

def haversine(lat1,lon1,lat2,lon2):
    R=6371
    dlat,dlon=math.radians(lat2-lat1),math.radians(lon2-lon1)
    a=math.sin(dlat/2)**2+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return R*2*math.asin(math.sqrt(a))

def create_tables(cur):
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS cities(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,state TEXT NOT NULL,zone TEXT,lat REAL NOT NULL,lng REAL NOT NULL);
    CREATE TABLE IF NOT EXISTS attractions(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,city_id INTEGER NOT NULL,type TEXT,significance TEXT,popularity REAL DEFAULT 5,google_rating REAL,entrance_fee INTEGER DEFAULT 0,best_time TEXT,description TEXT,lat REAL,lng REAL,FOREIGN KEY(city_id)REFERENCES cities(id));
    CREATE TABLE IF NOT EXISTS transport(id INTEGER PRIMARY KEY AUTOINCREMENT,from_city_id INTEGER NOT NULL,to_city_id INTEGER NOT NULL,mode TEXT NOT NULL,price_inr INTEGER NOT NULL,duration_hrs REAL NOT NULL,FOREIGN KEY(from_city_id)REFERENCES cities(id),FOREIGN KEY(to_city_id)REFERENCES cities(id));
    CREATE TABLE IF NOT EXISTS stays(id INTEGER PRIMARY KEY AUTOINCREMENT,city_id INTEGER NOT NULL,name TEXT NOT NULL,type TEXT NOT NULL,price_per_night INTEGER NOT NULL,rating REAL DEFAULT 4.0,FOREIGN KEY(city_id)REFERENCES cities(id));
    """)

def main():
    if os.path.exists(DB_PATH): os.remove(DB_PATH)
    conn=sqlite3.connect(DB_PATH); cur=conn.cursor(); create_tables(cur)
    city_map={}; total=0
    for state,cities in INDIA_CITY_TOURIST_PLACES.items():
        for city,places in cities.items():
            key=(city.lower(),state.lower()); lat,lng=get_coords(city,state)
            if key not in city_map:
                cur.execute("INSERT INTO cities(name,state,zone,lat,lng)VALUES(?,?,?,?,?)",(city,state,None,lat,lng))
                city_map[key]=cur.lastrowid
            cid=city_map[key]
            for idx,place in enumerate(places):
                ptype,sig=guess_type(place)
                pop=round(max(4.0, 9.6 - idx*0.4), 1)
                rating=round(min(4.9, 4.8 - idx*0.1), 1)
                desc=f"{place} is a premier {ptype.lower()} destination and must-visit attraction in {city}, {state}."
                cur.execute("INSERT INTO attractions(name,city_id,type,significance,popularity,google_rating,entrance_fee,best_time,description,lat,lng)VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                    (place,cid,ptype,sig,pop,rating,random.choice([0,0,50,100,200,500]),"October to March",desc,
                     lat+random.uniform(-0.02,0.02),lng+random.uniform(-0.02,0.02))); total+=1
    print(f"Cities: {len(city_map)}, Attractions: {total}")
    cities_db=cur.execute("SELECT id,name,lat,lng FROM cities").fetchall()
    tr=[]
    for i,c1 in enumerate(cities_db):
        for j,c2 in enumerate(cities_db):
            if i==j: continue
            d=haversine(c1[2],c1[3],c2[2],c2[3])
            if d>1200: continue
            tr.append((c1[0],c2[0],"Car",int(d*8),round(d/60,1)))
            tr.append((c1[0],c2[0],"Bus",int(d*3),round(d/45,1)))
            if d>50: tr.append((c1[0],c2[0],"Train",int(d*2),round(d/70,1)))
            if d>400: tr.append((c1[0],c2[0],"Flight",int(1500+d*3),round(d/700+1,1)))
    cur.executemany("INSERT INTO transport(from_city_id,to_city_id,mode,price_inr,duration_hrs)VALUES(?,?,?,?,?)",tr)
    print(f"Transport routes: {len(tr)}")
    tmpl=[("budget",["Backpacker Hostel","Budget Inn","Guest House"],500,1500,3.5),
          ("mid_range",["Comfort Hotel","Heritage Stay","City Hotel"],2000,5000,4.0),
          ("luxury",["Grand Palace Hotel","Luxury Resort","Premium Suite"],6000,15000,4.5)]
    sr=[]
    for cid,cname,_,_ in cities_db:
        for typ,names,lo,hi,br in tmpl:
            sr.append((cid,f"{random.choice(names)} {cname}",typ,random.randint(lo,hi),round(min(br+random.uniform(-0.3,0.5),5.0),1)))
    cur.executemany("INSERT INTO stays(city_id,name,type,price_per_night,rating)VALUES(?,?,?,?,?)",sr)
    conn.commit()
    for t in["cities","attractions","transport","stays"]:
        cur.execute(f"SELECT COUNT(*) FROM {t}"); print(f"  {t}: {cur.fetchone()[0]}")
    conn.close(); print(f"\nDatabase ready: {DB_PATH}")

if __name__=="__main__": main()
