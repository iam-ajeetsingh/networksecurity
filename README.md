## Network Security Project for Phishing Data 

### Step 1 : ETL Pipeline Setup:
- Extracted data from CSV file. 
- Transformed the csv data into JSON format
- Load the json data into MongoDB Database. 

### Data Ingestion Process : 
- There are 3 main components : 
   - Data Ingestion Config (contains all File Paths, Directories and Variables)
   - Data Ingestion Component
   - Data Ingestion Artifacts ()

    Data Ingestion Component does following steps: 
    1. Reading Data from MongoDB
    2. Creating a Feature Store to store the the retrieved data
    3. Spliting data into Train and Test 
    4. Saving the Training and Test Data in Ingested Folder as train.csv and test.csv files. 


