# potentiometer.py

import serial
import datetime
import time
import json
import re

import pymongo

# make sure the 'COM#' is set according the Windows Device Manager
ARDUINO_COM_PORT = "COM6"
BAUD_RATE = 9600

#Use init.py to create a UUID
with open("uuid.txt", "r") as uuid_file:
    UUID = uuid_file.read()

with open("dbinfo.txt", "r") as dbinfo:
    mongo_connection = pymongo.MongoClient(dbinfo.read())
#Set up db connection
mongo_db = mongo_connection["weather"]
temperature_db = mongo_db["temperature"]

#### TEST
data = "[DATA] {humidity_perc : 14.00, temperature_c : 21.00, heat_index_c : 19.52}"

def identify_message(message):
    if bool(re.search("^\[DATA\]", message)) :
            return("data")
    if bool(re.search("^\[COMMAND\]", message)):
            return("command")
    if bool(re.search("^\[MESSAGE\]", message)):
            return(message)
    return("other")
    
    
def send_data(data_store, db_object):
    ret = db_object.insert_many(data_store)
    return(ret)
    

def process_data(data_string, uuid = UUID, header_length = 7):
    # if identified as data, convert to format for MongoDB
    # "[DATA] " has 7 characters
    data_substring = data_string[header_length:]
    data_json = json.loads(data_substring)
    
    output_json = {"Timestamp" : time.time(),
                   "SensorID" : uuid,
                   "Temperature" : data_json["temperature_c"]}
    
    return(output_json)

def delete_data(db_object, uuid = UUID):
    db_object.delete_many({"SensorID": uuid})

message_cache = []
    
with serial.Serial(ARDUINO_COM_PORT, BAUD_RATE, timeout=1) as ser:
    
    time.sleep(2)

    while(True):
        line = ser.readline()   # read a byte
        if line:
            string = line.decode()
            message_type = identify_message(string)
            
            if message_type == "data":
                data_out = process_data(string)
                message_cache.append(data_out)
                print(data_out)
            if message_type == "command":
                message_result = send_data(message_cache, temperature_db)
                message_cache = []
                print(f"[{datetime.datetime.now()}]", len(message_result.inserted_ids), "documents uploaded")

