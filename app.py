import streamlit as st
import os
from dotenv import load_dotenv
import sqlite3
import pandas as pd
import google.generativeai as genai
from sql import create_table, insert_record, retrieve_data_from_table, delete_record, delete_table

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("Google API Key not found. Please set it in the environment variables.")

def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error fetching response from Gemini: {e}")
        return None

st.set_page_config(page_title="SQL Query Generator and Manager", page_icon=":guardsman:", layout="wide")
st.title("SQL Query Generator and Manager")

with st.expander("Create New Table"):
    table_name = st.text_input("Table Name")
    columns_input = st.text_area("Columns (e.g., Name TEXT, Age INT, Marks INT)")

    create_button_style = """
        <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        </style>
    """
    st.markdown(create_button_style, unsafe_allow_html=True)
    
    if st.button("Create Table", key="create_table_button"):
        if not table_name or not columns_input:
            st.error("Please provide both table name and column definitions.")
        else:
            try:
                columns = [col.strip().split() for col in columns_input.split(",")]
                create_table("student.db", table_name, columns)
                st.success(f"Table `{table_name}` created successfully!")
            except Exception as e:
                st.error(f"Error creating table: {e}")

with st.expander("Manage Existing Tables"):
    tables = sqlite3.connect("student.db").execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    table_names = [table[0] for table in tables]

    selected_table = st.selectbox("Select a table to manage", table_names)

    if selected_table:
        # Retrieve and display data from the selected table
        results = retrieve_data_from_table("student.db", selected_table)
        if results:
            st.subheader(f"Data from table `{selected_table}`")
            df = pd.DataFrame(results, columns=[f"Column {i + 1}" for i in range(len(results[0]))])
            st.table(df)
        else:
            st.info(f"No data available in `{selected_table}`.")

        # Insert a new record
        with st.form("Insert Record"):
            st.subheader("Insert a New Record")
            new_record = st.text_input("Enter record values (comma-separated, e.g., 'John, 25, 88')")
            submitted = st.form_submit_button("Insert Record")

            if submitted and new_record:
                try:
                    values = tuple(new_record.split(","))
                    insert_record("student.db", selected_table, values)
                    st.success("Record inserted successfully!")
                except Exception as e:
                    st.error(f"Error inserting record: {e}")

        # CRUD options: Update a record
        with st.form("Update Record"):
            st.subheader("Update an Existing Record")
            update_condition = st.text_input("Condition for record to update (e.g., 'Name = \"John\"')")
            update_values = st.text_input("Set values (e.g., 'Age = 30')")
            submitted = st.form_submit_button("Update Record")

            if submitted and update_condition and update_values:
                try:
                    conn = sqlite3.connect("student.db")
                    cursor = conn.cursor()
                    update_query = f"UPDATE {selected_table} SET {update_values} WHERE {update_condition}"
                    cursor.execute(update_query)
                    conn.commit()
                    st.success("Record updated successfully!")
                except Exception as e:
                    st.error(f"Error updating record: {e}")
                finally:
                    conn.close()

        # CRUD options: Delete a record
        st.subheader("Delete a Record")
        record_id = st.text_input("Enter condition to delete record (e.g., 'ID = 1')")
        if st.button("Delete Record"):
            if record_id:
                try:
                    delete_record("student.db", selected_table, record_id)
                    st.success("Record deleted successfully!")
                except Exception as e:
                    st.error(f"Error deleting record: {e}")

        # Option to delete the whole table
        if st.button(f"Delete Table `{selected_table}`"):
            confirm = st.radio("Are you sure you want to delete this table?", ("Yes", "No"))
            if confirm == "Yes":
                try:
                    delete_table("student.db", selected_table)
                    st.success(f"Table `{selected_table}` has been deleted.")
                except Exception as e:
                    st.error(f"Error deleting table `{selected_table}`: {e}")
            else:
                st.info("Table deletion canceled.")

        # Generate and Execute Query
        st.subheader("Generate and Execute SQL Query")
        user_input = st.text_input("Enter your question about this table:")

        if st.button("Generate and Execute Query for Table"):
            if not user_input.strip():
                st.error("Please enter a valid question.")
            else:
                question = f"Translate the following question into a valid SQL query for the table `{selected_table}`: {user_input}"
                generated_query = get_gemini_response(question)

                if generated_query:
                    st.subheader("Generated SQL Query")
                    st.code(generated_query, language="sql")

                    db_file = "student.db"  
                    try:
                        # Remove any unwanted formatting in the query
                        generated_query = generated_query.replace("```sql", "").replace("```", "").strip()

                        conn = sqlite3.connect(db_file)
                        cursor = conn.cursor()
                        cursor.execute(generated_query)
                        results = cursor.fetchall()
                        conn.commit()

                        if results:
                            st.subheader("Query Results")
                            df = pd.DataFrame(results, columns=[f"Column {i + 1}" for i in range(len(results[0]))])
                            st.table(df)
                        else:
                            st.success("Query executed successfully, but no data was returned.")
                    except Exception as e:
                        st.error(f"Error executing query: {e}")
                    finally:
                        conn.close()
                else:
                    st.error("Error generating the query.")
