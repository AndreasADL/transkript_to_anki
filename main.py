# System imports
import os
import logging
# Library imports
import deepl
from dotenv import load_dotenv
from gtts import gTTS
# Local imports
from anki_functions import create_sound_deck


load_dotenv() # passes values from local .env file to os
DEEPL_KEY = os.environ["DEEPL_KEY"]
ELEVENLABS_KEY = os.environ["ELEVENLABS_KEY"]
ANKI_PATH = os.path.expandvars(r"%APPDATA%/Anki2/User 1/collection.media")

# Read in the transcript file
def generate_tts(text, language='ru', filename='output.mp3'):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(filename)
    filename = os.path.basename(filename)
    return filename

def process_transcript(transcript_path, mp3_folder=os.getcwd()):
    with open(transcript_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    translator = deepl.Translator(DEEPL_KEY)

    triplets = []

    for i, line in enumerate(lines, start=1):
        original_text = line.strip()
        filename = transcript_path.split(".")[0]
        filename = os.path.join(mp3_folder, f"{filename}{i}.mp3")

        tts_result = generate_tts(original_text, filename=filename)
        translated_text = translator.translate_text(
            original_text,
            source_lang="ru",
            target_lang="en-gb").text

        triplet = (original_text, tts_result, translated_text)
        triplets.append(triplet)

    return triplets


def main():
    logging.basicConfig(filename="logging.log", level=logging.DEBUG)
    temp_folder = os.path.join(os.getcwd(), 'TEMP-mp3')
    os.makedirs(temp_folder, exist_ok=True)
    transcript_path = 'transcript.txt'  # Replace with the path to your transcript file
    result_triplets = process_transcript(transcript_path, temp_folder)
    deck_name = "ER84"
    anki_deck = create_sound_deck(result_triplets, deck_name)
    anki_deck.write_to_file(deck_name + '.apkg')

    # clean up temp_folder
    for file_name in os.listdir(temp_folder):
        destination = os.path.join(ANKI_PATH, file_name)
        try:
            os.rename(file_name, destination)
            logging.debug("The file has been moved to %s.", destination)
        except OSError as e:
            logging.error("Error: %s", e)

    try:
        os.rmdir(temp_folder)
        logging.debug("The folder %s has been deleted.", temp_folder)
    except OSError as e:
        logging.error("Error: %s", e)

    for triplet in result_triplets:
        original, tts_filename, translated_text = triplet
        logging.debug("Original: %s\nTTS File: %s\nTranslated: %s\n",
                     original, tts_filename, translated_text)

if __name__ == "__main__":
    main()
