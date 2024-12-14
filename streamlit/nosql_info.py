import streamlit as st
from utils import page_transition
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import nosql_upload

# NoSQL Information Page
import streamlit as st
from utils import page_transition
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import nosql_upload

# NoSQL Information Page
def nosql_info_page():
    st.markdown("<h1 style='text-align: center;'>Explore MongoDB Database</h1>", unsafe_allow_html=True)
    st.write("") 
    st.write("")
    st.write("") 

    # Connect to MongoDB
    client, db = nosql_upload.connect_to_mongodb('chatdb')
    
    if db is None:
        st.error("Failed to connect to MongoDB database. Please ensure the database is configured correctly.")
        return

    # State management for showing collections and documents
    if "show_collections" not in st.session_state:
        st.session_state.show_collections = False
    if "selected_collection" not in st.session_state:
        st.session_state.selected_collection = None

    # Centered button to list all collections
    centered_col = st.columns(3)
    with centered_col[1]:  # Center the button
        if st.button("List All Collections", key="list_collections"):
            st.session_state.show_collections = True

    # If collections are to be shown
    if st.session_state.show_collections:
        try:
            collections = db.list_collection_names()
            if collections:
                st.markdown("<h4>Available Collections:</h4>", unsafe_allow_html=True)
                for collection in collections:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"- **{collection}**")  # Collection name
                    with col2:
                        if st.button(f"Show Documents", key=f"documents_{collection}"):
                            st.session_state.selected_collection = collection
            else:
                st.info("No collections found in the selected database.")

        except Exception as e:
            st.error(f"Error fetching collections: {e}")

    # If a collection is selected, show its documents
    if st.session_state.selected_collection:
        try:
            collection_name = st.session_state.selected_collection
            st.markdown(f"<h4>Documents in Collection: {collection_name}</h4>", unsafe_allow_html=True)
            collection = db[collection_name]
            documents = collection.find().limit(5)  # Limit to 5 documents for preview

            if documents:
                # Show a sample of documents (limiting to 10 for easier viewing)
                st.table([doc for doc in documents])
            else:
                st.info(f"No documents found in collection {collection_name}.")
        except Exception as e:
            st.error(f"Error fetching documents for collection {st.session_state.selected_collection}: {e}")

    st.write("") 
    st.write("") 
    st.write("") 
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Choose Database", key="back_choose_nosql", on_click=page_transition, args=("page1",)):
            st.session_state.page = "page1"  # Set to `page1` for the choose database page
    with col2:
        if st.button("Proceed to Execute Page", key="to_execute_nosql", on_click=page_transition, args=("execute_nosql",)):
            st.session_state.page = "execute_query"  # Set to the page for executing queries

    # Reset button to clear all outputs and session state
    if st.button("Reset", key="reset_nosql", on_click=reset_page_nosql):
        pass

    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;  /* Set button width to 100% */
            height: 50px;  /* Set button height */
        }
        </style>
    """, unsafe_allow_html=True)

def reset_page_nosql():
    # Reset the session state related to collections and documents
    st.session_state.show_collections = False
    st.session_state.selected_collection = None
    # Call page transition if needed to reset the view as well
    page_transition('nosql_info')
