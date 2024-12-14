import streamlit as st

# Page transition function to avoid double click
def page_transition(target_page):
    # Disable further clicks
    st.session_state.oneclick = True
    # Update the target page
    st.session_state.page = target_page
    # Re-enable the clicks
    st.session_state.oneclick = False