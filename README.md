# Web-based SQL Query Generator and Result Viewer

This project implements a web-based SQL Query Generator and Result Viewer using **Streamlit**. The user can input natural language questions, and the system will use the **Gemini AI** model to generate SQL queries. The SQL queries are then executed against a **SQLite** database, and the results are displayed in a user-friendly manner.

## Steps

1. **Convert natural language questions into SQL queries** using Gemini AI.
2. **Display the generated SQL query.**
3. **Execute the SQL query** on an SQLite database.
4. **Show the query results** in a table or as a scalar metric (e.g., average, count).
5. **Display appropriate error messages** when issues occur.

## Requirements

To run this app, ensure you have the following dependencies installed:

- **Python** (version 3.7 or higher)
- **Streamlit**
- **Google Gemini API** (via the google-generativeai package)
- **SQLite3** (for database interaction)
- **Dotenv** (for loading environment variables like the API key)
- **Pandas** (for displaying results in tabular format)

## Set Up Your Google Gemini API Key

1. Go to your **Google Cloud Console**, create a project, and enable the **Gemini API**.
2. Once you have the API key, create a `.env` file in the root of the project and add your API key as follows:

```env
GOOGLE_API_KEY=your_api_key_here
