# Import required libraries
import os  # For accessing environment variables
import azure.cognitiveservices.speech as speechsdk  # Azure Speech SDK for speech-to-text and translation
from dotenv import load_dotenv  # Load environment variables from a .env file

# Load environment variables from a .env file
load_dotenv()

# Retrieve Azure Speech Service credentials from environment variables
service_region = os.getenv("AZURE_SPEECH_SERVICE_REGION")  # Azure region (e.g., "uksouth", "eastus")
speech_key = os.getenv("AZURE_SPEECH_SERVICE_KEY")  # Subscription key for Azure Speech Service


def recognize_and_translate_from_microphone():
    """
    Captures speech from the microphone, converts it to text using Azure Speech Service,
    and translates the recognized speech into a target language.
    """

    # Create a SpeechTranslationConfig object with the Azure Speech Service credentials
    speech_translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=speech_key, region=service_region
    )

    # Set the language for speech recognition (input language)
    speech_translation_config.speech_recognition_language = "en-US"

    # Define the target language for translation
    target_language = "fr"  # French (change to "es", "de", "hi", etc. for other languages)

    # Add the target language to the translation configuration
    speech_translation_config.add_target_language(target_language)

    # Configure audio input to use the system's default microphone
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    # Create a TranslationRecognizer object with the speech and audio configurations
    translation_recognizer = speechsdk.translation.TranslationRecognizer(
        translation_config=speech_translation_config, audio_config=audio_config
    )

    print("Speak into your microphone.")  # Prompt the user to speak

    # Start speech recognition and translation asynchronously and wait for the result
    translation_recognition_result = translation_recognizer.recognize_once_async().get()

    # Check the result of speech recognition and translation
    if translation_recognition_result.reason == speechsdk.ResultReason.TranslatedSpeech:
        # Successfully recognized speech, print the transcribed text
        print("Recognized:", translation_recognition_result.text)

        # Print the translated text in the target language
        print(f"Translated into '{target_language}': {translation_recognition_result.translations[target_language]}")

    elif translation_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        # No speech detected, print a message
        print("No speech could be recognized:", translation_recognition_result.no_match_details)

    elif translation_recognition_result.reason == speechsdk.ResultReason.Canceled:
        # Speech recognition was canceled due to an error
        cancellation_details = translation_recognition_result.cancellation_details
        print("Speech Recognition canceled:", cancellation_details.reason)

        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            # If there was an error, print the details
            print("Error details:", cancellation_details.error_details)
            print("Did you set the speech resource key and region values?")  # Suggest troubleshooting

# Call the function to start speech recognition and translation
recognize_and_translate_from_microphone()
