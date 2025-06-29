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


