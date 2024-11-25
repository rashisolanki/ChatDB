import mysql.connector
import pandas as pd

# Function to read Excel or CSV file
def read_file(file_path):
    if file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    elif file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload an Excel (.xlsx) or CSV (.csv) file.")


# Function to connect to MySQL
def connect_to_mysql(host, user, password, database):
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

# Function to create a table based on DataFrame structure
def create_table(cursor, table_name, df):
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    for column in df.columns:
        if pd.api.types.is_integer_dtype(df[column]):
            create_table_query += f"{column} INT,"
        elif pd.api.types.is_float_dtype(df[column]):
            create_table_query += f"{column} FLOAT,"
        else:
            create_table_query += f"{column} VARCHAR(255),"  # Default to VARCHAR
    create_table_query = create_table_query.rstrip(',') + ");"
    cursor.execute(create_table_query)

# Function to insert data into MySQL table

def insert_data(cursor, table_name, df):
    # Replace NaN values with None to ensure MySQL interprets them as NULL
    df = df.where(pd.notnull(df), None)

    for _, row in df.iterrows():
        # Ensure all columns in the DataFrame are accounted for in the SQL query
        sql = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join(['%s'] * len(row))})"
        
        # Convert row values to tuple and handle any remaining NaNs
        values = tuple(row.replace({pd.NA: None, float('nan'): None, 'nan': None}))
        
        try:
            cursor.execute(sql, values)
        except mysql.connector.errors.ProgrammingError as e:
            print("Error inserting row:", values)
            print("SQL error:", e)
            raise

def upload_sql_data(excel_file_path, table_name, host, user, password, database):
    # Step 1: Read the Excel file into a DataFrame
    df = read_file(excel_file_path)
    print("Excel/csv file read successfully.")

    # Step 2: Connect to MySQL database
    connection = connect_to_mysql(host, user, password, database)
    print("Connected to the database successfully.")
    
    cursor = connection.cursor()

    # Step 3: Create the table
    create_table(cursor, table_name, df)
    connection.commit()
    print("Table created successfully.")

    # Step 4: Insert data into MySQL table
    insert_data(cursor, table_name, df)
    connection.commit()
    print("Data uploaded successfully!")

    # Step 5: Clean up
    cursor.close()
    connection.close()
    print("Database connection closed.")
    
# # If this script is run directly
# if __name__ == "__main__":
#     # Step 1: Read the Excel file into a DataFrame
#     excel_file_path = 'Coffee Shop Sales.xlsx'  # Update the path to your Excel file
#     df = read_excel_file(excel_file_path)
#     print("Excel file read successfully.")

#     # Step 2: Connect to MySQL database
#     connection = connect_to_mysql('localhost', 'root', 'rashi123', 'chatdb')
#     print("Connected to the database successfully.")
    
#     cursor = connection.cursor()

#     # Step 3: Create the table
#     create_table(cursor, 'coffeeshop', df)
#     connection.commit()
#     print("Table created successfully.")

#     # Step 4: Insert data into MySQL table
#     insert_data(cursor, 'coffeeshop', df)
#     connection.commit()
#     print("Data uploaded successfully!")

#     # Step 5: Clean up
#     cursor.close()
#     connection.close()
#     print("Database connection closed.")


# def upload_sql_data(file_path, table_name, host, user, password, database):
#     try:
#         # Step 1: Read the file into a DataFrame
#         df = read_file(file_path)
#         success_msg = "File read successfully."

#         # Step 2: Connect to MySQL database
#         connection = connect_to_mysql(host, user, password, database)
#         success_msg += "\nConnected to the database successfully."
        
#         cursor = connection.cursor()

#         # Step 3: Create the table
#         create_table(cursor, table_name, df)
#         connection.commit()
#         success_msg += "\nTable created successfully."

#         # Step 4: Insert data into MySQL table
#         insert_data(cursor, table_name, df)
#         connection.commit()  # Ensure data is saved
#         success_msg += "\nData uploaded successfully!"

#         return success_msg  # Return the success message

#     except Exception as e:
#         error_msg = f"Failed to upload data: {str(e)}"
#         return error_msg  # Return the error message

#     finally:
#         # Step 5: Clean up
#         if 'cursor' in locals():
#             cursor.close()
#         if 'connection' in locals():
#             connection.close()
#         print("Database connection closed.")