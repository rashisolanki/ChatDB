import streamlit as sl
from nosql_nlp import translate_to_mongo  
from nosql_execute import execute_nosql_query  
from utils import page_transition  

def nl_nosql():
    # Create columns for displaying buttons side by side
    col1, col2 = sl.columns([3, 1])  # You can adjust the column widths if needed

    with col1:
        if sl.button("Back to Execute NoSQL Queries", key="execute_sql", on_click=page_transition, args=("execute_nosql",)):
            sl.session_state.page = "execute_nosql_queries_page"

    with col2:
        if sl.button("Reset Chat", key="reset_chat"):
            # Clear session state variables related to the chat
            sl.session_state.messages = []
            sl.session_state.user_prompt_history = []
            sl.session_state.chat_answers_history = []
            sl.session_state.chat_history = []
            sl.session_state.query_results = []  # Clear the stored query results
            sl.rerun()  # Rerun to clear the screen immediately

    # Page Title and Instructions
    sl.markdown("<h1 style='text-align: center;'>Natural Language Queries (NoSQL)</h1>", unsafe_allow_html=True)
    sl.markdown("<p style='text-align: center;'>Use natural language to ask questions about your NoSQL database.</p>", unsafe_allow_html=True)

    # Initialize chat history if not already in session state
    if "messages" not in sl.session_state:
        sl.session_state.messages = []

    # Display existing chat history
    for message in sl.session_state.messages:
        with sl.chat_message(message["role"]):
            sl.markdown(message["content"])

    # Manage history of user prompts and bot responses
    if "user_prompt_history" not in sl.session_state:
        sl.session_state["user_prompt_history"] = []
    if "chat_answers_history" not in sl.session_state:
        sl.session_state["chat_answers_history"] = []
    if "chat_history" not in sl.session_state:
        sl.session_state["chat_history"] = []
    if "query_results" not in sl.session_state:
        sl.session_state["query_results"] = []  # Initialize query results in session state

    # Display previous query results if any
    if sl.session_state.query_results:
        for idx, result in enumerate(sl.session_state.query_results):
            if result is not None:
                sl.write(f"Results of Query {idx + 1}:")
                if isinstance(result, list):
                    # If the result is a list, display it as a simple list
                    sl.write(result)
                elif isinstance(result, dict):
                    # If the result is a dictionary, display it as JSON
                    sl.json(result)
                else:
                    # Handle other types of results (e.g., plain text)
                    sl.write(result)

    # User input for SQL query
    query = sl.chat_input("Type your query here...")

    if query:
        # Display user input in the chat
        with sl.chat_message("user"):
            sl.markdown(query)
        
        # Append user query to session state
        sl.session_state.messages.append({"role": "user", "content": query})

        # Check if the query starts with 'SELECT'
        if query.strip().lower().startswith("db"):
            # If the query is a SELECT query, execute it directly
            output = query  # No need to translate, use the query as is

            # Display assistant's response in the chat message container
            with sl.chat_message("assistant"):
                sl.markdown(f"Executing NoSQL Query: {output}")

            # Execute the NoSQL query directly
            try:
                query_result = execute_nosql_query('chatdb', output)  # Call your function with the NoSQL query
                
                # Store the result in session state (it will persist across reruns)
                if query_result is not None:
                    sl.session_state.query_results.append(query_result)  # Store the result in session state
                    sl.write("Query executed successfully. Here are the results:")

                    # Display the result based on its type
                    if isinstance(query_result, list):
                        # If the result is a list, display it as a simple list
                        sl.write(query_result)
                    elif isinstance(query_result, dict):
                        # If the result is a dictionary, display it as JSON
                        sl.json(query_result)
                    else:
                        # Handle other types of results (e.g., plain text)
                        sl.write(query_result)
                else:
                    sl.write("No results returned from the NoSQL query.")
            
            except Exception as e:
                sl.write(f"An error occurred while executing the NoSQL query: {e}")


        else:
            # If it's not a SELECT query, translate it to SQL
            output = translate_to_mongo(query)

            # Store the output and query in session state histories
            sl.session_state["chat_answers_history"].append(output)
            sl.session_state["user_prompt_history"].append(query)
            sl.session_state["chat_history"].append((query, output))

            # Display assistant's response in the chat message container
            with sl.chat_message("assistant"):
                sl.markdown(output)  # Display the SQL query generated

            # Append assistant's response to session state
            sl.session_state.messages.append({"role": "assistant", "content": output})

            # Execute the SQL query using the translated SQL
            try:
                # Assuming execute_sql_query function returns a pandas DataFrame
                query_result = execute_nosql_query('chatdb', output)  # Call your function with the generated SQL query
                
                # Store the result in session state (it will persist across reruns)
                if query_result is not None:
                    sl.session_state.query_results.append(query_result)  # Store the result in session state
                    sl.write("Query executed successfully. Here are the results:")

                    if isinstance(query_result, list):
                        # If the result is a list, display it as a simple list
                        sl.write(query_result)
                    elif isinstance(query_result, dict):
                        # If the result is a dictionary, display it as JSON
                        sl.json(query_result)
                    else:
                        # Handle other types of results (e.g., plain text)
                        sl.write(query_result)

                else:
                    sl.write("No results returned from the NoSQL query.")
            
            except Exception as e:
                sl.write(f"An error occurred while executing the NoSQL query: {e}")
