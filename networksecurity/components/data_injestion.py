from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity import artifact_entity

## COnfiguration of the data ingestion config
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import sys
import os
import pymongo
import pandas as pd
import numpy as np
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URI")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
           
        except Exception as e:
            raise NetworkSecurityException(f"Error connecting to MongoDB: {e}")     

    def get_collection_as_dataframe(self):
        """Fetches data from MongoDB collection and returns it as a pandas DataFrame."""
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]

            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)
            
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def initiate_data_ingestion(self):
        try:
            dataframe= self.get_collection_as_dataframe()       
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            logging.info(f"Data ingestion completed successfully. DataFrame shape: {dataframe.shape}")       
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(f"Error initiating connection to MongoDB: {e}")
        
    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        """Exports the DataFrame to a feature store file."""
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            #creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(f"Error exporting data to feature store: {e}")
        
    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        """Splits the DataFrame into training and testing sets."""
        try:
            train_set, test_set = train_test_split(
                dataframe, 
                test_size=self.data_ingestion_config.train_test_split_ratio, 
            )
            logging.info(f"Data split into train and test sets. Train shape: {train_set.shape}, Test shape: {test_set.shape}")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)   
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)

        except Exception as e:
            raise NetworkSecurityException(f"Error splitting data into train and test sets: {e}")

    