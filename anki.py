from diki_translate import Diki
from babla_translate import Babla
from gtts import gTTS
import genanki
import pandas as pd
import eng_to_ipa as p
import contextlib
import random
import datetime
import argparse
import itertools
import os
import shutil


#adds note to deck
def noteAdder(note_word, phonetic, phonetic_media, meaning, example):
  with contextlib.suppress(TypeError):
    my_note = genanki.Note(
    model=my_model,
    fields=[note_word, phonetic, "[sound:"+ phonetic_media[6:] +"]", meaning, example])
    my_deck.add_note(my_note)
  
  
#generates tts from word
def ttsAdder(word):
  with contextlib.suppress(AssertionError):
    tts = gTTS(word, lang='en')
    tts_word = f"media/{str(word_index)}_" + word[:3] + ".mp3"
    tts.save(tts_word)
    my_package.media_files.append(tts_word)
    return tts_word
  
  
#generates meaning, example and phonetic of word
def meaningAdder(word):
  diki_list = list(itertools.islice(diki.translation(word), 5))
  babla_list = list(itertools.islice(babla.translation(word), 5))


  num = [len(diki_list), len(babla_list)]
  meaning_index = max(num)
  trans_list = []

  for i in range(meaning_index):
    with contextlib.suppress(IndexError):
        trans_list.append(diki_list[i])    

    with contextlib.suppress(IndexError):
        trans_list.append(babla_list[i])    


  uniqueList = []
  duplicateList = []
  
  for i in trans_list:
      if i not in uniqueList:
          uniqueList.append(i)
      elif i not in duplicateList:
          duplicateList.append(i)  


  if uniqueList:
    meaning_string = ', '.join(uniqueList[:5])
  else:
    meaning_string = " "


  dataset.at[word_index,'meaning'] = meaning_string
  dataset.at[word_index,'phonetic'] = p.convert(word)


  example = list(itertools.islice(babla.example(word), 1))
  with contextlib.suppress(IndexError):
    if example:
      dataset.at[word_index,'example'] = example[0]
    else:
      example = " "
      dataset.at[word_index,'example'] = example


  print(dataset.at[word_index,'phonetic'])
  print(dataset.at[word_index,'meaning'])
  print(dataset.at[word_index,'example'])



#cli and pd init
parser = argparse.ArgumentParser(description='English <-> Polish anki generator')
parser.add_argument('file')
args = parser.parse_args()
columns = ['word_column', 'phonetic', 'meaning', 'example']
dataset=pd.read_csv(args.file,header=None, index_col=False,names=columns,sep='\t',dtype=object)


# diki and babla module init
diki = Diki("english")
babla = Babla("english", "polish")


#genanki card model 
my_model = genanki.Model(
  random.randrange(1 << 30, 1 << 31),
  'Translation_model',
  fields=[
    {'name': 'word'},
    {'name': 'phonetic'},
    {'name': 'phonetic_media'},
    {'name': 'meaning'},
    {'name': 'example'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{word}} <br> {{phonetic}} \t {{phonetic_media}}',

      'afmt': '{{FrontSide}}<hr id="answer">{{meaning}} <br><br> {{example}}',
    },
  ],
  css='.card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n',
  )

#creates media folder to store tts and checks if it exist
try:
  folder_path = 'media'
  os.mkdir(folder_path)
  print('Media folder created')
except Exception:
  print('Media folder already exists')
  
  
current_day = datetime.datetime.now()
title = f'Translation_{str(current_day.strftime("%d.%m"))}'


my_deck = genanki.Deck(random.randrange(1 << 30, 1 << 31),title)
my_package = genanki.Package(my_deck)
my_package.media_files = []
not_translated = []


#main loop
for word_index in range(len(dataset)):
    current_word = dataset._get_value(word_index,'word_column')
    print(word_index, current_word)
    meaningAdder(current_word)

    if dataset.at[word_index,'meaning'] == " ":
      not_translated.append(current_word)
      dataset = dataset.drop(word_index)
    else:
      noteAdder(dataset.at[word_index,'word_column'],dataset.at[word_index,'phonetic'], ttsAdder(current_word),dataset.at[word_index,'meaning'], dataset.at[word_index,'example'])


#export
print(dataset)
dataset.to_csv(title + '.csv',index=False)
my_package.write_to_file(title + '.apkg')


#removes media folder
try:
  shutil.rmtree(folder_path)
  print('Media folder and its content removed')
except Exception:
  print('Media folder not deleted')
print(f"Words not translated : {not_translated}")