from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro-vision")

def get_response(question,image):
    if question != "":
        reponse = model.generate_content([question,image])
    else:
        reponse = model.generate_content(image)

    return reponse.text

#Initialize our streamlit app

st.set_page_config(page_title="Gemini Image")
st.header("Text Response of Image")
input = st.text_input("Input Prompt: ",key="input")

uploaded_file = st.file_uploader("Choose an Image ",type=["jpg","jpeg","png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_column_width=True)

submit = st.button("Tell me about the image")

#If submit is clicked 
if submit:
    response = get_response(input,image)
    st.subheader("The response is ")
    st.write(response)




