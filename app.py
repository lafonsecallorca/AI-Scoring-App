import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os 

load_dotenv() #this will load all env variables

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

prompt="""You are a text summarizer. You will be taking the text provided
and summarizing  the entire text in key points within 300 words. Please provide the 
summary of the text given here : """

def generate_summary(original_text, prompt):
    model=genai.GenerativeModel("gemini-pro")

    response=model.generate_content(prompt+original_text)
    return response.text

st.title("Text Summarizer")
user_text_input = st.text_input("Enter the text you would like to summarize:")

if st.button("Get Summary"):
    summary = generate_summary(user_text_input, prompt)
    st.markdown("AI Summary:")
    st.write(summary)




