from networksecurity.components.data_injestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig

if __name__ == "__main__":
    try:    
        logging.info("Starting data ingestion process...")
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(f"Data ingestion artifact: {data_ingestion_artifact}")
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        logging.info("Starting data validation process...")
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_ingestion_artifact)
        logging.info("End data validation process...")

    except Exception as e:
        raise NetworkSecurityException(f"Error initializing data ingestion config: {e}")