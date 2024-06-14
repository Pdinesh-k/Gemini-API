from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

#Function to load Gemini pro model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history = [])

def get_gemini_response(question):
    response = model.generate_content(question,stream = True)
    return response

#Intialize session state for chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

input_prompt = st.text_input("Input : ",key="input")
submit = st.button("Generate input")

if input_prompt and submit:
    response = get_gemini_response(input_prompt)
    st.session_state["chat_history"].append(("You : ",input_prompt))
    st.subheader("The Response is : ")
    for i in response:
        st.write(i.text)
        st.session_state["chat_history"].append(("AI : ",i.text))

st.subheader("The Chat history is : ")

for role,text in st.session_state["chat_history"]:
    st.write(f"{role}:{text}")




