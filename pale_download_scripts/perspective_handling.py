
from collections import defaultdict
import load_and_store_data as data
import utils
import re

class ChapterPerspectives():
  def __init__(self, absolute_chapter_num):
    self.img_src_to_perspective = dict()
    self.perspectives_to_word_counts = defaultdict(int)
    self.current_perspective = None

    self.absolute_chapter_num = absolute_chapter_num
    if self.absolute_chapter_num in data.known_chapter_perspectives:
      self.perspectives_are_known = True
      self.perspectives = data.known_chapter_perspectives[self.absolute_chapter_num]
      self.current_perspective = self.perspectives[0]
    else:
      self.perspectives_are_known = False
      self.perspectives = []
    self.perspective_index = -1

  def save_chapter_perspectives(self):
    data.add_known_chapter_perspectives(self.absolute_chapter_num, self.perspectives)
    data.write_known_chapter_perspectives()

  def add_word_count_to_current_perspective(self, word_count):
    self.perspectives_to_word_counts[self.current_perspective] += word_count

  def associate_img_with_perspective(self, perspective, contents, i):
    img_src = None
    potential_imgs = []
    for j in range(i-1, i+2):
      if contents[j].name == "p":
        potential_imgs += contents[j].findChildren("img", recursive=True)
    for img in potential_imgs:
      img_src = img.get("src")
    self.img_src_to_perspective[img_src] = perspective

  def print_current_perspectives_status(self, perspective_index):
    perspectives = self.perspectives[:]
    perspectives[perspective_index] = f"*{perspectives[perspective_index]}*"
    print("Perspectives: [" + ",".join(perspectives) + "]")

  def is_section_break(self, item):
    return item.name == "hr" or item.get_text().strip() == "🟂"

  def is_current_perspective(self, perspective):
    return self.perspective_index >= 0 and \
           perspective.lower() == self.perspectives[self.perspective_index]

  def print_next_paragraph(self, contents, i):
    j = i + 1
    while j < len(contents):
      if self.is_section_break(contents[j]):
        print("(section break)")
      elif (contents[j].name == "p" and
          contents[j].get_text() and
          not utils.skip_line(contents[j].get_text().lower().strip())):
        print(contents[j].get_text())
        print("[...]\n")
        break
      j += 1
    return j

  def confirm_unexpected_perspective(self, expected_perspective, actual_perspective):
    print(f"\nExpected next perspective {expected_perspective} but found {actual_perspective}.")
    print("How should this be handled?")
    print("1] Skip this perspective, keep perspective "
          f"{self.perspectives[self.perspective_index]}")
    print("2] Add this as the next perspective for this chapter")
    print(f"3] Replace expected {expected_perspective} with {actual_perspective}")
    print(f"4] Use {expected_perspective} as perspective label for next section (default)")
    print("(Enter a number) ", end="")
    response = input()
    if response == "1":
      perspective = None
    if response == "2":
      self.perspectives.insert(self.perspective_index + 1, actual_perspective.lower())
      perspective = actual_perspective
    elif response == "3":
      self.perspectives[self.perspective_index + 1] = actual_perspective
      perspective = actual_perspective
    else:
      perspective = expected_perspective
    return perspective

  def handle_new_perspective_when_perspectives_are_known(self, perspective):
    expected_next_perspective = (
      "" if self.perspective_index + 1 >= len(self.perspectives)
      else self.perspectives[self.perspective_index + 1])
    if perspective == expected_next_perspective:
      return perspective
    else:
      return self.confirm_unexpected_perspective(expected_next_perspective, perspective)

  def confirm_new_perspective(self, perspective):
    print(f"\nConfirm adding {perspective.capitalize()} as next perspective")
    print("1] Confirm adding perspective (default)")
    print("2] Skip this perspective")
    print("3] Enter a different perspective to use")
    print("(Enter a number): ", end="")
    response = input()
    if response == "2":
      return None
    elif response == "3":
      print("Perspective: ", end="")
      perspective = input()
      if self.is_current_perspective(perspective):
        print(f"Already reading from perspective {perspective}. Continuing.")
        return None
      else:
        print(f"Adding perspective {perspective}")
        self.perspectives.append(perspective.lower())
        return perspective.lower()
    else:
      self.perspectives.append(perspective)
      return perspective

  def handle_new_perspective_when_perspectives_are_unknown(self, perspective):
    if perspective in utils.main_perspective_designator:
      # No need to confirm common perspectives.
      self.perspectives.append(perspective)
      return perspective
    else:
      return self.confirm_new_perspective(perspective)

  def prompt_user_for_interlude_perspective(self, contents, i):
    print("\nFound interlude, beginning with text")
    print("-----------------------------------------")
    i = self.print_next_paragraph(contents, i)
    print("Who is this perspective? (to see another paragraph, enter 'next/n') ", end="")
    response = None
    while True:
      response = input()
      print()
      if response.lower() not in {"next", "n"}:
          break
      i = self.print_next_paragraph(contents, i)
      print("\n-- Perspective name (or 'next/n' to see more): ", end = "")
    return response.lower()

  def check_whether_text_line_indicates_new_perspective(self, line, contents, i):
    if line in utils.main_perspective_designator:
      return line.split()[0]  # Remove "(again)" if present.
    if line in utils.interlude_designator:
      if self.perspectives_are_known:
        perspective = self.perspectives[self.perspective_index + 1]
        return perspective
      else:
        return self.prompt_user_for_interlude_perspective(contents, i)
    if re.fullmatch("[a-z]+", line):
      if self.is_current_perspective(line) or \
         line in utils.ignore_false_perspective:
        return None
      if (self.perspectives_are_known and
          self.perspectives[self.perspective_index + 1] == line):
        return line
      print(f"\nThe formatting of this line seems to indicate a new perspective: {line}")
      print("Print additional lines to check the perspective? y/(default no) ", end="")
      response = input()
      if response.lower() == "y":
        print()
        i = i+1
        while True:
          i = self.print_next_paragraph(contents, i)
          print("Enter 'next/n' for more text: ", end="")
          response = input()
          if response.lower() not in {"next", "n"}:
            break
      return line

  def confirm_use_perspective_associated_with_image(self, img_src, contents, i):
    print("\nFound a new section that begins with a new image, which seems "
          f"to be associated with {self.img_src_to_perspective[img_src].capitalize()}.")
    print("Switch to this perspective? (Enter a number)")
    print("1] Confirm (Default)")
    print("2] Print a paragraph of text following the image")
    print("3] Do not shift perspectives")
    response = input()
    while True:
      if response == "3":
        return None
      if response == "2":
        while True:
          i = self.print_next_paragraph(contents, i)
          print("\nEnter a number, or 'next/n' to see more: ")
          response = input()
          if response.lower() not in {"next", "n"}:
            break
      else:
        return self.img_src_to_perspective[img_src]

  def handle_unrecognized_image(self, img_src, contents, i):
    print("\nFound a section separator followed by an image, which often "
          "indicates that the perspective has shifted. However, I don't "
          "recognize the image. Whose perspective is this?")
    print(f"Image: {img_src}")
    print("--------------------------------")
    while True:
      i = self.print_next_paragraph(contents, i)
      print("\nPerspective (or 'next/n' to see more): ", end="")
      response = input()
      if response.lower() not in {"next", "n"}:
        break
    return response.lower()

  def use_perspective_associated_with_image(self, img_src, contents, i):
    if img_src in self.img_src_to_perspective:
      perspective = self.img_src_to_perspective[img_src]
      if self.is_current_perspective(perspective):
        # No shift in perspective.
        return None
      elif (self.perspectives_are_known and
          perspective == self.perspectives[self.perspective_index + 1]):
        # No need to confirm expected perspective shift
        return self.img_src_to_perspective[img_src]
      else:
        return self.confirm_use_perspective_associated_with_image(img_src, contents, i)
    else:
      if self.perspectives_are_known:
        return self.perspectives[self.perspective_index + 1]
      else:
        return self.handle_unrecognized_image(img_src, contents, i)

  def handle_img_perspective_change(self, img_src, contents, i):
    for j in range(i-1, i+2):
      # Check whether the previous or next line indicates perspective.
      item_text = contents[j].get_text().strip().lower()
      if item_text:
        line_perspective_indicator = \
          self.check_whether_text_line_indicates_new_perspective(item_text, contents, i)
        if line_perspective_indicator:
          return line_perspective_indicator
    # Fall back on stored image/character associations
    return self.use_perspective_associated_with_image(img_src, contents, i)

  def check_for_new_perspective(self, contents, i):
    line = contents[i].get_text().strip()
    if line:
      return self.check_whether_text_line_indicates_new_perspective(line.lower(), contents, i)
    else:
      img_src = contents[i].findChildren("img", recursive=True)
      if img_src:
        img_src = img_src[0].get("src")
        if self.is_section_break(contents[i-1]) or self.is_section_break(contents[i-2]):
          return self.handle_img_perspective_change(img_src, contents, i)

  def handle_potential_new_perspective(self, contents, i):
    new_perspective = self.check_for_new_perspective(contents, i)
    if new_perspective:
      if self.perspectives_are_known:
        new_perspective = self.handle_new_perspective_when_perspectives_are_known(new_perspective)
      else:
        new_perspective = self.handle_new_perspective_when_perspectives_are_unknown(new_perspective)
    if new_perspective:
      self.associate_img_with_perspective(new_perspective, contents, i)
      self.current_perspective = new_perspective
      self.perspective_index += 1

  def handle_no_perspectives_found(self, contents):
    if self.perspectives_are_known:
      self.current_perspective = self.perspectives[0]
      self.perspective_index = 0
    else:
      print("\nBegan reading chapter but no perspective was found...")
      print("Do you know whose perspective this chapter is from?")
      print("Enter perspective, or 'print/p' to print paragraphs from this chapter: ", end="")
      response = input()
      i = 0
      while True:
        if response not in {"print", "p"}:
          break
        i = self.print_next_paragraph(contents, i)
        print("Perspective, or print/p for more: ", end="")
        response = input()
      self.perspectives.append(response.lower())
      self.current_perspective = response.lower()
      self.perspective_index = 0
