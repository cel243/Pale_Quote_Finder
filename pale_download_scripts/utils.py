import os

pale_chapter_dir = "Pale_Chapters"
stored_data_dir = "stored_data"
download_script_dir = "pale_download_scripts"

previous_chapter_designator = ["previous chapter"]
next_chapter_designator = ["next chapter", "ex chapr"]
interlude_designator = ["interlude", "interude", "interludes", "prologue"]
main_perspective_designator = ["avery", "verona", "lucy"]
main_perspective_designator += list(map(lambda x: x + " (again)", main_perspective_designator))

ignore_false_perspective = ["now", "earlier", "after", "weird", \
                            "saturday", "before", "opening", "later", \
                            "summer", "ow"]

def skip_line(line):
  if line in (previous_chapter_designator + next_chapter_designator):
    return True
  if "last thursday:" in line:
    return True

