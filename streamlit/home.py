import streamlit as st
from utils import page_transition

def home_page():
    st.markdown("<h1 style='text-align: center;'>ChatDB</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Querying SQL and NoSQL Database Systems</h4>", unsafe_allow_html=True)
    st.write("")  
    st.write("")  
    st.markdown("""<p style='text-align: center; color: #7d7d7d;'>ChatDB is an innovative interactive platform designed 
                to enhance your understanding of database querying. By combining the power of natural 
                language processing with database management, ChatDB serves as your personal assistant 
                for learning SQL and NoSQL query languages.</p>""", unsafe_allow_html=True)
    st.write("")  
    st.write("")  
    st.write("")  

    col1, col2 = st.columns([1, 1])  
    with col1:
        if st.button("Choose Database", key="choose_db", on_click=page_transition, args=("page1",), disabled=st.session_state.oneclick):
            pass
    with col2:
        if st.button("Upload a Database", key="upload_db", on_click=page_transition, args=("page2",), disabled=st.session_state.oneclick):
            pass

    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;  /* Set button width to 100% */
            height: 50px;  /* Set button height */
        }
        </style>
    """, unsafe_allow_html=True)