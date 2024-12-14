import streamlit as st
from utils import page_transition

def choose():
    st.markdown("<h1 style='text-align: center;'>Choose a Database</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Please choose a database from SQL or NoSQL databases:</p>", unsafe_allow_html=True)
    st.write("")  
    st.write("") 
    st.write("") 

    # Define two buttons for selecting the database type
    col1, col2 = st.columns(2)

    # When user selects SQL
    with col1:
        if st.button("SQL", key="sql", on_click=page_transition, args=("sql_info",), disabled=st.session_state.oneclick):
            pass

    # When user selects NoSQL
    with col2:
        if st.button("NoSQL", key="nosql", on_click=page_transition, args=("nosql_info",), disabled=st.session_state.oneclick):
            pass

    # Centering the "Back to Home" button
    st.write("")  # Add some spacing
    if st.button("Back to Home", key="choose_back", on_click=page_transition, args=("home",), disabled=st.session_state.get("oneclick", False)):
        pass

    # Styling for buttons to maintain consistent format and set specific height for the "Back to Home" button
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;  /* Set button width to 100% */
            height: 50px;  /* Set button height */
        }
        </style>
    """, unsafe_allow_html=True)
