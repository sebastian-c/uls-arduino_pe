# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 14:26:23 2023

@author: Sebastian
"""

import pymongo
import pandas as pd
import numpy as np


with open("dbinfo.txt", "r") as dbinfo:
    mongo_connection = pymongo.MongoClient(dbinfo.read())
#mongo_connection.list_database_names()
mongo_db = mongo_connection["weather"]
# mongo_db.list_collection_names()
sensors_db = mongo_db["sensors"]
temperature_db = mongo_db["temperature"]

sensor_data = []
for row in sensors_db.find():
    sensor_data.append(row)
    
temperature_data = []
for row in temperature_db.find():
    temperature_data.append(row)


sensor_data = pd.DataFrame(sensor_data)
sensor_data = sensor_data.drop("_id", axis = 1)
temperature_data = pd.DataFrame(temperature_data)
temperature_data = temperature_data.drop("_id", axis = 1)

all_data = sensor_data.merge(temperature_data, on = "SensorID", how = "left")

all_data.Temperature = pd.Series(np.random.randn(all_data.shape[0]) * 4 + 23)

all_data.groupby("location_x")["Temperature"].mean()

