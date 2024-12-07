from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, ConfigurationError
from bson.objectid import ObjectId


class DocumentService:
    VALID_DOCUMENT_TYPES = [
        'personal_info',
        'medical_info',
        'dental_questionnaire',
        'psychological_info'
    ]

    def __init__(self, connection_uri: str, database_name: str):
        """
        Initializes the DocumentService for MongoDB interactions.

        :param connection_uri: MongoDB connection URI (e.g., "mongodb://localhost:27017").
        :param database_name: Name of the database to use.
        """
        try:
            # Create a MongoClient
            self.client = MongoClient(connection_uri, serverSelectionTimeoutMS=5000)

            # Test connection
            self.client.server_info()  # Raises an exception if the connection fails

            # Access the specified database
            self.database = self.client[database_name]
            # Access the 'users' collection
            self.collection: Collection = self.database['users']

            print(f"Connected to MongoDB database: {database_name}")

        except ConnectionFailure as ce:
            print(f"Failed to connect to MongoDB: {ce}")
            raise
        except ConfigurationError as conf_err:
            print(f"Configuration error: {conf_err}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

    def find_user_by_user_id(self, user_id: int) -> dict:
        """
        Finds a single user document by user_id.

        :param user_id: The Django user.id to search for.
        :return: The user document, or None if not found.
        """
        return self.collection.find_one({"user_id": int(user_id)})

    def insert_user(self, user_data: dict) -> str:
        """
        Inserts a user document into the 'users' collection.

        :param user_data: A dictionary representing the user data.
        :return: The ID of the inserted user document.
        """
        # Ensure user_data contains 'user_id'
        if 'user_id' not in user_data:
            raise ValueError("user_data must include 'user_id' field.")

        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)

    def update_user(self, user_id, update_data):
        """
        Updates a user document in MongoDB.

        :param user_id: The ID of the user document to update.
        :param update_data: A dictionary containing the fields to update.
        :return: The number of modified documents (0 if no update was made).
        """
        result = self.collection.update_one(
            {"_id": ObjectId(user_id)},  # Convert to ObjectId if necessary
            {"$set": update_data}  # Update the specified fields
        )
        print("Matched count:", result.matched_count)  # Debugging
        print("Modified count:", result.modified_count)  # Debugging
        return result.modified_count

    def find_users(self, query: dict, limit: int = 0) -> list:
        """
        Finds users based on a query.

        :param query: A dictionary representing the query filter.
        :param limit: The maximum number of users to return (0 for no limit).
        :return: A list of matching user documents.
        """
        cursor = self.collection.find(query).limit(limit)
        return list(cursor)

    def delete_user(self, user_id: int) -> int:
        """
        Deletes a user document.

        :param user_id: The Django user.id of the user to delete.
        :return: The number of documents deleted.
        """
        result = self.collection.delete_one({"user_id": user_id})
        return result.deleted_count
