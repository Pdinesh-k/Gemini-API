from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from io import BytesIO

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro-vision")

def generate_func(image_prompt,input,image_data):
    response = model.generate_content([image_prompt,input,image_data[0]])
    return response.text

def get_bytes(image):
    if image is not None:
        image_byte_arr = BytesIO()
        image.save(image_byte_arr, format='PNG')
        bytes = image_byte_arr.getvalue()
        key = [
            {
            "mime_type" : "image/png",
            "data" : bytes
            }
        ]
        return key
st.set_page_config(page_title="Cheenu's BOT")
st.header("Invoice Extractor using Gemini")
image_uploader = st.file_uploader("Upload the required Image",type=["png","jpg","jpeg"])
if image_uploader is not None:
    image = Image.open(image_uploader)
    st.image(image,caption="Uploaded Image")
input_box = st.text_input("Ask something about this Image",key="input")
submit = st.button("Submit the question")


input_prompt = """
Hi my dear Gemini , I know you are master at everything , but i need one help from you , which is i have uploaded one image , just extract the data from it and answer my questions that's the task for you
"""
if submit:
    bytes_value = get_bytes(image)
    result = generate_func(input_prompt,input_box,bytes_value)
    st.subheader("The Response is : ")
    st.write(result)



