# Import required libraries
import os  # For accessing environment variables
import azure.cognitiveservices.speech as speechsdk  # Azure Speech SDK for text-to-speech (TTS)
from dotenv import load_dotenv  # Load environment variables from a .env file

# Load environment variables from a .env file
load_dotenv()

# Retrieve Azure Speech Service credentials from environment variables
service_region = os.getenv("AZURE_SPEECH_SERVICE_REGION")  # Azure region (e.g., "uksouth", "eastus")
speech_key = os.getenv("AZURE_SPEECH_SERVICE_KEY")  # Subscription key for Azure Speech Service

# Create a SpeechConfig object with the Azure Speech Service credentials
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Configure audio output to use the system's default speaker
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# Set the voice name for speech synthesis
# AvaMultilingualNeural is a neural voice that can speak multiple languages
speech_config.speech_synthesis_voice_name = "en-US-AvaMultilingualNeural"

# Create a SpeechSynthesizer object with the speech and audio configurations
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# Prompt the user to enter text
print("Enter some text that you want to synthesize into speech >")
text = input()  # Take user input

# Synthesize the input text into speech asynchronously and wait for the result
speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

# Check the result of the speech synthesis process
if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    # If synthesis was successful, print a confirmation message
    print(f"Speech synthesized successfully for text: [{text}]")

elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
    # If synthesis was canceled, print the reason
    cancellation_details = speech_synthesis_result.cancellation_details
    print(f"Speech synthesis canceled: {cancellation_details.reason}")

    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        # If there was an error, print the error details
        if cancellation_details.error_details:
            print(f"Error details: {cancellation_details.error_details}")
            print("Did you set the speech resource key and region values correctly?")
