from pymongo import MongoClient
import json
from tabulate import tabulate
from nosql_upload import connect_to_mongodb 
from pprint import pprint
import sys
import re

# Define function for each query type
def handle_find(collection, params, extra_condition):
    filter_ = eval(params) if params.strip() else {}
    query = collection.find(filter_)
    if extra_condition:
        query = eval(f"query.{extra_condition}")
    
    result = list(query)
    return result

def handle_aggregate(collection, params):
    pipeline = eval(params)
    result = list(collection.aggregate(pipeline))
    return result

def handle_count(collection, params):
    filter = eval(params) if params.strip() else {}
    result = collection.count_documents(filter)
    return result

def handle_distinct(collection, params):
    key = params.strip('"').strip("'") 
    result = collection.distinct(key)
    return result
  
# Function to execute NoSQL queries
def execute_nosql_query(db_name, query):
    # Step 1: Connect to MongoDB
    client, db = connect_to_mongodb(db_name)

    # all_collections = db.list_collection_names()
    # print("\nAll Collections: ", all_collections)

    # Extract collection name and query type
    collection_name = query.split('.')[1].split('(')[0]
    # print("\nCollection: ", collection_name)

    query_type = query.split('.')[2].split('(')[0]
    # print("Query Type: ", query_type)

    # Extract query parameters (if any) from within parentheses
    params_start = query.find('(') + 1
    params_end = query.find(')', params_start)
    params = query[params_start:params_end]
    # print("Params: ", params)
    
    # Extract extra condition after parentheses
    extra_condition = query[query.find(').') + 2:] if ').' in query else ""
    # print("Extra Condition: ", extra_condition)

    # Reference collection
    collection = db[collection_name]

    # Execute based on query type
    if query_type == "find":
        result = handle_find(collection, params, extra_condition)
        # print("\nResult: ")
        # pprint(result)
        return result

    elif query_type == "aggregate":
        result = handle_aggregate(collection, params)
        # print("\nResult: ")
        # pprint(result)
        return result

    elif query_type == "count":
        result = handle_count(collection, params)
        # print("\nResult: ")
        # pprint(result)
        return result

    elif query_type == "distinct":
        result = handle_distinct(collection, params)
        # print("\nResult: ")
        # pprint(result)
        return result

    else:
        # print(f"Unsupported query type: {query_type}")
        return f"Unsupported query type: {query_type}"

    # Clean up
    client.close()
