from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
import sys

if __name__ == "__main__":
    try:
        trauning_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(trauning_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info(f"Data Ingestion started with config: {data_ingestion_config}")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("MAIN-- Data Ingestion Completed successfully.")
        print(data_ingestion_artifact)
    
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
