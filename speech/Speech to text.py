import os
import azure.cognitiveservices.speech as speechsdk
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_DEPLOYMENT_ENDPOINT = os.getenv("OPENAI_DEPLOYMENT_ENDPOINT")
OPENAI_GPT4_DEPLOYMENT_NAME = os.getenv("OPENAI_GPT4_DEPLOYMENT_NAME")

#init the openai client
client = AzureOpenAI(
  azure_endpoint = OPENAI_DEPLOYMENT_ENDPOINT, 
  api_key=OPENAI_API_KEY,  
  api_version="2023-05-15"
)

SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")
engine_name = "test"


speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
# Set up Azure Text-to-Speech language 
speech_config.speech_synthesis_language = "en-US"
# Set up Azure Speech-to-Text language recognition
speech_config.speech_recognition_language = "en-US"
speech_config.set_property(speechsdk.PropertyId.Speech_LogFilename, "./log/log.txt")

# Set up the voice configuration
speech_config.speech_synthesis_voice_name = "en-US-JennyMultilingualNeural"
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

# Define the speech-to-text function
def speech_to_text():
    # Set up the audio configuration
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    # Create a speech recognizer and start the recognition
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    print("Say something...")

    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "Sorry, I didn't catch that."
    elif result.reason == speechsdk.ResultReason.Canceled:
        return "Recognition canceled."

# Define the text-to-speech function
def text_to_speech(text):
    try:
        result = speech_synthesizer.speak_text_async(text).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Text-to-speech conversion successful.")
            return True
        else:
            print(f"Error synthesizing audio: {result}")
            return False
    except Exception as ex:
        print(f"Error synthesizing audio: {ex}")
        return False

def evaluate_sentiment(text):
    system_message = """
    You are an AI assistant that helps recognize the sentiment in a given text.
    1. Evaluate the given text and provide the category of the sentiment as either positive, negative, or neutral.
    2. Do not provide any additional examples to the output, just the category.
    """

    response = client.chat.completions.create(
        model=OPENAI_GPT4_DEPLOYMENT_NAME,
        messages = [
            {"role":"system","content":system_message},
            {"role":"user","content":text}
            ],
        temperature=0   
    )
    return response.choices[0].message.content

def translate(text, target_language):
    system_message = """You are a helpful assistant that translates text into """ + target_language + """.
    Answer in a clear and concise manner only translating the text.
    Text:
    """

    response = client.chat.completions.create(
        model=OPENAI_GPT4_DEPLOYMENT_NAME,
        messages = [
            {"role":"system","content":system_message},
            {"role":"user","content":text}
            ],
        temperature=0   
    )
    return response.choices[0].message.content


# Main program loop
while True:
    # Get input from user using speech-to-text
    user_input = speech_to_text()
    print(f"You said: {user_input}")

    # Evaluate the sentiment using OpenAI
    response = evaluate_sentiment(user_input)
    print(f"AI says: {response}")

    # Translate the text to Spanish using OpenAI
    translated_text = translate(user_input, "Spanish")
    print(f"AI translated to Spanish: {response}")
    # Convert the response to speech using text-to-speech
    text_to_speech(translated_text)