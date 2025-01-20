# Web-based SQL Query Generator and Result Viewer

This project implements a web-based SQL Query Generator and Result Viewer using **Streamlit**. The user can input natural language questions, and the system will use the **Gemini AI** model to generate SQL queries. The SQL queries are then executed against a **SQLite** database, and the results are displayed.

## Steps

1. **Convert natural language questions into SQL queries** using Gemini AI.
2. **Display the generated SQL query.**
3. **Execute the SQL query** on an SQLite database.
4. **Show the query results** in a table or as a scalar metric (e.g., average, count).

## Requirements

To run this app, the following dependencies installed:

- **Python**
- **Streamlit**
- **Google Gemini API** 
- **SQLite3** 
- **Dotenv** 
