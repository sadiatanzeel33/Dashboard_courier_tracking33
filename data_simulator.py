import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Courier status types
statuses = ['In Transit', 'Delivered', 'Delayed', 'Out for Delivery']

# Major cities with approximate lat/lon
cities = [
    {"name": "Karachi", "lat": 24.8607, "lon": 67.0011},
    {"name": "Lahore", "lat": 31.5497, "lon": 74.3436},
    {"name": "Islamabad", "lat": 33.6844, "lon": 73.0479},
    {"name": "Quetta", "lat": 30.1798, "lon": 66.9750},
    {"name": "Peshawar", "lat": 34.0151, "lon": 71.5249},
    {"name": "Multan", "lat": 30.1575, "lon": 71.5249},
    {"name": "Faisalabad", "lat": 31.4180, "lon": 73.0791},
    {"name": "Rawalpindi", "lat": 33.5651, "lon": 73.0169}
]

def generate_tracking_data(num_entries=100):
    base_time = datetime.now()
    data = []

    for i in range(num_entries):
        status = random.choice(statuses)
        city = random.choice(cities)

        # Add slight variation to lat/lon around city center
        lat = city["lat"] + np.random.uniform(-0.1, 0.1)
        lon = city["lon"] + np.random.uniform(-0.1, 0.1)

        data.append({
            'Package ID': f'PKG-{1000 + i}',
            'Customer': f'Customer-{i}',
            'City': city["name"],
            'Status': status,
            'Updated At': base_time - timedelta(minutes=random.randint(0, 180)),
            'Latitude': lat,
            'Longitude': lon
        })

    return pd.DataFrame(data)

