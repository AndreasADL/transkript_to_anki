""" Entry point to create anki cards"""
import random
import os
import genanki


# To be adjusted every time
TRAINING_PATH = "./German C1 Scrum"
DECK_NAME = "German C1 Scrum"
ANKI_PATH = os.path.expandvars(r"%APPDATA%/Anki2/User 1/collection.media")
CSS_STYLE = """.target {
  font-family: 'Arial';
  font-size: 26px;
  font-weight: bold;
  text-align: center;
}"""
""".native {
  font-family: 'Arial';
  font-size: 20px;
  font-style: italic;
  text-align: center;
}"""

# check https://docs.ankiweb.net/templates/styling.html#card-styling

# To be left alone
MODEL_UNDERSTAND_ID = random.randrange(1 << 30, 1 << 31)
MODEL_REPRODUCE_ID = random.randrange(1 << 30, 1 << 31)
DECK_ID = random.randrange(1 << 30, 1 << 31)
MODEL_SOUND_UNDERSTAND = genanki.Model(
  MODEL_UNDERSTAND_ID,
  'Target to Native Model with Target Media',
  fields=[
    {'name': 'Target Language'},
    {'name': 'Native Language'},
  ],
  templates=[
    {
      'name': 'Target-to-Native',
      'qfmt': '<div class="target">{{Target Language}}</div>',
      'afmt': '{{FrontSide}}<hr id="answer"><div class="native">{{Native Language}}</div>',
    }
  ],
  css=CSS_STYLE
  )
MODEL_SOUND_REPRODUCE = genanki.Model(
  MODEL_REPRODUCE_ID,
  'Native to Target Model with Target Media',
  fields=[
    {'name': 'Native Language'},
    {'name': 'Target Language'},
  ],
  templates=[
    {
      'name': 'Native-to-Target',
      'qfmt': '<div class="native">{{Native Language}}</div>',
      'afmt': '{{FrontSide}}<hr id="answer"><div class="target">{{Target Language}}</div>',
    }
  ],
  css=CSS_STYLE
  )
MODEL_TEXT_UNDERSTAND = genanki.Model(
  MODEL_UNDERSTAND_ID,
  'Target to Native Model with Target Media',
  fields=[
    {'name': 'Target Language'},
    {'name': 'Native Language'},
    {'name': 'Target Media'},
  ],
  templates=[
    {
      'name': 'Target-to-Native',
      'qfmt': '<div class="target">{{Target Language}} {{Target Media}}</div>',
      'afmt': '{{FrontSide}}<hr id="answer"><div class="native">{{Native Language}}</div>',
    }
  ],
  css=CSS_STYLE
  )
MODEL_TEXT_REPRODUCE = genanki.Model(
  MODEL_REPRODUCE_ID,
  'Native to Target Model with Target Media',
  fields=[
    {'name': 'Native Language'},
    {'name': 'Target Language'},
    {'name': 'Target Media'},
  ],
  templates=[
    {
      'name': 'Native-to-Target',
      'qfmt': '<div class="native">{{Native Language}}</div>',
      'afmt': '{{FrontSide}}<hr id="answer"><div class="target">{{Target Language}} {{Target Media}}</div>',
    }
  ],
  css=CSS_STYLE
  )


def create_sound_deck(sound_note_list, deck_name, both_ways=True):
    deck = genanki.Deck(deck_id=DECK_ID, name=deck_name)
    for target, native, sound in sound_note_list:
        new_note = genanki.Note(
        model=MODEL_SOUND_UNDERSTAND,
        fields=[target, native, f"[sound:{sound}]"])
        deck.add_note(new_note)
        if both_ways:
            new_note = genanki.Note(
                model=MODEL_SOUND_UNDERSTAND,
                fields=[target, native, f"[sound:{sound}]"])
    return genanki.Package(deck)

def create_text_deck(sound_note_list, deck_name, both_ways=True):
    deck = genanki.Deck(deck_id=DECK_ID, name=deck_name)
    for target, native in sound_note_list:
        new_note = genanki.Note(
        model=MODEL_TEXT_UNDERSTAND,
        fields=[target, native])
        deck.add_note(new_note)
        if both_ways:
            new_note = genanki.Note(
                model=MODEL_TEXT_UNDERSTAND,
                fields=[target, native])
    return genanki.Package(deck)
