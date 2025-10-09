from math import radians, sin, cos, sqrt, atan2

nhl_arenas = {
    'Anaheim Ducks': (33.807895, -117.876447),
    'Utah Hockey Club': (40.7683, -111.9017),
    'Boston Bruins': (42.366386, -71.061616),
    'Buffalo Sabres': (42.874835, -78.876223),
    'Calgary Flames': (51.037387, -114.052001),
    'Detroit Red Wings': (42.324958, -83.052084),
    'Edmonton Oilers': (53.546562, -113.496529),
    'Florida Panthers': (26.158400, -80.325319),
    'Los Angeles Kings': (34.043094, -118.267062),
    'Montreal Canadiens': (45.496470, -73.569945),
    'San Jose Sharks': (37.332670, -121.901351),
    'Ottawa Senators': (45.296754, -75.927115),
    'Vancouver Canucks': (49.277604, -123.109633),
    'Tampa Bay Lightning': (27.942742, -82.451793),
    'Las Vegas Golden Knights': (36.102908, -115.178132),
    'Toronto Maple Leafs': (43.643540, -79.379028),
    'Chicago Blackhawks': (41.880098, -87.674442),
    'Carolina Hurricanes': (35.802913, -78.722331),
    'Colorado Avalanche': (39.748721, -105.007682),
    'Columbus Blue Jackets': (39.969368, -83.006205),
    'Dallas Stars': (32.790525, -96.810715),
    'New Jersey Devils': (40.733012, -74.172097),
    'Minnesota Wild': (44.944139, -93.100850),
    'New York Islanders': (40.682617, -73.975331),
    'Nashville Predators': (36.159033, -86.778682),
    'New York Rangers': (40.750523, -73.993420),
    'St. Louis Blues': (38.626435, -90.202611),
    'Philadelphia Flyers': (39.901674, -75.171888),
    'Winnipeg Jets': (49.892724, -97.143712),
    'Pittsburgh Penguins': (40.439481, -79.989581),
    'Washington Capitals': (38.898144, -77.020923)
}

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 3958.8  # Earth radius in miles
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c