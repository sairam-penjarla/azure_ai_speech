# Import required libraries
import os  # For accessing environment variables
import azure.cognitiveservices.speech as speechsdk  # Azure Speech SDK for speech recognition
from dotenv import load_dotenv  # Load environment variables from a .env file

# Load environment variables from a .env file
load_dotenv()

# Retrieve Azure Speech Service credentials from environment variables
service_region = os.getenv("AZURE_SPEECH_SERVICE_REGION")  # Azure region (e.g., "uksouth", "eastus")
speech_key = os.getenv("AZURE_SPEECH_SERVICE_KEY")  # Subscription key for Azure Speech Service


def recognize_from_microphone():
    """
    Captures speech from the microphone, converts it to text using Azure Speech Service,
    and prints the recognized text or error messages.
    """

    # Create a SpeechConfig object with the Azure Speech Service credentials
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Set the language for speech recognition (change to another language if needed)
    speech_config.speech_recognition_language = "en-US"

    # Configure audio input to use the system's default microphone
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    # Create a SpeechRecognizer object with the speech and audio configurations
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")  # Prompt the user to speak

    # Start speech recognition asynchronously and wait for the result
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    # Check the result of speech recognition
    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        # Successfully recognized speech, print the transcribed text
        print("Recognized:", speech_recognition_result.text)

    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        # No speech detected, print a message
        print("No speech could be recognized:", speech_recognition_result.no_match_details)

    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        # Speech recognition was canceled due to an error
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled:", cancellation_details.reason)

        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            # If there was an error, print the details
            print("Error details:", cancellation_details.error_details)
            print("Did you set the speech resource key and region values?")  # Suggest troubleshooting

# Call the function to start speech recognition
recognize_from_microphone()
