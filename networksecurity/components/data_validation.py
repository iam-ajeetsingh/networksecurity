from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH

# scipy is used for statistical tests in general.
# we used it for data drift detection
from scipy.stats import ks_2samp  
# ks_2samp uses 2 samples to perform the Kolmogorov-Smirnov test
# to find the drift in the data.
import pandas as pd
import os, sys

from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def validate_no_of_columns(self, df: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config['columns'])
            logging.info(f"Expected number of columns: {number_of_columns}")
            logging.info(f"Actual number of columns: {len(df.columns)}")
            if len(df.columns) == number_of_columns:
                logging.info("Number of columns validation passed")
                return True
            else:
                logging.error("Number of columns validation failed")
                return False
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e


    def detect_data_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column] # we are comparing the same column from both dataframes
                is_same_dist=ks_2samp(d1,d2) # Kolmogorov-Smirnov test
                if threshold<=is_same_dist.pvalue:  # if p-value is >= threshold, we assume the distributions are similar and no drift is detected
                    is_found=False   
                else:
                    is_found=True   # if p-value is < threshold, we assume the distributions are different and drift is detected
                    status=False

                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                    
                    }})
                
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            #Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        


    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info("Initiating data validation")

            #train_file_path=self.data_ingestion_artifact.training_file_path
            #test_file_path=self.data_ingestion_artifact.testing_file_path

            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            ## read the data from the train and test file
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            ## Validate the number of columns in both train and test dataframes
            is_train_valid = self.validate_no_of_columns(train_df)
            is_test_valid = self.validate_no_of_columns(test_df)

            if not is_train_valid: 
                error_message = f"Train data validation failed: Expected {len(self._schema_config)} columns, but got {len(train_df.columns)}"

            if not is_test_valid: 
                error_message = f"Test data validation failed: Expected {len(self._schema_config)} columns, but got {len(test_df.columns)}"

            ## lets check the datadrift
            drift_status= self.detect_data_drift(base_df=train_df, current_df=test_df)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)

            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

            data_validation_artifact = DataValidationArtifact(
                validation_status=drift_status,
                #valid_train_file_path=self.data_ingestion_artifact.training_file_path,
                #valid_test_file_path=self.data_ingestion_artifact.testing_file_path,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )



            logging.info("Data validation completed successfully")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e 
