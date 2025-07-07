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
      

### Step 5 : Model Training Process :
- There are following main components : 
   - Model Trainer Config (contains all File Paths, Directories and Variables)
   - Model Trainer Component
         - perform model training on multiple models.
         - Perform Hyperparameter Tunning 
         - Evaluate the performance of all the models.
         - Select the best model.
         - Log the metrices of the best model into the mLflow experiment tracking remote server on Dagshub.(for each run it adds 2 experiments:  1 for training and 1 for testing)
         - Push the model to the Local repository.
   - Final Output of Trainer compoment is : 
         - model.pkl
         - preprocessor.pkl
   - These above models pickle files are presently stored locally but they can be pushed to S3 Bucket if need be. 


### Step 6 : Creating a FastAPI application for running the Model Training Pipeline using Web App
   - creatred a training_pipeline.py to run the Data ingestion --> Data validation --> Data Transformation --> Model Training as a single pipeline.
   - added code of app.py containing the FastAPI App code to run the above training_pipeline. 
   - can run this app using commadn > uvicorn app:app --reload
   - since i have imported "from uvicorn import run as app_run" in the app.py file, i can run the app.py file just as we run a python script "python app.py ".
   - It runs successfully and now we can train our model using http://127.0.0.1:8000/train 
   


### Step 6 : Creating Batch Prediction Pipeline : 
   - It accepts a CSV file, reads it, preprocesses it using the preprocessor object, and then uses the model to predict the target variable.
   - The predicted values are added to the DataFrame and saved to a CSV file in the 'prediction_output' directory.
   - The DataFrame is then converted to an HTML table and returned as a response to be rendered in the browser.

### Step 7 : Pusing Final Model and Model Artifacts to AWS S3 Bucket:
   - Since this model.pkl file we used is very small in size, so we pushed it to github repo. but for complex models this model.pkl file gets bigger in size(in GBs). 
   - We need to push these Trained Model.pkl and other artifacts to some other storage and that is why we are using AWS S3 bucket to store them. 
   - we achieve this my syncing our local Artifacts and final_model directories to the Cloud. 
   
Note : for connecting to S3 Bucket we are not using S3fs or Boto3 libraries , instead we are using AWS CLI. we can use either one. 

   - created an IAM user testsecurity and created Access Key for CLI
   - use AWS Configure command to configure the AWS Access key using VSCode CMD : 
   - Created an S3 Bucket named 'networksecurity'
   - Model artifacts get pushed to S3 bucket on successful run of app.py file.  


### Step 8 : Creating a Docker Image and Pushing it to AWS ECR and Deploying it as a container in Amazon EC2 Instance using GitHub Actions CI/CD pipeline:
   - 1. Creating a Docker Image file
      - pulled python:3.10-slim-buster base image 
      - installed aws CLI and other requirements.txt dependencies 
      - running the command : "python app.py" to run the app.py file.

Note: Docker is case-sensitive and The Docker CLI always looks for a file named: 'Dockerfile'. i made a mistake and named it 'DockerFile' and docker could not find this file. 

   - 2. Created .github\workflows\main.yml file 
         - added code to run github action of Continuous Integration on each push of code to repo. 
         - added ignore the code commit/push to following: 
            - .github/workflows/main.yml
            - .gitignore
            - README.md
            - app.py

   - 3.  Created an AWS Private Elastic Container Registry(ECR) repository named "networksecurity".
         - build-and-push-ecr-image using Continuous Delivery
         - Install Utilities
         - Configure AWS credentials 
               - Access_Key
               - Secret Access_Key
               - AWS_Region
               - ECR_LOGIN_URI
               - ECR_REPOSITORY_NAME
            
            For this Configuring AWS Credential we need to create 5 Secrets in Github-Actions:
            To do this got to -> Github Repo Settings --> Secrets and Variables --> Actions --> Repository Secrets -> new repo secret.
         - Login to Amazon ECR 

Note : Where is the Docker Image Stored Before Being Pushed to ECR?
- Docker builds the image locally : 
   - The image is stored on the GitHub Actions runner’s local Docker daemon.
   - The GitHub runner is a temporary virtual machine (ephemeral) provided by GitHub to execute the workflow.
   - we can think of this as the image being stored on that VM’s local storage.
   - GitHub Actions runners are ephemeral. They are temporary, short-lived virtual machines that exist only for the duration of a single workflow run.
   - After the workflow finishes, the runner is shut down, and the local docker image is automatically discarded.
   - Each time your workflow starts, GitHub spins up a fresh virtual machine.
   - It downloads your repository code. It runs all the steps in your workflow.
   - When the workflow finishes (whether success or failure), the virtual machine is immediately destroyed.

    
   - 4. Deploying the Docker image to Amazon EC2 Instance:
         - Created an EC2 instance named 'Networksecurity'
         - Done the basic pre-requisite setup on EC2 instance. 
         - For basic Docker Setup In EC2 following commands to be Executed: 
             - sudo apt-get update -y   (optional)
             - sudo apt-get upgrade     (Optional)
             - # Required commands:
             - curl -fsSL https://get.docker.com -o get-docker.s   
             - sudo sh get-docker.sh
             - sudo usermod -aG docker ubuntu
             - newgrp docker

         - After running all the above command in EC2 instance,
         - Now we need to create self-hosted runner which will run my Docker image. (got to Settings--> Actions --> Runners --> add new Runner )
         -  This Runner will act as listener on github repo to listen to any chnages on the github repo. 
         - In the Process of creating the self-hosted runner i need to run the commands (in EC2 instance)  given there to Download , Configure and Run the runner. Adding a self-hosted runner requires that you download, configure, and execute the GitHub Actions Runner.  
         - enter name of runner group  - default
         - enter the name of runner - 'self-hosted'
         - rest everything is default. 
         - once you run ./run.sh you get the following terminal output: 
               ubuntu@ip-172-31-30-67:~/actions-runner$ ./run.sh 
               √ Connected to GitHub
               Current runner version: '2.325.0'
               2025-07-06 23:36:25Z: Listening for Jobs
         
         - So now the self-hosted runner is Listening for jobs 

         - on making commit to github-repo workflow runs and the self hosted runner prints: 
           - 2025-07-06 23:52:43Z: Running job: Continuous Deployment(CD) - Deploy Docker Image to Amazon EC2 instance
           - 2025-07-06 23:53:28Z: Job Continuous Deployment(CD) - Deploy Docker Image to Amazon EC2 instance completed with result: Succeeded

Note: Make sure the following things : 
   - 1. make sure the host="0.0.0.0" not "localhost"
   - 2. add the inboud rule in EC2 instance for custom TCP , Port : 8080 (as given in workflow docker file)
   - 3. make sure the action runner script is running in EC2 instance. i.e. run.sh. This script runs the self-hosted runner which listen to the deployment of image on EC2. Continuous Deployment part will run only when this runner is running on EC2 instance. 


Note : I faced error in deployment stage wherein the container was getting exited due to the authentication issue with dagshub server. it was looking for Oauth in browser but there is no way to do it in container. So fixed that part by removing the authentication line of code. 





   


