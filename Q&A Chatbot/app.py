from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

#Function to load Gemini Model and get responses
model = genai.GenerativeModel("gemini-pro")

def generate_text(question):
    response = model.generate_content(question)
    return response.text

#Creating an Frontend application with minimal code
st.set_page_config(page_title="Cheenu's BOT")
st.title("Cheenu's first AI")
st.header("AI Chatbot")

input = st.text_input("Ask Someting",key = "input")
submit = st.button("Give me response")

if submit:
    response = generate_text(input)
    st.subheader("The response is : ")
    st.write(response)

