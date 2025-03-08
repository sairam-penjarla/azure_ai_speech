import os
import azure.cognitiveservices.speech as speechsdk
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from dotenv import load_dotenv

load_dotenv()

# Load Azure Speech Service credentials
service_region = os.getenv("AZURE_SPEECH_SERVICE_REGION")
speech_key = os.getenv("AZURE_SPEECH_SERVICE_KEY")

timeout_seconds = 5  # Timeout to stop listening when user stops speaking

app = Flask(__name__)
socketio = SocketIO(app)

def get_translator():
    """Configures the speech translation service"""
    translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=speech_key, region=service_region
    )
    translation_config.speech_recognition_language = "en-US"
    translation_config.add_target_language("fr")
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    return speechsdk.translation.TranslationRecognizer(
        translation_config=translation_config, audio_config=audio_config
    )

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start_listening')
def start_listening():
    recognizer = get_translator()
    socketio.emit('status', {'status': 'listening'})
    print("Listening...")

    done = False
    
    def stop_callback(evt):
        """Callback to stop listening"""
        nonlocal done
        done = True
    
    recognizer.session_stopped.connect(stop_callback)
    recognizer.canceled.connect(stop_callback)

    def recognizing_handler(evt):
        """Send partial results to the UI in real-time"""
        socketio.emit('interim_text', {'text': evt.result.text})

    def recognized_handler(evt):
        """Send recognized text for translation"""
        if evt.result.reason == speechsdk.ResultReason.TranslatedSpeech:
            text = evt.result.text
            translation = evt.result.translations["fr"]
            socketio.emit('translation_result', {'original': text, 'translated': translation})
            print(f"English: {text} -> French: {translation}")

    recognizer.recognizing.connect(recognizing_handler)
    recognizer.recognized.connect(recognized_handler)
    recognizer.start_continuous_recognition()
    
    while not done:
        pass

@socketio.on('stop_listening')
def stop_listening():
    socketio.emit('status', {'status': 'translating'})
    print("Stopped listening, translating...")

if __name__ == '__main__':
    socketio.run(app, debug=True)
