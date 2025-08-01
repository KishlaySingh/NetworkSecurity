from networksecurity.components.data_injestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig

if __name__ == "__main__":
    try:    
        logging.info("Starting data ingestion process...")
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(f"Data ingestion artifact: {data_ingestion_artifact}")
        
    except Exception as e:
        raise NetworkSecurityException(f"Error initializing data ingestion config: {e}")