import os
import time
from pymongo import MongoClient, ASCENDING
from pymongo.errors import CollectionInvalid, ConnectionFailure
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    MONGO_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
    MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
    MONGO_HOST = "mongodb" # Connect to the service name in Docker Compose
    MONGO_PORT = 27017
    DB_NAME = "annaforces_db"

    # Retry connection logic
    max_retries = 5
    retry_delay = 10 # seconds
    client = None

    for attempt in range(max_retries):
        try:
            # Connect to MongoDB
            client = MongoClient(
                host=MONGO_HOST,
                port=MONGO_PORT,
                username=MONGO_USERNAME,
                password=MONGO_PASSWORD,
                authSource='admin',
                serverSelectionTimeoutMS=5000 # Timeout after 5 seconds
            )
            client.admin.command('ping')
            print("MongoDB connection successful.")
            break # Exit loop on successful connection
        except ConnectionFailure as e:
            print(f"Connection failed (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    else: # This else belongs to the for loop, runs if the loop completes without break
        print("Could not connect to MongoDB after several attempts. Exiting.")
        return # Exit the script if connection fails

    try:
        db = client[DB_NAME]

        # --- Create 'users' collection and indexes ---
        try:
            db.create_collection("users")
            print("Collection 'users' created.")
        except CollectionInvalid:
            print("Collection 'users' already exists.")
        
        users_collection = db["users"]
        users_collection.create_index([("username", ASCENDING)], unique=True, name="idx_username_unique")
        users_collection.create_index([("email", ASCENDING)], unique=True, name="idx_email_unique")
        print("Indexes created/ensured for 'users' collection.")

        # --- Create 'problems' collection and indexes ---
        try:
            db.create_collection("problems")
            print("Collection 'problems' created.")
        except CollectionInvalid:
            print("Collection 'problems' already exists.")

        problems_collection = db["problems"]
        problems_collection.create_index([("difficulty", ASCENDING)], name="idx_difficulty")
        problems_collection.create_index([("tags", ASCENDING)], name="idx_tags")
        print("Indexes created/ensured for 'problems' collection.")

        print("\nDatabase initialization complete!")

    except Exception as e:
        print(f"An error occurred during database initialization: {e}")

    finally:
        if client:
            client.close()
            print("MongoDB connection closed.")

if __name__ == "__main__":
    main()