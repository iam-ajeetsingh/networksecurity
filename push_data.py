import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca = certifi.where()
# this certifi package is used to provide Mozilla's CA Bundle
# which is used to verify the SSL certificates of the MongoDB server
# Why this is needed?
# Because the MongoDB server uses SSL/TLS to encrypt the connection
# and the certifi package provides the CA Bundle to verify the SSL certificates
# so that the connection is secure and trusted

import pandas as pd
import numpy as np
import pymongo

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json(self, csv_file_path):
        try: 
            data = pd.read_csv(csv_file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    # why csv to json?
    # because MongoDB stores data in JSON format
    # so we need to convert the CSV data to JSON format
    # and then insert it into the MongoDB database        


    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            # Create a new client and connect to the server
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]

            # Create a new collection
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)  # Insert the records into the collection
            # Note: The insert_many method is used to insert multiple records at once
            # If you want to insert a single record, you can use the insert_one method
            return(len(self.records))  # Return the number of records inserted
                   
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        

if __name__ == "__main__":
    FILE_PATH = "Network_Data\phishingData.csv"
    DATABASE = "AJEET_DB"
    Collection = "Network_Data"
    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json(csv_file_path = FILE_PATH)
    print(records)
    no_of_records = networkobj.insert_data_mongodb(records,DATABASE, Collection)
    print(no_of_records, "records inserted into the MongoDB database")

