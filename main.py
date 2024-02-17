# System imports
import os
import logging
# Library imports
import deepl
from dotenv import load_dotenv
from gtts import gTTS
import elevenlabs
# Local imports
from anki_functions import create_sound_deck


load_dotenv() # passes values from local .env file to os
DEEPL_KEY = os.environ["DEEPL_KEY"]
ELEVENLABS_KEY = os.environ["ELEVENLABS_KEY"]
ANKI_PATH = os.path.expandvars(r"%APPDATA%/Anki2/User 1/collection.media")

# Read in the transcript file
def generate_gtts(text, language='ru', filename='output.mp3'):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(filename)
    filename = os.path.basename(filename)
    return filename

def generate_tts(text, filename='output.mp3'):
    audio = elevenlabs.generate(
    text=text,
    voice="Antoni",
    model="eleven_multilingual_v2"
    )
    with open(filename, mode='bx') as f:
        f.write(audio)
    filename = os.path.basename(filename)
    return filename

def process_transcript(
        transcript_path, mp3_folder=os.getcwd(), out_name=None):
    with open(transcript_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    translator = deepl.Translator(DEEPL_KEY)
    out_name = out_name or os.path.splitext(os.path.basename(transcript_path))[0]
    triplets = []

    for i, line in enumerate(lines, start=1):
        original_text = line.strip()
        filename = os.path.join(mp3_folder, f"{out_name}-{i}.mp3")

        tts_result = generate_tts(original_text, filename=filename)
        translated_text = translator.translate_text(
            original_text,
            source_lang="ru",
            target_lang="en-gb").text

        triplet = (original_text, translated_text, tts_result)
        triplets.append(triplet)

    return triplets


def main():
    elevenlabs.set_api_key(ELEVENLABS_KEY)
    logging.basicConfig(filename="logging.log", level=logging.DEBUG)
    temp_folder = os.path.join(os.getcwd(), 'TEMP-mp3')
    os.makedirs(temp_folder, exist_ok=True)
    transcript_path = 'transcript.txt'  # Replace with the path to your transcript file
    result_triplets = process_transcript(transcript_path, temp_folder)
    deck_name = "ER84"
    anki_deck = create_sound_deck(result_triplets, deck_name)
    anki_deck.write_to_file(deck_name + '.apkg')

if __name__ == "__main__":
    main()
