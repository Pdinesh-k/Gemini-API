from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import pdf2image
import io
import base64


genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([prompt,pdf_content[0],input])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        #Convert the pdf to image
        image = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = image[0]

        #Convert to bytes
        img_bytes_arr = io.BytesIO()
        first_page_arr = first_page.save(img_bytes_arr,"JPEG")
        img_bytes_arr = img_bytes_arr.getvalue()

        pdf_parts = [
        {
        "mime_type" : "image/jpeg",
        "data" :  base64.b64encode(img_bytes_arr).decode()
        }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
st.set_page_config(page_title="ATS Tracker")
st.header("ATS Tracking Systtem")
input_box = st.text_input("Job Description",key="input")
uploaded_file = st.file_uploader("Upload your Resume(PDF)",type=["pdf"])

if uploaded_file is not None:
    st.write("File Uploaded Successfully")

submit_1 = st.button("Percentage Match")

submit_2 = st.button("How Can I Improvise my Skills")

submit_3 = st.button("Tell me about the Resume")

input_prompt_1 = """
You are an experienced ATS Tracking system with a deep understanding of Data Science
Machine Learning , Artifical Intelligence , FullStackDevelopment , Devops and ATS Functionality,
Your task is to evaluate the resume against the provided job description.
Give me the percentage which matches in his resume by the specified job description,
The output should come as percentage and then keywords missing on job roles
"""

input_prompt_2 = """
You are an experienced HR With Tech Experience in the field of Data Science
Machine Learning , Artifical Intelligence , FullStackDevelopment , Devops , your task is to review 
the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with these roles.
Highlight the points which he can improve his Skills so that he will perfectly match for this role 
according to the job roles , you should clearly give the output according to the missing keywords in Resume
"""

input_prompt_3 = """
You are an experienced HR With Tech Experience in the field of Data Science
Machine Learning , Artifical Intelligence , FullStackDevelopment , Devops , your task is to review 
the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with these roles.
Highlight with the strengths and weaknesses of the applicant in relation
to the specified job roles
"""

if submit_1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt_1,pdf_content,input_box)
        st.subheader("The Response is : ")
        st.write(response)
    else:
        st.write("Please upload the Resume")

elif submit_2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt_2,pdf_content,input_box)
        st.subheader("The Response is : ")
        st.write(response)
    else:
        st.write("Please upload the Resume")

else:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt_3,pdf_content,input_box)
        st.subheader("The Response is : ")
        st.write(response)
    else:
        st.write("Please upload the Resume")


