import sqlite3

# Connect to SQLite
def connect_to_db(db="student.db"):
    return sqlite3.connect(db)

# Create a new table
def create_table(db, table_name, columns):
    conn = None
    try:
        conn = connect_to_db(db)
        cursor = conn.cursor()
        column_defs = ", ".join([f"{col[0]} {col[1]}" for col in columns])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_defs});"
        cursor.execute(create_table_query)
        conn.commit()
        print(f"Table `{table_name}` created successfully!")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
    finally:
        if conn:
            conn.close()

# Insert records
def insert_record(db, table_name, values):
    conn = None
    try:
        conn = connect_to_db(db)
        cursor = conn.cursor()
        placeholders = ", ".join(["?"] * len(values))
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        cursor.execute(insert_query, values)
        conn.commit()
        print("Record inserted successfully!")
    except sqlite3.Error as e:
        print(f"Error inserting record: {e}")
    finally:
        if conn:
            conn.close()

# Retrieve data
def retrieve_data_from_table(db, table_name):
    conn = None
    try:
        conn = connect_to_db(db)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name};")
        data = cursor.fetchall()
        return data
    except sqlite3.Error as e:
        print(f"Error retrieving data: {e}")
        return None
    finally:
        if conn:
            conn.close()

# Delete a record
def delete_record(db, table_name, condition):
    conn = None
    try:
        conn = connect_to_db(db)
        cursor = conn.cursor()
        delete_query = f"DELETE FROM {table_name} WHERE {condition}"
        cursor.execute(delete_query)
        conn.commit()
        print(f"Record(s) deleted from `{table_name}`.")
    except sqlite3.Error as e:
        print(f"Error deleting record(s): {e}")
    finally:
        if conn:
            conn.close()

# Delete a table
def delete_table(db, table_name):
    conn = None
    try:
        conn = connect_to_db(db)
        cursor = conn.cursor()
        delete_table_query = f"DROP TABLE IF EXISTS {table_name};"
        cursor.execute(delete_table_query)
        conn.commit()
        print(f"Table `{table_name}` deleted successfully!")
    except sqlite3.Error as e:
        print(f"Error deleting table `{table_name}`: {e}")
    finally:
        if conn:
            conn.close()

# Check if table exists
def table_exists(db, table_name):
    conn = None
    try:
        conn = connect_to_db(db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
        exists = cursor.fetchone() is not None
        return exists
    except sqlite3.Error as e:
        print(f"Error checking table existence: {e}")
        return False
    finally:
        if conn:
            conn.close()

# Main logic to test the functions
if __name__ == "__main__":
    columns = [("Name", "TEXT"), ("Age", "INT"), ("Marks", "INT")]

    if table_exists("student1.db", "STUDENT1"):
        print("Table already exists. Deleting and recreating...")
        delete_table("student1.db", "STUDENT1")

    create_table("student1.db", "STUDENT1", columns)

    insert_record("student1.db", "STUDENT1", ("John", 25, 88))
    insert_record("student1.db", "STUDENT1", ("Mahi", 25, 34))
    insert_record("student1.db", "STUDENT1", ("David", 20, 89))
    insert_record("student1.db", "STUDENT1", ("Martha", 25, 88))
    insert_record("student1.db", "STUDENT1", ("Kiran", 20, 90))

    records = retrieve_data_from_table("student1.db", "STUDENT1")
    for record in records:
        print(record)

    delete_record("student1.db", "STUDENT1", "Name = 'John'")
