import os
import gradio as gr
import assemblyai as aai
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def voice_to_voice(audio_file):

    # transcribe audio
    transcription = audio_transcription(audio_file)

    # translate text
    translation = text_translation(transcription)

    # convert text to speech
    speech = text_to_speech(translation)

    return speech


def audio_transcription(audio_file):

    # Set the AssemblyAI API key
    aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    return transcript.text


def text_translation(transcription):
    return transcription


def text_to_speech(translation):
    return translation


audio_input = gr.Audio(
    sources=["microphone"],
    type="filepath"
)

demo = gr.Interface(
    fn=voice_to_voice,
    inputs=audio_input,
    outputs=[gr.Audio(label="English"), gr.Audio(
        label="Hindi"), gr.Audio(label="Kannada")]
)

if __name__ == "__main__":
    demo.launch()
