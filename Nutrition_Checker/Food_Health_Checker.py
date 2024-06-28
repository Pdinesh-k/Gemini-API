from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt,image):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts=[
            {
                "mime_type" : uploaded_file.type,
                "data" : bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("File not uploaded")
    
input_prompt = """
You are an expert in nutritionist where you need to see the food items from the image
and calculate the total calories , also provide the details of every food items with calories
intake in below format

1.Item 1 : No of calories
2.Item 2 : No of calories
----
----
Finally you can also mention whether the food is healthy or not and also
mention the percentage split of the ratio of carbohydrates , fats , fibres , sugar and
other important things required in our diet 

If there is no food in the image , Tell there is no Food in the above image in a good manner
"""
    
#Initialize our Streamlit app

st.set_page_config(page_title="Calories Advisor App")

st.header("Calories and Health Checker")
uploaded_file = st.file_uploader("Choose an image...",type=["jpeg","jpg","png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,use_column_width=True)
submit = st.button("Tell me about the total calories")

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt,image_data)
    st.subheader("The Response : ")
    st.write(response)

