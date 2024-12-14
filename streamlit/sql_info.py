import streamlit as st
from utils import page_transition
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sql_upload

# SQL Information Page
import streamlit as st
from utils import page_transition
import sql_upload

# SQL Information Page
def sql_info_page():
    st.markdown("<h1 style='text-align: center;'>Explore SQL Database</h1>", unsafe_allow_html=True)
    st.write("") 
    st.write("")
    st.write("") 

    # Use the connection from sql_upload
    conn = sql_upload.connect_to_mysql('localhost', 'root', 'rashi123', 'chatdb')

    if conn is None:
        st.error("Failed to connect to the SQL database. Please ensure the database is configured correctly.")
        return

    # State management for showing tables and attributes
    if "show_tables" not in st.session_state:
        st.session_state.show_tables = False
    if "selected_table" not in st.session_state:
        st.session_state.selected_table = None
    if "sample_data" not in st.session_state:
        st.session_state.sample_data = None

    # Centered button to list all tables
    centered_col = st.columns(3)
    with centered_col[1]:  # Center the button
        if st.button("List All Tables", key="list_tables"):
            st.session_state.show_tables = True

    # If tables are to be shown
    if st.session_state.show_tables:
        try:
            query = "SHOW TABLES;"  # Standard for MySQL
            cursor = conn.cursor()
            cursor.execute(query)
            tables = cursor.fetchall()
            cursor.close()

            if tables:
                st.markdown("<h4>Available Tables:</h4>", unsafe_allow_html=True)
                for table in tables:
                    col1, col2, col3 = st.columns([3, 1, 1])  # Add an extra column for the new button
                    with col1:
                        st.markdown(f"- **{table[0]}**")  # `table[0]` for the table name
                    with col2:
                        if st.button(f"Show Attributes", key=f"attributes_{table[0]}"):
                            st.session_state.selected_table = table[0]
                            st.session_state.sample_data = None  # Clear sample data when showing attributes
                    with col3:
                        if st.button(f"Show Sample Data", key=f"sample_{table[0]}"):
                            st.session_state.selected_table = table[0]
                            st.session_state.sample_data = table[0]  # Set the selected table for sample data

            else:
                st.info("No tables found in the selected database.")

        except Exception as e:
            st.error(f"Error fetching tables: {e}")

    # Only show sample data if requested
    if st.session_state.sample_data:
        try:
            sample_table_name = st.session_state.sample_data
            st.markdown(f"<h4>Sample Data from Table: {sample_table_name}</h4>", unsafe_allow_html=True)
            query = f"SELECT * FROM {sample_table_name} LIMIT 5;"
            cursor = conn.cursor()
            cursor.execute(query)
            sample_data = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]  # Get column names
            cursor.close()

            if sample_data:
                st.dataframe(
                    {column: [row[idx] for row in sample_data] for idx, column in enumerate(column_names)}
                )
            else:
                st.info(f"No data found in table {sample_table_name}.")
        except Exception as e:
            st.error(f"Error fetching sample data for table {sample_table_name}: {e}")

    # Ensure no attributes are shown if sample data is being displayed
    if st.session_state.selected_table and not st.session_state.sample_data:
        try:
            table_name = st.session_state.selected_table
            st.markdown(f"<h4>Attributes of Table: {table_name}</h4>", unsafe_allow_html=True)
            query = f"DESCRIBE {table_name};"
            cursor = conn.cursor()
            cursor.execute(query)
            attributes = cursor.fetchall()
            cursor.close()

            if attributes:
                st.table(
                    [{"Field": attr[0], "Type": attr[1], "Null": attr[2], "Key": attr[3]} for attr in attributes]
                )
            else:
                st.info(f"No attributes found for table {table_name}.")
        except Exception as e:
            st.error(f"Error fetching attributes for table {st.session_state.selected_table}: {e}")

    st.write("") 
    st.write("") 
    st.write("") 

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Choose Database", key="back_choose", on_click=page_transition, args=("page1",)):
            st.session_state.page = "page1"  # Set to `page1` for the choose database page
    with col2:
        if st.button("Proceed to Execute Page", key="to_execute", on_click=page_transition, args=("execute_sql",)):
            st.session_state.page = "execute_query"  # Set to the page for executing queries

    # Reset button to clear all outputs and session state
    if st.button("Reset", key="reset", on_click=reset_page):
        pass

    # Add button width styling for attributes and sample data buttons
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;  /* Set button width to 100% */
            height: 50px;  /* Set button height */
        }

        /* Specific buttons for show attributes and sample data */
        .stButton[data-baseweb="button"] {
            min-width: 250px;  /* Increase the width of buttons */
        }
        </style>
    """, unsafe_allow_html=True)

def reset_page():
    st.session_state.show_tables = False
    st.session_state.selected_table = None
    st.session_state.sample_data = None
    # Call page transition if needed to reset the view as well
    page_transition('sql_info')
