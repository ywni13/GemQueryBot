from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3  # For SQLite database interaction
import google.generativeai as genai
import pandas as pd  # For tabular data display

# Load environment variables
load_dotenv()

# Configure the Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("Google API Key not found. Please set it in the environment variables.")

# Function to fetch a SQL query from Gemini AI
def get_gemini_response(question):
    """
    Fetches a SQL query based on the question provided using Gemini AI.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(question)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error fetching response from Gemini: {e}")
        return None

# Function to execute a SQL query and fetch results
def execute_sql_query(sql, db):
    """
    Executes the given SQL query on the specified SQLite database.
    Returns the fetched results or an error message.
    """
    try:
        if not sql.lower().startswith(("select", "insert", "update", "delete")):
            st.error("The response contains invalid SQL. Please ensure a valid SQL query is generated.")
            return None

        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        st.error(f"Error executing SQL query: {e}")
        return None

# Prompt for Gemini AI
prompt = """
You are an expert in converting English questions to SQL queries.
The database is named 'STUDENT' and has the following columns: NAME, CLASS, SECTION, MARKS.
Please generate only SQL queries without any other code or explanation.

Examples:
1. How many records are present?
   SELECT COUNT(*) FROM STUDENT;

2. List all students in class 'Data Science'.
   SELECT * FROM STUDENT WHERE CLASS = 'Data Science';

Respond with only the SQL query and nothing else.
"""

# Initialize Streamlit app
st.set_page_config(page_title="SQL Query Generator")
st.header("SQL Query Generator and Result Viewer")

# Input field for user question
user_input = st.text_input("Enter your question:")

if st.button("Generate and Execute Query"):
    if not user_input.strip():
        st.error("Please enter a valid question.")
    else:
        # Generate the SQL query
        question = prompt + f"\n\nQuestion: {user_input}"
        generated_query = get_gemini_response(question)

        if generated_query:
            # Display the generated SQL query
            st.subheader("Generated SQL Query")
            st.code(generated_query, language="sql")

            # Execute the SQL query
            db_file = "student.db"  # Ensure this matches your SQLite database path
            results = execute_sql_query(generated_query, db_file)

            if results:
                st.subheader("Query Results")
                # Check if it's a single scalar value
                if len(results) == 1 and len(results[0]) == 1:
                    st.metric(label="Result", value=results[0][0])
                else:
                    # Convert to a DataFrame for better display
                    df = pd.DataFrame(results, columns=["Column " + str(i + 1) for i in range(len(results[0]))])
                    st.table(df)
            else:
                st.info("No data returned from the query.")

