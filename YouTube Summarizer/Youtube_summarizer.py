from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re

prompt = """
You are a YouTube video summarizer. You will be taking the transcript
text and summarizing the entire video, providing the important summary
in points within 250 words. The transcript text will be appended here. Please provide the summary:
"""

# Getting the summary based on the prompt from Google Gemini Pro
def get_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Getting the transcript details from the YouTube video
def extract_transcript_text(video_id):
    transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

    transcript = ""
    for i in transcript_text:
        transcript += " " + i["text"]
    return transcript

# Function to extract the video ID from various YouTube URL formats
def get_video_id(url):
    # Regular expression to extract video ID from full and shortened YouTube URLs
    regex = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None

st.header("YouTube Video Summarizer!!")
link = st.text_input("Provide your YouTube Link")
if link:
    video_id = get_video_id(link)
    if video_id:
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

        if st.button("Get Detailed Notes"):
            transcript_text = extract_transcript_text(video_id)

            if transcript_text:
                response = get_gemini_content(transcript_text, prompt)
                st.markdown("## Detailed Notes:")
                st.write(response)
    else:
        st.error("Invalid YouTube URL. Please provide a correct URL.")
