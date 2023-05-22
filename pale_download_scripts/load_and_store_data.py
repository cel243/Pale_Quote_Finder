import os
import pickle
import utils

#-- Available data -------------------#

# Mapping from absolute chapter number to a list of
# the perspectives that occur in this chapter, in order.
# Names may appear more than once for a singl chapter.
known_chapter_perspectives = dict()

# Mapping from chapter file name to a map of
# character names to # words for that character.
word_counts = dict()

# Mapping from chapter titles to the web link for
# that chapter.
chapter_links = dict()

path_to_known_chapter_perspectives = os.path.join(utils.download_script_dir, utils.stored_data_dir, "chapter_perspectives.pickle")
path_to_word_counts = os.path.join(utils.download_script_dir, utils.stored_data_dir, "word_counts_per_character.pickle")
path_to_chapter_links = os.path.join(utils.download_script_dir, utils.stored_data_dir, "chapter_links.pickle")

#-- Data storage ---------------------#

def write_known_chapter_perspectives():
  with open(path_to_known_chapter_perspectives, "wb") as file:
    pickle.dump(known_chapter_perspectives, file)

def write_word_counts():
  with open(path_to_word_counts, "wb") as file:
    pickle.dump(word_counts, file)

def write_chapter_links():
  with open(path_to_chapter_links, "wb") as file:
    pickle.dump(chapter_links, file)

#-- Update data ----------------------#

def add_known_chapter_perspectives(absolute_chapter_num, perspective):
  global known_chapter_perspectives
  known_chapter_perspectives[absolute_chapter_num] = perspective

def add_word_counts(absolute_chapter_num, perspectives_to_counts):
  print("Word counts by character:")
  for perspective, count in perspectives_to_counts.items():
    print(f"{perspective.capitalize()} : {count}")
  global word_counts
  word_counts[absolute_chapter_num] = perspectives_to_counts

def add_chapter_link(chapter_title, link):
  global chapter_links
  chapter_links[chapter_title] = link

#-- Load data ------------------------#

if os.path.exists(path_to_known_chapter_perspectives):
  with open(path_to_known_chapter_perspectives, "rb") as file:
    known_chapter_perspectives = pickle.load(file)

if os.path.exists(path_to_word_counts):
  with open(path_to_word_counts, "rb") as file:
    word_counts = pickle.load(file)

if os.path.exists(path_to_chapter_links):
  with open(path_to_chapter_links, "rb") as file:
    chapter_links = pickle.load(file)
