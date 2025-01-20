import sqlite3
##Connect to sqlite
connection=sqlite3.connect(r"E:\TexttoSQL\student.db")
##Create cursor to insert,create table etc
cursor=connection.cursor()
table_info="""
Create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT);

"""
cursor.execute(table_info)
## Insert Some more records

cursor.execute('''Insert Into STUDENT values('Krishna','Data Science','A',90)''')
cursor.execute('''Insert Into STUDENT values('Sudeep','Data Science','B',100)''')
cursor.execute('''Insert Into STUDENT values('Darsh','Data Science','A',86)''')
cursor.execute('''Insert Into STUDENT values('Vicky','DEVOPS','A',50)''')
cursor.execute('''Insert Into STUDENT values('Dipika','DEVOPS','A',35)''')
print("The isnerted records are")
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)
print("Database connected and table created successfully!")

## Commit your changes int he databse
connection.commit()
connection.close()