import sys
import json
import sql_upload
import nosql_upload
from sql_execute import execute_sql_query
# from sql_nlp import interpret_nl_query
from nosql_execute import execute_nosql_query

def upload_data():
    # Ask user to specify SQL or NoSQL
    data_type = input("Would you like to upload to SQL or NoSQL? ").lower()

    if data_type == "sql":
        excel_file_path = input("Enter the Excel file path: ")
        table_name = input("Enter the SQL table name: ")
        sql_upload.upload_sql_data(excel_file_path, table_name, 'localhost', 'root', 'rashi123', 'chatdb')

    elif data_type == "nosql":
        json_file_path = input("Enter the JSON file path: ")
        collection_name = input("Enter the NoSQL collection name: ")
        nosql_upload.upload_nosql_data(json_file_path, 'chatdb', collection_name)

    else:
        print("Invalid input. Please choose either 'sql' or 'nosql'.")

def execute_query():
    # Ask user to specify SQL or NoSQL
    query_type = input("Would you like to execute an SQL or NoSQL query? ").lower()

    if query_type == "sql":
        # nlp_mode = input("Would you like to enter a natural language query? (yes/no): ").lower()
        query = input("Enter your SQL query: ")
        execute_sql_query(query, 'localhost', 'root', 'rashi123', 'chatdb')

        # if nlp_mode == "yes":
        #     nl_query = input("Enter your natural language query: ")
        #     table_name = input("Enter the SQL table name: ")
        #     # Generate SQL from NLP query
        #     sql_query = interpret_nl_query(nl_query, table_name)
        #     print("Interpreted SQL query:", sql_query)
        #     execute_sql_query(sql_query, 'localhost', 'root', 'rashi123', 'chatdb')    

    #     else:
    #         query = input("Enter your SQL query: ")
    #         execute_sql_query(query, 'localhost', 'root', 'rashi123', 'chatdb')

    elif query_type == "nosql":
        query_input = input("Enter your MongoDB query: ")
        # query_dict = json.loads(query_input)  # Load the input as a JSON-like dictionary
        execute_nosql_query('chatdb', query_input)

    else:
        print("Invalid input. Please choose either 'sql' or 'nosql'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please specify either 'upload' or 'execute' as the first argument.")
        sys.exit(1)

    operation = sys.argv[1].lower()

    if operation == "upload":
        upload_data()

    elif operation == "execute":
        execute_query()

    else:
        print("Invalid option. Please choose 'upload' or 'execute'.")
        sys.exit(1)


# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Please specify either 'sql' or 'nosql' as the first argument.")
#         sys.exit(1)

#     # Choose SQL or NoSQL based on the first argument
#     data_type = sys.argv[1].lower()

#     if data_type == "sql":
#         # Example usage: python main.py sql 'Coffee Shop Sales.xlsx' 'coffeeshop'
#         if len(sys.argv) != 4:
#             print("Usage for SQL: python main.py sql <excel_file_path> <table_name>")
#             sys.exit(1)

#         excel_file_path = sys.argv[2]
#         table_name = sys.argv[3]
#         upload_sql_data(excel_file_path, table_name, 'localhost', 'root', 'rashi123', 'chatdb')

#     elif data_type == "nosql":
#         # Example usage: python main.py nosql 'US_STATE_recipes.json' 'chatdb' 'recipes'
#         if len(sys.argv) != 4:
#             print("Usage for NoSQL: python main.py nosql <json_file_path> <collection_name>")
#             sys.exit(1)

#         json_file_path = sys.argv[2]
#         db_name = 'chatdb'
#         collection_name = sys.argv[3]
#         upload_nosql_data(json_file_path, db_name, collection_name)

#     else:
#         print("Invalid option. Please choose 'sql' or 'nosql'.")
#         sys.exit(1)
