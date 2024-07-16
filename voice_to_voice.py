import os
import gradio as gr
import assemblyai as aai
from dotenv import load_dotenv, find_dotenv
from translate import Translator
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
import uuid
from pathlib import Path


load_dotenv(find_dotenv())


def voice_to_voice(audio_file):

    # transcribe audio
    transcript  = audio_transcription(audio_file)

    if transcript.error:
        raise gr.Error(transcript.error)
    else:
        text = transcript.text

    # translate text
    hi_translation, ja_translation, es_translation = text_translation(text)

    # convert text to speech
    hi_audio_path = text_to_speech(hi_translation)
    ja_audio_path = text_to_speech(ja_translation)
    es_audio_path = text_to_speech(es_translation)

    hi_path = Path(hi_audio_path)
    ja_path = Path(ja_audio_path)
    es_path = Path(es_audio_path)

    return hi_path, ja_path, es_path


def audio_transcription(audio_file):

    # Set the AssemblyAI API key
    aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    return transcript.text


def text_translation(text):

    translator_hi = Translator(from_lang="eng", to_lang="hi")
    hi_text = translator_hi.translate(text)

    
    translator_ja = Translator(from_lang="eng", to_lang="ja")
    ja_text = translator_ja.translate(text)

    translator_es = Translator(from_lang="eng", to_lang="es")
    es_text = translator_es.translate(text)


    return hi_text, ja_text, es_text



def text_to_speech(text):
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABSAI_API_KEY")
    client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY)
    
    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id="kmSVBPu7loj4ayNinwWM", # Adam pre-made voice
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2", # use the turbo model for low latency, for other languages use the `eleven_multilingual_v2`
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=1.0,
            style=0.5,
            use_speaker_boost=True,
        ),
    )

    # uncomment the line below to play the audio back
    # play(response)

    # Generating a unique file name for the output MP3 file
    save_file_path = f"{uuid.uuid4()}.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
    return save_file_path


audio_input = gr.Audio(
    sources=["microphone"],
    type="filepath"
)

demo = gr.Interface(
    fn=voice_to_voice,
    inputs=audio_input,
    outputs=[gr.Audio(label="Hindi"), gr.Audio(
        label="Japanese"), gr.Audio(label="Spanish")]
)

if __name__ == "__main__":
    demo.launch()
