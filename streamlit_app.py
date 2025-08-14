import streamlit as st
from query_engine import students_df, admin_context, process_query

st.title("📊 Dumroo Admin NL Query (Gemini)")

with st.expander("Example questions"):
    st.write("""
    - Which students haven’t submitted their homework yet?
    - Show me performance data for Grade 8 from 2025-08-10
    - List students with quiz scores above 80
    - Who has submitted homework in class A?
    """)

user_query = st.text_input("Ask about your students:")

if st.button("Search"):
    if user_query:
        results = process_query(user_query, students_df, admin_context)
        st.dataframe(results)
