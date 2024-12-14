import streamlit as st
from utils import page_transition
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sql_execute import execute_sql_query
from sql_sample_queries import generate_queries, query_patterns, nl_descriptions, metadata  # Import from your sample_sql_queries

def match_query(nl_input):
    # Define some keywords for each clause
    keyword_map = {
        "group_by": ["total", "average", "sum", "count", "group by"],
        "order_by": ["order by", "ascending", "descending", "sorted"],
        "having": ["having", "greater than", "less than", "threshold"],
        "join": ["join", "on", "combine"],
        "aggregation": ["sum", "average", "count", "aggregate"],
    }

    # Check if the input matches any of the clauses
    matched_clauses = []
    for clause, keywords in keyword_map.items():
        if any(keyword in nl_input.lower() for keyword in keywords):
            matched_clauses.append(clause)

    # If no specific clause is matched, consider it a general SQL query
    if not matched_clauses:
        matched_clauses.append("sql_queries")

    return matched_clauses

def sample_sql_queries():
    st.markdown("<h1 style='text-align: center;'>Sample Queries</h1>", unsafe_allow_html=True)
    st.write("""
    Here you can view and run predefined queries for your SQL database.
    """)

    # Input for chat interface
    user_input = st.text_input("Enter your SQL-related query in natural language:")

    if user_input:
        # Match the user's query to a SQL clause
        matched_clauses = match_query(user_input)

        if matched_clauses:
            # Retrieve table metadata based on clause
            queries = []
            for clause in matched_clauses:
                if clause in ["group_by", "order_by", "having", "aggregation"]:
                    for table, attributes in metadata.items():
                        queries.extend(generate_queries(clause, attributes, table))
                elif clause == "join":
                    queries.extend(generate_queries(clause, attributes=None))
                elif clause == "sql_queries":
                    for table, attributes in metadata.items():
                        queries.extend(generate_queries(clause, attributes, table))

            if queries:
                st.write(f"Here are sample queries for the matched clauses: {', '.join(matched_clauses)}")
                
                for i, (query, description) in enumerate(queries, 1):
                    query_key = f"query_{i}"  # Unique key for each query
                    col1, col2 = st.columns([3, 1])  # Create two columns: one for the query and description, one for the button
                    
                    with col1:
                        st.write(f"{i}. {query}")
                        st.write(f"Description: {description}")
                    
                    with col2:
                        # Add a button to execute the query
                        if st.button("Execute", key=f"execute_{i}"):
                            try:
                                # Execute the query
                                results = execute_sql_query(query)
                                
                                if not results.empty:
                                    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
                                    st.write("Execution Results:")
                                    st.dataframe(results)  
                                    st.markdown("</div>", unsafe_allow_html=True)
                                else:
                                    st.write("No results returned for this query.")

                            except Exception as e:
                                st.error(f"Error executing query: {str(e)}")
            else:
                st.write(f"No queries generated for the matched clauses: {', '.join(matched_clauses)}.")
        else:
            st.write("Sorry, we couldn't match your query to a known SQL clause. Please try again with more specific terms.")
    
    # Back button
    if st.button("Back to Execute SQL Queries", key="back_to_execute", on_click=page_transition, args=("execute_sql",)):
        st.session_state.page = "execute_sql_queries_page"
