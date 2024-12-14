import streamlit as st
from utils import page_transition
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from nosql_execute import execute_nosql_query  # Import for executing MongoDB queries
from nosql_sample_queries import generate_queries, generate_join_queries, query_patterns, nl_descriptions, metadata  # Import from your nosql_sample_queries

def match_query(nl_input):
    # Define some keywords for each clause
    keyword_map = {
        "find": ["find", "where", "equals", "greater than", "less than", "equal to", "not equal to"],
        "aggregate": ["aggregate", "group by", "sum", "average"],
        "count": ["count", "total", "number of", "documents", "entries"],
        "distinct": ["distinct", "unique", "different"],
        "join": ["join", "lookup", "combine", "match"],
    }

    # Check if the input matches any of the clauses
    matched_clauses = []
    for clause, keywords in keyword_map.items():
        if any(keyword in nl_input.lower() for keyword in keywords):
            matched_clauses.append(clause)

    # If no specific clause is matched, consider it a general NoSQL query
    if not matched_clauses:
        matched_clauses.append("nosql_queries")

    return matched_clauses

def sample_nosql_queries():
    st.markdown("<h1 style='text-align: center;'>Sample MongoDB Queries</h1>", unsafe_allow_html=True)
    st.write("""
    Here you can view and run predefined queries for your MongoDB database.
    """)

    # Input for chat interface
    user_input = st.text_input("Enter your NoSQL-related query in natural language:")

    if user_input:
        # Match the user's query to a MongoDB clause
        matched_clauses = match_query(user_input)

        if matched_clauses:
            # Retrieve collection metadata based on clause
            queries = []
            for clause in matched_clauses:
                if clause in ["find", "aggregate", "count", "distinct"]:
                    for collection, attributes in metadata.items():
                        queries.extend(generate_queries(clause, attributes, collection))
                elif clause == "join":
                    queries.extend(generate_join_queries())  # Use generate_join_queries for join queries

            if queries:
                st.write(f"Here are sample queries for the matched clauses: {', '.join(matched_clauses)}")
                
                for i, (description, query) in enumerate(queries, 1):
                    # print(query)
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
                                results = execute_nosql_query('chatdb', query)
                                
                                if results:
                                    # Display results in a scrollable div
                                    st.markdown(
                                        f"""
                                        <div style="height: 300px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px;">
                                            <pre>{results}</pre>
                                        </div>
                                        """, 
                                        unsafe_allow_html=True
                                    )
                                else:
                                    st.write("No results returned for this query.")

                            except Exception as e:
                                st.error(f"Error executing query: {str(e)}")
            else:
                st.write(f"No queries generated for the matched clauses: {', '.join(matched_clauses)}.")
        else:
            st.write("Sorry, we couldn't match your query to a known NoSQL clause. Please try again with more specific terms.")
    
    # Back button
    if st.button("Back to Execute NoSQL Queries", key="back_to_execute", on_click=page_transition, args=("execute_nosql",)):
        st.session_state.page = "execute_nosql_queries_page"
