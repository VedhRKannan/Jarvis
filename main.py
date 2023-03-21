import openai
import pyttsx3
from io import BytesIO
import speech_recognition as sr

openai.api_key = "sk-" # Enter your private API key here
engine = pyttsx3.init()
messages = [
    {"role": "system", "content": "You are a kind helpful assistant named Jarvis. You are an expert in Science, History and Cooking. You will provide helpful and concise responses. "}, 
] # Modify system message to your specific needs


def transcribe_microphone_smart():
    # Create a recognizer object
    r = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Speak now...")
        # Listen for speech and stop after 2 seconds of silence
        audio = r.listen(source, phrase_time_limit=2)

    # Use Google's Speech Recognition API to transcribe the audio
    try:
        transcription = r.recognize_google(audio, show_all=False)
        return transcription
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
        return ""
    except sr.RequestError as e:
        print(
            "Could not request results from Speech Recognition service; {0}".format(e))
        return ""


while True:
    # r = s_r.Recognizer()
    # with s_r.Microphone() as source:
    #     audio =r.listen(source)
    #     print("Listening...")

    message = transcribe_microphone_smart()
    if message == "bye":
        engine.say("Bye. If you need anything I am here.")
        engine.runAndWait()
        exit()
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-4", messages=messages
        )

    reply = chat.choices[0].message.content
    print(f"Jarvis: {reply}")
    pyttsx3.speak(reply)
    messages.append({"role": "assistant", "content": reply})
