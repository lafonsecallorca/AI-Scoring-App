import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os 

load_dotenv() #this will load all env variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are a text summarizer. You will be taking the text provided
and summarizing  the entire text in key points within 300 words. The text will be
appended here : """

def generate_summary(original_text, prompt):
    model=genai.GenerativeModel("gemini-pro")

    response=model.generate_content(prompt+original_text)
    return response.text