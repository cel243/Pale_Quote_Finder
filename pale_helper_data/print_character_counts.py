import os
import pickle


path_to_word_counts = \
  os.path.join("pale_download_scripts", \
               "stored_data", "word_counts_per_character.pickle")

with open(path_to_word_counts, "rb") as file:
  word_counts = pickle.load(file)

for chapter, counts in word_counts.items():
  print(chapter, end="-")
  for character, words in counts.items():  
    print(f"{character},{words}", end=";")
  print()

# with open(path_to_word_counts, "wb") as file:
#   pickle.dump(word_counts, file)
