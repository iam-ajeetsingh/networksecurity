# code to test MongoDB connection 
# just to ensure that the connection is working properly
# and the database is accessible
# Update the password in the URI with your actual password
# and ensure that the MongoDB server is running

from dotenv import load_dotenv
import os

from pymongo.mongo_client import MongoClient

#uri = "mongodb+srv://ajeetsinghcet05:<password>@cluster0.nlmyh0x.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Reading URI as an environment variable from .env file

# 1. Load variables from .env into the environment
load_dotenv()

# 2. Fetch the URI
uri = os.getenv("MONGO_DB_URL")

# Check if the URI is set
# If not, raise an error
if not uri:
    raise RuntimeError("MONGO_DB_URL not set in environment")

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)