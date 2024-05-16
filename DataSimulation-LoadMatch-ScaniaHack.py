# Databricks notebook source
import pandas as pd
from datetime import datetime, timedelta

# Function to generate sample data
def generate_sample_data(start_date, end_date):
    data = []
    current_date = start_date
    position_id = 1

    while current_date >= end_date:
        data.append({
            'positionid': position_id,
            'vehicleid': position_id % 3 + 1,
            'timeposition': current_date.strftime('%Y-%m-%d %H:%M:%S'),
            'latitude': 40.7128,
            'longitude': -74.0060,
            'altitude': 50,
            'speed': 60,
            'heading': 90,
            'vehiclestopped': 0,
            'timesave': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'internalnumber': position_id % 3 + 1
        })
        position_id += 1
        current_date -= timedelta(days=1)

    return data

# Define start and end dates
end_date = datetime.now()
start_date = end_date - timedelta(days=90)  # 3 months back

# Generate sample data
sample_data = generate_sample_data(start_date, end_date)

# Create DataFrame
df = pd.DataFrame(sample_data)

# Display DataFrame
print(df)

# COMMAND ----------

# MAGIC %pip install geojson
# MAGIC %pip install overpass

# COMMAND ----------

import requests
import json

# Define the Overpass API endpoint
overpass_url = "http://overpass-api.de/api/interpreter"

# Define the bounding box for Stockholm mainland region
bbox = (59.195, 17.635, 59.387, 18.306)  # (min_latitude, min_longitude, max_latitude, max_longitude)

# Construct the query to search for roads and parking amenities
query = f"""
[out:json];
(
  way["highway"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
  node["amenity"="parking"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
);
out center;
"""

# Send the query to the Overpass API
response = requests.get(overpass_url, params={'data': query})

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Print the results
    for element in data['elements']:
        print(element)
else:
    print("Error:", response.status_code)


# COMMAND ----------

len(data["elements"])


# COMMAND ----------

data

# COMMAND ----------

import random

# Assuming your data is stored in a variable called 'data' and 'elements' key holds the list
elements_list = data["elements"]

# Define the number of samples you want to select
num_samples = 90 * 30  # Adjust this number as needed

elements_with_center = [element for element in elements_list if 'center' in element]

# Perform sampling without replacement
sampled_elements = random.sample(elements_with_center, num_samples)

sampled_coordinates = [element for element in sampled_elements]
sampled_coordinates[0]

# COMMAND ----------

import pandas as pd
from datetime import datetime, timedelta
import random
import numpy as np

# Function to generate sample data for a single vehicle
def generate_vehicle_data(vehicle_id):
    data = []
    start_date = datetime.now() - timedelta(days=90)  # Start date 90 days ago
    position_id = vehicle_id * 1000  # Start position ID for the vehicle
    
    idx_sample_coordinates = vehicle_id - 1

    for _ in range(90):  # Generate data for each day in the last 90 days
        position_id += 1

        # Extract latitude and longitude
        sampled_coordinates_i = sampled_coordinates[idx_sample_coordinates]['center']
        idx_sample_coordinates += 1
        latitude = sampled_coordinates_i['lat']
        longitude = sampled_coordinates_i['lon']


        altitude = random.randint(28, 70)  # Altitude in meters
        # Create the list
        speed = np.random.choice(np.arange(0, 120), p=[0.2]+([0.8/119])*119)
        # speed = random.randint(0, 120 )  # Speed in km/h, considering legal limits
        heading = random.randint(0, 360)  # Heading in degrees
        vehicle_stopped = 0 if speed > 0 else 1  # Vehicle stopped if speed is 0
        timesave = start_date.strftime('%Y-%m-%d %H:%M:%S')

        data.append({
            'positionid': position_id,
            'vehicleid': vehicle_id,
            'timeposition': start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'latitude': latitude,
            'longitude': longitude,
            'altitude': altitude,
            'speed': speed,
            'heading': heading,
            'vehiclestopped': vehicle_stopped,
            'timesave': timesave,
            'internalnumber': position_id % 1000  # Internal number within vehicle
        })
        
        start_date += timedelta(days=1)  # Move to the next day

    return data

# Function to generate sample data for multiple vehicles
def generate_sample_data(num_vehicles):
    data = []
    for vehicle_id in range(1, num_vehicles + 1):
        data.extend(generate_vehicle_data(vehicle_id))
    return data

# Define the number of vehicles
num_vehicles = 30

# Generate sample data
sample_data = generate_sample_data(num_vehicles)

# Create DataFrame
df = pd.DataFrame(sample_data)

# Display DataFrame
print(df)


# COMMAND ----------

# Save DataFrame to CSV with documentation header
csv_filename = 'fleet_management_data.csv'


df.to_csv(csv_filename, index=False)


# COMMAND ----------

pd.read_csv(csv_filename, encoding='utf-8')

# COMMAND ----------

pd

# COMMAND ----------

csv_filename

# COMMAND ----------




# COMMAND ----------


