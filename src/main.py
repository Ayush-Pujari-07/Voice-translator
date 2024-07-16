import os
import uuid
import warnings
import gradio as gr
import assemblyai as aai

from pathlib import Path
from deep_translator import GoogleTranslator
from deepgram import DeepgramClient, SpeakOptions
from dotenv import load_dotenv, find_dotenv


warnings.filterwarnings("ignore")

# Define output directory as a constant
OUTPUT_DIR = 'filepath'


load_dotenv(find_dotenv())


def voice_to_voice(audio_file):

    # transcribe audio
    transcript = audio_transcription(audio_file)

    if transcript.error:
        raise gr.Error(transcript.error)

    # translate text
    hi_translation, tr_translation, ja_translation = text_translation(
        transcript.text)

    # convert text to speech
    hi_audio_path = text_to_speech(hi_translation)
    tr_audio_path = text_to_speech(tr_translation)
    ja_audio_path = text_to_speech(ja_translation)

    hi_path = Path(hi_audio_path)
    tr_path = Path(tr_audio_path)
    ja_path = Path(ja_audio_path)

    return hi_path, tr_path, ja_path


def audio_transcription(audio_file):

    # Set the AssemblyAI API key
    aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    print(f"transcript text: {transcript.text}")
    return transcript


# def text_translation(text: str):

#     # English to Hindi
#     print(f"text: {text}")
#     translator_es = Translator(from_lang="en", to_lang="es")
#     es_text = translator_es.translclsate(text)

#     translator_tr = Translator(from_lang="en", to_lang="tr")
#     tr_text = translator_tr.translate(text)

#     translator_ja = Translator(from_lang="en", to_lang="ja")
#     ja_text = translator_ja.translate(text)

#     return es_text, tr_text, ja_text

def text_translation(text: str):

    # English to Hindi
    print(f"text: {text}")
    translator_hi = GoogleTranslator(source="en", target="hi")
    hi_text = translator_hi.translate(text)
    print(f"hi_text: {hi_text}")

    translator_tr = GoogleTranslator(source="en", target="tr")
    tr_text = translator_tr.translate(text)
    print(f"tr_text: {tr_text}")

    translator_ja = GoogleTranslator(source="en", target="ja")
    ja_text = translator_ja.translate(text)
    print(f"ja_text: {ja_text}")

    return hi_text, tr_text, ja_text


# def text_to_speech(text):

#     client = ElevenLabs(
#         api_key=os.environ.get("ELEVENLABSAI_API_KEY"))

#     # Calling the text_to_speech conversion API with detailed parameters
#     response = client.text_to_speech.convert(
#         voice_id="N2lVS1w4EtoT3dr4eOWO",  # Adam pre-made voice
#         optimize_streaming_latency="0",
#         output_format="mp3_22050_32",
#         text=text,
#         # use the turbo model for low latency, for other languages use the `eleven_multilingual_v2`
#         model_id="eleven_multilingual_v2",
#         voice_settings=VoiceSettings(
#             stability=0.5,
#             similarity_boost=1.0,
#             style=0.5,
#             use_speaker_boost=True,
#         ),
#     )

#     # Generating a unique file name for the output MP3 file
#     save_file_path = f"{uuid.uuid4()}.mp3"

#     # Writing the audio to a file
#     with open(save_file_path, "wb") as f:
#         for chunk in response:
#             if chunk:
#                 f.write(chunk)

#     print(f"{save_file_path}: A new audio file was saved successfully!")

#     # Return the path of the saved audio file
#     return save_file_path

def text_to_speech(text):
    try:
        if not os.environ.get("DEEPGRAM_API_KEY"):
            raise gr.Error("DEEPGRAM_API_KEY is not set")

        if not os.path.exists("translatdaudio"):
            os.mkdir("translatdaudio")

        filename = os.path.join("translatdaudio", "{}.mp3".format(uuid.uuid4()))

        deepgram = DeepgramClient(os.environ.get("DEEPGRAM_API_KEY"))

        options = SpeakOptions(
            model="aura-orpheus-en",
        )

        response = deepgram.speak.v("1").save(
            filename, {"text": text}, options)
        print(response.to_json(indent=4))

        return filename

    except Exception as e:
        print(f"Exception: {e}")


def create_output_dir():
    """Create the output directory if it doesn't exist"""
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)


def create_audio_input():
    """Create and return the audio input component"""
    return gr.Audio(sources=['microphone'], type=OUTPUT_DIR)


def create_audio_outputs():
    """Create and return the audio output components"""
    return [
        gr.Audio(label="Hindi"),
        gr.Audio(label="Turkish"),
        gr.Audio(label="Japanese")
    ]


def launch_demo():
    """Launch the Gradio demo interface"""
    demo = gr.Interface(
        fn=voice_to_voice,
        inputs=create_audio_input(),
        outputs=create_audio_outputs()
    )
    demo.launch()


if __name__ == "__main__":
    launch_demo()
