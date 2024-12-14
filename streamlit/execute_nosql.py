import streamlit as st
from utils import page_transition

def execute_nosql():
    st.markdown("<h1 style='text-align: center;'>Execute NoSQL Queries</h1>", unsafe_allow_html=True)
    st.write("") 
    st.write("") 
    st.write("""
    Select how you would like to proceed:
    - View and run predefined sample queries.
    - Use natural language to query the database.
    """)

    st.write("") 
    st.write("") 
    st.write("") 

    # Centered buttons for choosing query execution methods
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Show Sample Queries", key="sample_queries", on_click=page_transition, args=("sample_nosql",)):
            st.session_state.page = "sample_queries_nosql_page"  # Transition to Sample Queries Page

    with col2:
        if st.button("Ask Queries in Natural Language", key="natural_language_queries_nosql", on_click=page_transition, args=("nlq_nosql",)):
            st.session_state.page = "natural_language_nosql_page"  # Transition to Natural Language Queries Page

    # Back navigation buttons side by side
    st.write("") 
    st.write("") 
    st.write("") 
    
    back_col1, back_col2 = st.columns(2)

    with back_col1:
        if st.button("Back to NoSQL Info Page", key="back_to_nosql_info", on_click=page_transition, args=("nosql_info",)):
            st.session_state.page = "nosql_info_page"  # Navigate back to NoSQL Info Page

    with back_col2:
        if st.button("Back to Home", key="choose_back", on_click=page_transition, args=("home",), disabled=st.session_state.get("oneclick", False)):
            pass

    # Styling for buttons
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;  /* Set button width to 100% */
            height: 50px;  /* Set button height */
        }
        </style>
    """, unsafe_allow_html=True)
