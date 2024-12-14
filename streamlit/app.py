import streamlit as st
from home import home_page
from choose_db import choose
from sql_info import sql_info_page
from nosql_info import nosql_info_page
from upload_db import upload_page
from execute_sql import execute_sql
from sample_sql import sample_sql_queries
from execute_nosql import execute_nosql
from sample_nosql import sample_nosql_queries
from nl_sql import nl_sql
from nl_nosql import nl_nosql

if "page" not in st.session_state:
    st.session_state.page = "home"
if "oneclick" not in st.session_state:
    st.session_state.oneclick = False

st.set_page_config(page_title='ChatDB', page_icon=':💬:')

def main():
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "page1":
        choose()
    elif st.session_state.page == "page2":
        upload_page()
    elif st.session_state.page == "sql_info":
        sql_info_page()
    elif st.session_state.page == "nosql_info":
        nosql_info_page()   
    elif st.session_state.page == "execute_sql":
        execute_sql()
    elif st.session_state.page == "sample_sql":
        sample_sql_queries()
    elif st.session_state.page == "nlq_sql":
        nl_sql()
    elif st.session_state.page == "execute_nosql":
        execute_nosql()
    elif st.session_state.page == "sample_nosql":
        sample_nosql_queries()
    elif st.session_state.page == "nlq_nosql":
        nl_nosql()

if __name__ == "__main__":
    main()
