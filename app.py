import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os 

load_dotenv() #this will load all env variables

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

prompt="""You are an exam question creator and grader. You will be taking the text provided
and create 10 exam questions along with their answers from the text. The text provided will be given here : """

def generate_qa(original_text, prompt):
    model=genai.GenerativeModel("gemini-pro")

    response=model.generate_content(prompt+original_text)
    return response.text

def scrape_website(website_url):
    pass

def extract_answer_keys(summary, section):
    # Split the summary by the "Answers:" section
    parts = summary.split(section)
    
    # If the "Answers:" section exists and there's at least one part after it
    if len(parts) > 1:
        # Extract the text after the "Answers:" section
        if section == "Answers:":
            answer_keys_section = parts[1].strip()

        answer_keys_section = parts[1].strip()
        
        # Split the answer keys section into individual lines
        lines = answer_keys_section.split("\n")
        
        # Initialize an empty list to store answer keys
        answer_keys = []
        
        # Iterate through each line to extract answer keys
        for line in lines:
            # Skip any empty lines
            if line.strip() != "":
                # Add the line to the list of answer keys
                answer_keys.append(line.strip())
        
        return answer_keys
    else:
        return None

def save_to_file(contents, filename):
    st.write("Custom save_to_file function: Saves contents to a file.")
    with open(filename, "w") as file:
        for line in contents:
            file.write(line + "\n")

st.title("Exam Q&A")
user_text_input = st.text_input("Enter the text you would like to summarize:")


if st.button("Get Summary"):
    examq_a = generate_qa(user_text_input, prompt)
    #if summary.prompt_feedback:
    #    print(summary.prompt_feedback)
    ans_section = "Answers:"
    qs_section = "Questions:"
    answer_key = extract_answer_keys(examq_a, ans_section )
    question_key = extract_answer_keys(examq_a, qs_section)
    answer_file = "answers.txt"
    question_file = "questions.txt"
    save_to_file(answer_key, answer_file)
    save_to_file(question_key, question_file)
    save_to_file
    st.markdown("AI Q&A:")
    st.write(examq_a)
   

   




