## Network Security Project for Phishing Data 

### Step 1 : ETL Pipeline Setup:
- Extracted data from CSV file. 
- Transformed the csv data into JSON format
- Load the json data into MongoDB Database. 

### Step 2 : Data Ingestion Process : 
- There are 3 main components : 
   - Data Ingestion Config (contains all File Paths, Directories and Variables)
   - Data Ingestion Component
   - Data Ingestion Artifacts ()

    Data Ingestion Component does following steps: 
    1. Reading Data from MongoDB
    2. Creating a Feature Store to store the the retrieved data
    3. Spliting data into Train and Test 
    4. Saving the Training and Test Data in Ingested Folder as train.csv and test.csv files.
    5. 
#### MongoDB Atlas UI showing the Collection Name : Network_Data and DataBase Name : AJEET_DB 
![image](https://github.com/user-attachments/assets/9b5c5c64-dde2-4193-9ddc-1e058d8e7ea0)

#### Directory Structure after Data Ingestion Process Showing Data Ingestion Artifacts and Logs Directories:

![image](https://github.com/user-attachments/assets/e9fb3ecc-50da-48bd-824b-12655ea44ce8)

#### Log File Content: 
![image](https://github.com/user-attachments/assets/c82928e0-31df-4e86-b25c-f565107a0517)


### Step 3 : Data Validation Process :

   1. Checking for same schema in the new data:
      - same no. of columns/ features 
      - same datatypes for each column/feature
   2. Checking for Data Drift in new data: 
      - checking weather the distribution of data is same as that of training data. or did it change for new data?
   3. Validate no. of Columns, Numerical Columns Exist or not in the new data?
   
   4. Creating Data Validation Report.
#### Data Validation Workflow is as follows: 
![image](https://github.com/user-attachments/assets/b5ac7e59-0748-4a83-b7fa-1ef68ba5c56c)

#### Data Validation Log File : 
![image](https://github.com/user-attachments/assets/6cd09281-9402-4dc8-b73e-585aac6c9327)

#### Data Ingestion and Data Validation Artifacts : 
![image](https://github.com/user-attachments/assets/21fddb2d-e3bc-44aa-8c99-a34af874ce76)  

### Step 4 : Data Transformation Process :
- There are following main components : 
   - Data Transformation Config (contains all File Paths, Directories and Variables)
   - Data Transforamtion Component
   - Reading Data from Data Validation Artifacts (train.csv and test.csv)
   - Data Transformation Step 
      - Dividing Dependent and Independent Features from Train data
      - Imputing Null/ NaN values using KNN imputer
      - Handling Missing Values 
      - using Feature Engineering Technique-SMOTETomek to handle Data Imbalance. 

   - Data Transformation Artifacts Creation. (train.npy and test.npy)

   Note: (In Feature Engineering : For train data we use fit.transform() and for test data we use only transform() to avoid any Data leakage)

![image](https://github.com/user-attachments/assets/19b2f01b-d4de-4a79-9d2c-92f850ae7154)
![image](https://github.com/user-attachments/assets/d2273a4a-790d-43f8-afd7-a931f11d4508)
      



