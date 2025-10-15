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
    DB_NAME = "data"

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
        # Check if database exists
        if DB_NAME in client.list_database_names():
            print(f"Database '{DB_NAME}' already exists. Skipping creation.")
            db = client[DB_NAME]
        else:
            print(f"Database '{DB_NAME}' not found. Creating now.")
            db = client[DB_NAME]
            # You can perform initial setup for a new DB here if needed
            print(f"Database '{DB_NAME}' created.")

        # --- Create 'users' collection and indexes ---
        if "users" not in db.list_collection_names():
            try:
                db.create_collection("users")
                print("Collection 'users' created.")
                users_collection = db["users"]
                users_collection.create_index([("username", ASCENDING)], unique=True, name="idx_username_unique")
                users_collection.create_index([("email", ASCENDING)], unique=True, name="idx_email_unique")
                print("Indexes created for 'users' collection on username and email.")
            except CollectionInvalid:
                # This is a fallback, though the 'if' should prevent it
                print("Collection 'users' already exists.")
        else:
            print("Collection 'users' already exists. Ensuring indexes.")
            users_collection = db["users"]
            users_collection.create_index([("username", ASCENDING)], unique=True, name="idx_username_unique")
            users_collection.create_index([("email", ASCENDING)], unique=True, name="idx_email_unique")
            print("Indexes ensured for 'users' collection on username and email.")


        # --- Create 'problems' collection and indexes ---
        if "problems" not in db.list_collection_names():
            try:
                db.create_collection("problems")
                print("Collection 'problems' created.")
                problems_collection = db["problems"]
                problems_collection.create_index([("difficulty", ASCENDING)], name="idx_difficulty")
                problems_collection.create_index([("tags", ASCENDING)], name="idx_tags")
                print("Indexes created for 'problems' collection.")
            except CollectionInvalid:
                print("Collection 'problems' already exists.")
        else:
            print("Collection 'problems' already exists. Ensuring indexes.")
            problems_collection = db["problems"]
            problems_collection.create_index([("difficulty", ASCENDING)], name="idx_difficulty")
            problems_collection.create_index([("tags", ASCENDING)], name="idx_tags")
            print("Indexes ensured for 'problems' collection.")


        # --- Create 'submissions' collection and indexes ---
        if "submissions" not in db.list_collection_names():
            try:
                db.create_collection("submissions")
                print("Collection 'submissions' created.")
                submissions_collection = db["submissions"]
                submissions_collection.create_index([("username", ASCENDING)], name="idx_username")
                submissions_collection.create_index([("problem_id", ASCENDING)], name="idx_problem_id")
                submissions_collection.create_index([("verdict", ASCENDING)], name="idx_verdict")
                submissions_collection.create_index([("username", ASCENDING), ("problem_id", ASCENDING)], name="idx_user_problem")
                submissions_collection.create_index([("username", ASCENDING), ("verdict", ASCENDING)], name="idx_user_verdict")
                submissions_collection.create_index([("problem_id", ASCENDING), ("verdict", ASCENDING)], name="idx_problem_verdict")
                print("Indexes created for 'submissions' collection.")
            except CollectionInvalid:
                print("Collection 'submissions' already exists.")
        else:
            print("Collection 'submissions' already exists. Ensuring indexes.")
            submissions_collection = db["submissions"]
            submissions_collection.create_index([("username", ASCENDING)], name="idx_username")
            submissions_collection.create_index([("problem_id", ASCENDING)], name="idx_problem_id")
            submissions_collection.create_index([("verdict", ASCENDING)], name="idx_verdict")
            submissions_collection.create_index([("username", ASCENDING), ("problem_id", ASCENDING)], name="idx_user_problem")
            submissions_collection.create_index([("username", ASCENDING), ("verdict", ASCENDING)], name="idx_user_verdict")
            submissions_collection.create_index([("problem_id", ASCENDING), ("verdict", ASCENDING)], name="idx_problem_verdict")
            print("Indexes ensured for 'submissions' collection.")

        print("\nDatabase initialization check complete!")

    except Exception as e:
        print(f"An error occurred during database initialization: {e}")

    finally:
        if client:
            client.close()
            print("MongoDB connection closed.")

if __name__ == "__main__":
    main()