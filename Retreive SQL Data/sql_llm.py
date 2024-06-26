from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
import sqlite3

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

#Function to load Gemini and provide sql query as response
def get_gemini_response(quiz,prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([quiz,prompt[0]])
    return response.text

#Function to retrieve query from sql database
def read_sql_query(sql,db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

prompt = [
    """
You are an expert in converting English Questions to SQL query!
The SQL database has the name STUDENT and has the following columns - NAME,
CLASS , SECTION \n\n For example , \n Example 1 - How many entries of records are present?,
the SQL command will be something like this SELECT COUNT(*) FROM STUDENT;
\n Example 2 - Tell me all the student studying in Data Science class?,
the SQL command will be something like this SELECT * FROM STUDENT
where CLASS="Data Science";
also the sql code should not have in beginning or end and sql word in the output

    """
]

st.set_page_config(page_title="Retrievation of Any SQL query")
st.header("Gemini App to Retreive SQL data")
question = st.text_input("Input: ",key="input")
submit = st.button("Ask the question")

if submit:
    response = get_gemini_response(question,prompt)
    print(response)
    data = read_sql_query(response,"student.db")
    st.subheader("The Response is")
    for row in data:
        print(row)
        st.header(row)