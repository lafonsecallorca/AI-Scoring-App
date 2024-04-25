import streamlit as st
import speech_recognition as sr
import spacy
import en_core_web_md

nlp = en_core_web_md.load()


def read_questions_from_file(file_path):
    with open(file_path, 'r') as file:
        questions = [line.strip() for line in file.readlines()[:10] if line.strip()]
    return questions

def save_to_file(contents, filename):
    with open(filename, "w") as file:
        for line in contents:
            file.write(line + "\n")

def main():
    st.title("Questionnaire")

    file_path = "questions.txt"  # Path to your file containing questions
    questions = read_questions_from_file(file_path)
    answer_key = read_questions_from_file("answers.txt")
    num_questions = len(questions)
    current_question_index = st.session_state.get('current_question_index', 0)

    if 'responses' not in st.session_state:
        st.session_state.responses = [""] * num_questions

    if current_question_index < num_questions:
        st.write("Answer the question below:")
        st.write(questions[current_question_index])


        response = st.session_state.responses[current_question_index]  # Retrieve response from session state
        
        record_button = st.button("Record Response")
        stop_button = st.button("Stop Recording")

        if record_button:
            st.session_state.stop_recording = False
            with sr.Microphone() as source:
                  st.write("Say something...")
                  r = sr.Recognizer()
                  r.adjust_for_ambient_noise(source)
                  while not st.session_state.stop_recording:
                     audio_data = r.listen(source)
                     st.write("Recognizing...")
                     
                     try:
                        text = r.recognize_google(audio_data)
                        response = text  # Update response with speech-to-text result
                        st.session_state.responses[current_question_index] = response  # Save response to session state
                        st.write("You said:", text)
                     except sr.UnknownValueError:
                        st.write("Google Speech Recognition could not understand the audio")
                     except sr.RequestError as e:
                        st.write("Could not request results from Google Speech Recognition service; {0}".format(e))
                     if st.session_state.stop_recording:
                        break

        if stop_button:
            st.session_state.stop_recording = True
            current_question_index += 1
            st.session_state.current_question_index = current_question_index  # Update current question index when stopping recording


        if st.button("Submit") and response:  # Submit only if a response is provided
            current_question_index += 1
            st.session_state.current_question_index = current_question_index
            
            
    if current_question_index == num_questions:
        st.write("All questions answered!")


        correct_answers = 0
        for i, (question, response) in enumerate(zip(questions, st.session_state.responses)):
   
            
            # Compute similarity between student response and answer key
            similarity = nlp(response).similarity(nlp(answer_key[i]))
            
#            st.write(f"{similarity} and right answer: {answer_key[i]}")
            # Set a threshold value for similarity
            threshold = 0.75
            
            # Check if similarity is above the threshold
            if similarity >= threshold:
                correct_answers += 1

        st.write(f"Number of correct answers: {correct_answers} out of {num_questions}")

        for i, (question, response) in enumerate(zip(questions, st.session_state.responses)):
            st.write(f"{question}: {response}")

        student_answers = "studentsanswers.txt"
        save_to_file(st.session_state.responses, student_answers)

if __name__ == "__main__":
    main()
