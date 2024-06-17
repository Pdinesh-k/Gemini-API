from dotenv import load_dotenv
#To Load all the environment variables from .env
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

#Function to load Gemini Pro Vision
model = genai.GenerativeModel("gemini-pro-vision")

def gemini_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

#Function to get bytes from the Image so we can process Invoice Extractor
def get_bytes(uploaded_file):

    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type" : uploaded_file.type,
                "data" : bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

#Initialize Streamlit app
st.set_page_config(page_title = "Invoice Extractor")
st.header("Multi Language Invoice Extrator")
input_text = st.text_input("Input : ",key = "input")

uploaded_file = st.file_uploader("Choose an Image",type=["jpeg","jpg","png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded your Image",use_column_width=True)

submit = st.button("Tell me about the Invoice")

input_prompt = """
You are an axpert in understanding invoices . We will upload a
 image as invoice and you will have to answer 
 any questions based on uploaded invoice image """

if submit:
    image_data = get_bytes(uploaded_file)
    response = gemini_response(input_prompt,image_data,input_text)
    st.subheader("The response is")
    st.write(response)



