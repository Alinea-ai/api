from pymongo import MongoClient
from pymongo.errors import ConfigurationError

def connect_to_mongodb(host="127.0.0.1", port=27017, username=None, password=None, database=None):
    """
    Connects to a MongoDB server.

    :param host: MongoDB host (default: localhost)
    :param port: MongoDB port (default: 27017)
    :param username: MongoDB username (optional)
    :param password: MongoDB password (optional)
    :param database: Default database to connect to (optional)
    :return: A MongoClient instance
    """
    try:
        if username and password:
            # Connect with authentication
            uri = f"mongodb://{username}:{password}@{host}:{port}"
        else:
            # Connect without authentication
            uri = f"mongodb://{host}:{port}"

        # Create a client instance
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)

        # Test connection
        client.server_info()  # Will raise an exception if unable to connect

        if database:
            print(f"Connected to MongoDB database: {database}")
            return client[database]  # Return the specific database
        else:
            print("Connected to MongoDB server")
            return client  # Return the client for general use
    except ConfigurationError as conf_err:
        print(f"Configuration error: {conf_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example Usage
if __name__ == "__main__":
    # Replace with your MongoDB credentials if needed
    client = connect_to_mongodb()

    # List databases
    if client:
        print("Databases available:")
        print(client.list_database_names())
