import requests
import chapter_parser
import os
import utils
import re
import load_and_store_data as data

class Chapter():
  def __init__(self, url, get_full_data=True, previous_chapter=None, manual_chapter_num_override=None):
    self.parser = chapter_parser.ChapterParser(requests.get(url).text)

    self.url = url

    self.arc_name = self.parser.get_arc_name()
    self.arc_num, self.relative_chapter_num = self.parser.get_arc_and_chapter_num()

    self.chapter_title = f"{self.arc_name} {self.arc_num}.{self.relative_chapter_num}"

    self.padded_arc_num = str(self.arc_num).zfill(2)

    if get_full_data:
      self.absolute_chapter_num = (
          manual_chapter_num_override if manual_chapter_num_override is not None 
          else previous_chapter.absolute_chapter_num + 1 if previous_chapter is not None
          else self.get_chap_num_from_context())
      self.padded_absolute_chapter_num = str(self.absolute_chapter_num).zfill(3)
      self.parser.set_absolute_chapter_num(self.absolute_chapter_num)

      print(f"Reading chapter {self.chapter_title}...")
      self.chapter_text, self.perspectives, perspectives_to_word_counts = \
          self.parser.process_chapter_text()
      self.perspectives = set(map(lambda x: x.title(), self.perspectives))
      self.next_chapter_link = self.parser.find_next_chapter_link()
      data.add_word_counts(self.get_chapter_file_name(), perspectives_to_word_counts)
      data.write_word_counts()

  def get_chapter_file_name(self):
    return (f"({self.padded_absolute_chapter_num}) " + 
            f"{self.chapter_title} "
            f"({'-'.join(self.perspectives)})")

  def get_chap_num_from_context(self):
    """
    Uses the "previous chapter" link to find the title of the previous chapter,
    then searches the Pale_Chapters/ directory to try to find the chapter
    number N of that chapter. If found, returns N + 1. 

    If no previous chapter is found, returns 1.
    """
    previous_chapter_link = self.parser.find_previous_chapter_link()
    if previous_chapter_link is None:
      return 1  # No chapter context found

    previous_chapter = Chapter(previous_chapter_link, get_full_data=False)

    previous_chapter_dir = os.path.join(utils.pale_chapter_dir, previous_chapter.padded_arc_num)
    if not os.path.exists(previous_chapter_dir):
      return 1  # No chapter context found

    for filename in os.listdir(previous_chapter_dir):
      if previous_chapter.chapter_title in filename:
        absolute_chap_num_str = re.findall("^\(([0-9]+)\)", filename)[0]
        return int(absolute_chap_num_str) + 1

    return 1  # No chapter context found


