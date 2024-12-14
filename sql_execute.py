from sql_upload import connect_to_mysql 
import pandas as pd
from tabulate import tabulate 

# Function to execute a SQL query and print the result
def execute_sql_query(query, host='localhost', user='root', password='rashi123', database='chatdb'):
   # Step 1: Connect to MySQL database
    connection = connect_to_mysql(host, user, password, database)
    cursor = connection.cursor()

   # Step 2: Execute the query
    cursor.execute(query)

    # Step 3: Fetch all rows and column names
    rows = cursor.fetchall()
    columns = [i[0] for i in cursor.description]  # Get column names
    
    # Step 4: Use Pandas DataFrame to print the result in a table format
    df = pd.DataFrame(rows, columns=columns)
    
    # Step 5: Print the DataFrame with borders using tabulate
   #  print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))  # Use 'grid' format for borders
   
    # Clean up
    cursor.close()
    connection.close()

    return df
