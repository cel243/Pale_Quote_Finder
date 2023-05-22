import os
import sys
import pale_chapter
import utils
import load_and_store_data as data

"""
Downloads ALL chapters of Pale (none of the extra materials) and stores the 
raw text of the chapters in txt files, in a directory "Pale_Chapters/", created 
in the same directory the script is run in. Each arc of Pale gets its own 
subdirectory,

Chapter download begins with Blood Run Cold 0.0, but if you want to start later
you can pass in a start link as an argument to the process. 

  EX: If you want to download ONLY the most recent chapter, run 
    `python get_text.py <link_to_chapter>`

  If you only want one specific chapter, that isn't the most recent one, 
  just add a break statement at the end of the while loop in
  download_chapters().
"""

#-- Instantiation ------------------------------------------------------------------#

START_LINK = "https://palewebserial.wordpress.com/2020/05/05/blood-run-cold-0-0/"
MAN_CHAPTER_NUM_OVERRIDE = None

if len(sys.argv) > 1:
  START_LINK = sys.argv[1]
if len(sys.argv) > 2:
  MAN_CHAPTER_NUM_OVERRIDE = sys.argv[2]

#-----------------------------------------------------------------------------------#

def write_chapter(chapter):
  if not os.path.exists(utils.pale_chapter_dir):
    os.mkdir(utils.pale_chapter_dir)
  path_to_arc = os.path.join(utils.pale_chapter_dir, chapter.padded_arc_num)
  if not os.path.exists(path_to_arc):
    os.mkdir(path_to_arc)
  
  full_path = os.path.join(path_to_arc, f"{chapter.get_chapter_file_name()}.txt")
  with open(full_path, 'w') as file:
    file.write(chapter.chapter_text)

  data.add_chapter_link(chapter.chapter_title, chapter.url)
  data.write_chapter_links()

def download_chapters(url):
  """Retrieve and write all Pale chapters, starting at `url`."""
  chapter = None
  manual_chapter_num_override=MAN_CHAPTER_NUM_OVERRIDE
  while url is not None:
    print("\n-----------------------------------")
    print(url)
    chapter = \
      pale_chapter.Chapter(url, get_full_data=True, \
                           previous_chapter=chapter, \
                           manual_chapter_num_override=manual_chapter_num_override)
    manual_chapter_num_override = None
    url = chapter.next_chapter_link
    write_chapter(chapter)
    print(f"Wrote {chapter.get_chapter_file_name()}")
    break

if __name__ == "__main__":
  download_chapters(START_LINK)
