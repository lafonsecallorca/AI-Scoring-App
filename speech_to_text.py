import speech_recognition as sr

# Initialize recognizer
r = sr.Recognizer()

with sr.Microphone() as source:
    print("Say something...")
    # Adjust for ambient noise
    r.adjust_for_ambient_noise(source)
    
    # Record audio 
    audio_data = r.listen(source)
    print("Recognizing...")

    try:
        text = r.recognize_google(audio_data)
        print("You said:", text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
