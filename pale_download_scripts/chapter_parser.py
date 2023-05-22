import bs4
import utils
import re
from collections import defaultdict
import os
import load_and_store_data as data
import perspective_handling

class ChapterParser():
  def __init__(self, raw_page_html):
    self.page_soup = bs4.BeautifulSoup(raw_page_html, features="html.parser")
    self.main_page_contents = self.get_main_page_contents()

  def set_absolute_chapter_num(self, absolute_chapter_num):
    """
    In addition to setting the absolute chapter number for
    this chapter, creates an object that tracks how perspectives
    change throughout the chapter.
    """
    self.absolute_chapter_num = absolute_chapter_num
    self.perspective_handler = perspective_handling.ChapterPerspectives(absolute_chapter_num)

  def get_main_page_contents(self):
    """
    Gets the soup for the portion of the chapter page containing
    the 'main' contents (e.g. title, header photo, chapter text, etc).
    """
    main_contents = self.page_soup.html.find_all("div", {"class": "entry-content"})
    return main_contents[0].contents

  def find_previous_chapter_link(self):
    """
    Returns the link attached to "Previous Chapter" (or equivalent),
    if found.
    """
    for child_link in self.page_soup.findChildren("a", recursive=True):
      if child_link.get_text().strip().lower() in utils.previous_chapter_designator:
          return child_link.get("href")

  def find_next_chapter_link(self):
    """
    Returns the link attached to "Next Chapter" (or equivalent),
    if found.
    """
    for child_link in self.page_soup.findChildren("a", recursive=True):
      if child_link.get_text().strip().lower() in utils.next_chapter_designator:
          return child_link.get("href")

  #--- Chapter title information ----------------------------------#
  # Page title has form "[Arc Name] - [Arc Num].[Chap Num] | Pale"
  # (Exceptions include Cherrypop's interlude and Break chapters)

  def get_arc_name(self):
    title = self.page_soup.title.get_text()
    if re.search("break [0-9]", title.lower()):
      return "Summer Break"
    return re.findall("[A-Za-z ]+", title)[0].strip()

  def get_arc_and_chapter_num(self):
    title = self.page_soup.title.get_text()
    if "12a" in title:  # Cherrypop's interlude has separate formatting.
      return 12, "a"
    elif re.search("break [0-9]", title.lower()):
      break_num = re.findall("[0-9]+", title)[0]
      return 13, f"B{break_num}"
    elif (self.get_arc_name() == "Summer Break" and
          not re.search("[0-9]", title)):
      return 13, "SB"
    else:
      arc_num = re.findall("([0-9]+)\.", self.page_soup.title.get_text())[0]
      relative_chap_num = re.findall("\.([0-9a-z]+)", self.page_soup.title.get_text())[0]
      return arc_num, relative_chap_num

  #----------------------------------------------------------------#

  def process_chapter_text(self):
    """
    Returns the text of the chapter. Stylistics markings like itallics
    won't be encoded. There may be some leading or trailing new line
    characters.

    Headers, or lines, that seem to indicate new perspectives, trigger
    perspective handling routines.

    Certain lines are not written (e.g. 'Next Chapter').
    """
    text=""
    contents = list(filter(lambda x: x.name is not None, self.main_page_contents))
    for i in range(len(contents)):
      item = contents[i]
      line = item.get_text().strip()
      if line and not utils.skip_line(line.lower()):
        self.perspective_handler.handle_potential_new_perspective(contents, i)
        line.replace('’', "'").replace("”", '"').replace("“", '"')
        text += line+"\n\n"
        self.perspective_handler.add_word_count_to_current_perspective(len(line.split()))
      elif contents[i].name == "p" and contents[i].findChildren("img", recursive=True):
        self.perspective_handler.handle_potential_new_perspective(contents, i)

      if self.perspective_handler.current_perspective is None:
        self.perspective_handler.handle_no_perspectives_found(contents)

    self.perspective_handler.save_chapter_perspectives()

    return text, \
           self.perspective_handler.perspectives, \
           self.perspective_handler.perspectives_to_word_counts
