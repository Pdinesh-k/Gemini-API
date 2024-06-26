import sqlite3

#Connect to sqllite
connection = sqlite3.connect("student.db")

#Create a cursor object to insert records , create table , retrieve
cursor = connection.cursor()

#Create the table
table_info = """
Create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT);
"""

#Line to create table
cursor.execute(table_info)

#Insert value
cursor.execute(""" Insert into STUDENT values("Cheenu","AI","A",99)""")
cursor.execute(""" Insert into STUDENT values("Oreo","ML","A",100)""")
cursor.execute(""" Insert into STUDENT values("Snow","DEVOPS","A",80)""")
cursor.execute(""" Insert into STUDENT values("Annie","FULL STACK","B",75)""")

#Display all the records
data = cursor.execute(""" Select * from STUDENT""")

for row in data:
    print(row)

#Close the connection
connection.commit()
connection.close()