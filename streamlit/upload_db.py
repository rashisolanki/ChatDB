import streamlit as st
from utils import page_transition
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sql_upload
import nosql_upload

def upload_page():
    st.title("Upload Database")
    st.write("Choose your preferred database type and upload your file.")

    # Database type selection
    db_type = st.selectbox("Would you like to upload to SQL or NoSQL?", ["Select", "SQL", "NoSQL"])

    if db_type == "SQL":
        # Upload file and specify table name
        excel_file = st.file_uploader("Upload Excel or CSV file for SQL:", type=["xlsx", "csv"])
        table_name = st.text_input("Enter the SQL table name:")

        # Upload button logic
        if excel_file and table_name and st.button("Upload to SQL"):
            # Save the uploaded file temporarily
            temp_file_path = "temp_uploaded_file." + ("xlsx" if excel_file.name.endswith("xlsx") else "csv")
            with open(temp_file_path, "wb") as f:
                f.write(excel_file.getbuffer())

            try:
                # Upload data to SQL
                sql_upload.upload_sql_data(temp_file_path, table_name, 'localhost', 'root', 'rashi123', 'chatdb')
                st.success(f"Data uploaded successfully to SQL table '{table_name}'!")
                st.session_state.db_name = table_name  # Save table name for later use
                st.session_state.db_type = "SQL"  # Save the selected DB type

            except Exception as e:
                st.error(f"Failed to upload data to SQL: {e}")

    elif db_type == "NoSQL":
        # Upload file and specify collection name
        json_file = st.file_uploader("Upload JSON or XML file for NoSQL:", type=["json", "xml"])
        collection_name = st.text_input("Enter the NoSQL collection name:")

        # Upload button logic
        if json_file and collection_name and st.button("Upload to NoSQL"):
            # Save the uploaded file temporarily
            temp_file_path = "temp_uploaded_file." + ("json" if json_file.name.endswith("json") else "xml")
            with open(temp_file_path, "wb") as f:
                f.write(json_file.getbuffer())

            try:
                # Upload data to NoSQL
                nosql_upload.upload_nosql_data(temp_file_path, 'chatdb', collection_name)
                st.success(f"Data uploaded successfully to NoSQL collection '{collection_name}'!")
                st.session_state.collection_name = collection_name  # Save collection name for later use
                st.session_state.db_type = "NoSQL"  # Save the selected DB type

            except Exception as e:
                st.error(f"Failed to upload data to NoSQL: {e}")

    elif db_type == "Select":
        st.info("Please select a database type to proceed.")

    else:
        st.warning("Invalid selection. Please choose 'SQL' or 'NoSQL'.")
    
    # Navigation buttons
    col1, col2 = st.columns([1, 3])  

    with col1:
        if st.button("Back to Home", key="upload_back", on_click=page_transition, args=("home",)):
            pass

    with col2:
        # Ensure button action based on DB type
        if db_type == "SQL" and st.session_state.get("db_type") == "SQL":
            # For SQL, add the page transition logic for the Explore Database button
            if st.button("Query Database", key="upload_execute", on_click=page_transition, args=("nlq_sql",)):
                pass
        elif db_type == "NoSQL" and st.session_state.get("db_type") == "NoSQL":
            # For NoSQL, add the page transition logic for the Explore Database button
            if st.button("Query Database", key="upload_execute", on_click=page_transition, args=("nlq_nosql",)):
                pass
    
    # Styling for buttons
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;  /* Set button width to 100% */
            height: 50px;  /* Set button height */
        }
        .stButton>button:nth-of-type(3) {
            background-color: red;  /* Change background color to red for the Upload button */
            color: white;  /* Change text color to white */
        }
        </style>
    """, unsafe_allow_html=True)

    # Display the uploaded database name
    if "db_name" in st.session_state:
        st.markdown(f"<p style='text-align: center;'>Currently working with database: <strong>{st.session_state.db_name}</strong></p>", unsafe_allow_html=True)
