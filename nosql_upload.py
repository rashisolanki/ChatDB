import json
from pymongo import MongoClient
import xml.etree.ElementTree as ET

# # Function to load JSON data
# def load_json(file_path):
#     with open(file_path, 'r') as file:
#         data = json.load(file)
#     return list(data.values()) if isinstance(data, dict) else data

# Function to load JSON or XML data
def load_data(file_path):
    if file_path.endswith('.json'):
        return load_json(file_path)
    elif file_path.endswith('.xml'):
        return load_xml(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload a JSON (.json) or XML (.xml) file.")

# Function to load JSON data
def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Ensure data is a list of dictionaries
    if isinstance(data, dict):
        # If the data is a dictionary, convert it to a list of one dictionary
        return [data]
    elif isinstance(data, list):
        # If the data is a list, return it as is
        return data
    else:
        raise ValueError("Data must be a list of dictionaries.")

# Function to load XML data
def load_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Convert XML to list of dictionaries assuming each child element is a record
    data = []
    for child in root:
        record = {elem.tag: elem.text for elem in child}
        data.append(record)
    return data

# Function to connect to MongoDB
def connect_to_mongodb(db_name):
    client = MongoClient('mongodb://localhost:27017/')
    db = client[db_name]
    return client, db

# Function to insert data into MongoDB collection
def insert_data_to_mongodb(collection, data):
    for doc in data:
        try:
            collection.insert_one(doc)
        except Exception as e:
            # Check for BSONObjectTooLarge error
            if "BSONObjectTooLarge" in str(e):
                print("Error: Document size exceeds the 16MB BSON limit enforced by MongoDB.")
                continue  # Skip this document or handle it as needed
    print("Data upload attempt completed.")

def upload_nosql_data(json_file_path, db_name, collection_name):
    # Step 1: Load JSON data
    data = load_data(json_file_path)
    
    if not data:
        raise ValueError("Data must be a non-empty list of documents.")
    
    # Step 2: Connect to MongoDB
    client, db = connect_to_mongodb(db_name)
    collection = db[collection_name]
    
    # Step 3: Insert data into MongoDB
    insert_data_to_mongodb(collection, data)
    
    # Clean up
    client.close()
    print("NoSQL data uploaded successfully.")


# def upload_nosql_data(json_file_path, db_name, collection_name):
#     # Step 1: Load JSON data
#     data = load_data(json_file_path)
#     if not data:
#         raise ValueError("Data must be a non-empty list of documents.")
    
#     # Step 2: Connect to MongoDB
#     client, db = connect_to_mongodb(db_name)
#     collection = db[collection_name]
    
#     # Step 3: Insert data into MongoDB
#     insert_data_to_mongodb(collection, data)
    
#     # Clean up
#     client.close()
#     print("NoSQL data uploaded successfully.")

# if __name__ == "__main__":
#     json_file_path = 'US_STATE_recipes.json' 
#     try:
#         data = load_json(json_file_path)
#         if not data:
#             raise ValueError("Data must be a non-empty list of documents.")
        
#         upload_to_mongodb(data, 'chatdb', 'recipes')

#     except (FileNotFoundError, json.JSONDecodeError) as e:
#         print(f"Error: {e}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
