import requests
import bs4
import re
import os
import sys
import pickle

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

Interludes are only marked with the actual character perspective if the 
Interlude has been added to INTERLUDE_PERSPECTIVES below.
"""

# Instantiate script argument values #######################################

CURRENT_INTERLUDE_PERSPECTIVE = None
START_LINK = None
if len(sys.argv)<2:
    START_LINK = "https://palewebserial.wordpress.com/2020/05/05/blood-run-cold-0-0/"
else:
    START_LINK = sys.argv[1]
    if len(sys.argv) > 2:
        # If this is an interlude, the perspective will have (hopefully)
        # been passed in as an argument to the script. 
        CURRENT_INTERLUDE_PERSPECTIVE = sys.argv[2]

#-----------------------------------------------------------------------------#

# Load mapping of interludes to perspectives ##################################

with open("interlude_perspectives.pickle", "rb") as file:
    INTERLUDE_PERSPECTIVES = pickle.load(file)

#-----------------------------------------------------------------------------#

# Definitions ##############################################################

class Chapter():
  def __init__(self, url):
    self.url = url

#-----------------------------------------------------------------------------#

def get_next_link(entry_contents):
    """Returns the link to the next chapter, or None if there is no next
    chapter. Also returns the remainder of the page's contents after the
    first occurrence of the 'Next Chapter' link. """
    for i in range(len(entry_contents)):
        item = entry_contents[i]
        if type(item) == bs4.element.Tag:
            for child in item.findChildren("a" , recursive=True):
                if child.get_text().strip() in {"Next Chapter", "ex Chapr"}:
                    return child.get("href"), entry_contents[i+1:]
    return None, entry_contents

def handle_interlude_perspective(chap_title, perspective):
    """Returns 'Interlude - [perspective of this chapter]'. 
    This function should only be called on interlude chapters."""
    if perspective == "Interude":
        # Fix Cherry's spelling.
        perspective = "Interlude - Cherrypop"
    else:
        if chap_title in INTERLUDE_PERSPECTIVES:
            perspective = "Interlude - " + INTERLUDE_PERSPECTIVES[chap_title]
        else:
            # We do not already know the perspective of this interlude and must either request it from the user, or store the perspective provided by the user.
            if CURRENT_INTERLUDE_PERSPECTIVE is not None:
                perspective = "Interlude - " + CURRENT_INTERLUDE_PERSPECTIVE
                INTERLUDE_PERSPECTIVES[chap_title] = CURRENT_INTERLUDE_PERSPECTIVE
                with open('interlude_perspectives.pickle', 'wb') as file:
                    pickle.dump(INTERLUDE_PERSPECTIVES, file)
            else:
                perspective = "Interlude - ??"
                print("*************** WARNING ******************\n\nThere is no interlude perspective specified yet for "+chap_title+". Please pass in the interlude perspective of this chapter as the second argument to the script, after the chapter link, and the perspective will be saved for future use.\n\n******************************************")
    return perspective

def get_header(entry_contents, chap_title):
    """Returns the perspective of this chapter (e.g. 'Lucy').
    If no perspective is found, returns an empty string. Also returns
    the remainder of the page's contents after the perspective is found.
    For Interludes, returns 'Interlude - <character>'
    'Break' chapters should not call this function.
    """
    perspective = None
    remainder = entry_contents
    for i in range(len(entry_contents)):
        item = entry_contents[i]
        # Sometimes perspective headers are <h1> elements, and sometimes they're
        # <p> elements. <h1> elements are always perspective markers.
        if item.name == "h1":
            if perspective is None:
                perspective =  item.get_text().strip()
                remainder = entry_contents[i+1:]
            else:
                # Multiple perspectives found.
                return "All", remainder
        elif item.name == "p":
            if item.get_text().strip().lower() == "nora":
                return "Avery-Nora",remainder
            if item.get_text().strip().lower() in {"interlude", "interludes", "interude"}:
                # This is an interlude
                perspective = handle_interlude_perspective(chap_title, perspective)
                remainder = entry_contents[i+1:]
                return perspective, remainder
            if item.get_text().strip().lower() in {"avery", "verona", "lucy", 
                "avery (again)", "verona (again)", "lucy (again)", "prologue"}:
                if perspective is None:
                    perspective = item.get_text().strip()
                    remainder = entry_contents[i+1:]
                else:
                    # Multiple perspectives found.
                    return "All", remainder
    return perspective, remainder

def get_chapter_text(entry_contents):
    """Returns the text of the chapter. Stylistics markings like itallics
    won't be encoded. There may be some leading or trailing new line
    characters. """
    text=""
    for item in entry_contents:
        if item.name == "p":
            if item.get_text().strip() in {"Next Chapter", "Nex Chapr", 
                "Next Chaptr", "Previs Chaptr", "Previus Chaptir", 
                "Previous Chapter"}\
                or "Last Thursday" in item.get_text():
                # The next/previous chapter links are paragraphs on the page,
                # but should not be included in the chapter text.
                continue
            else:
                # Otherwise, append this text.
                text+=item.get_text()+"\n\n"
    # Fix special curly quotes before returning because they make searching
    # hard.
    return text.replace('’', "'").replace("”", '"').replace("“", '"')

def download_this_chapter(chapter, page_text):
    """Given the raw html of the chapter page, populates the 
    `chapter` passed in with the chapter's title, perspective, the link
    of the next chapter, and the text of the chapter. Returns nothing
    but modifies `chapter`. """
    soup = bs4.BeautifulSoup(page_text, features="html.parser")
    if "12a" in soup.title.get_text():
        # Fix Cherry's spelling.
        chapter.title = "False Moves 12.a"
    else:
        # Normal page title looks like "Lost For Word 1.3 | Pale". 
        # Get the part before the "|" and remove any special characters.
        chapter.title = re.sub("[^A-Za-z\.0-9\ ]","",soup.title.get_text()
                          .split("|")[0]).strip().replace("  "," ")

        # Check if this is a 'Break' chapter, and apply a special naming
        # rule if so. Otherwise, the chapter title is just the title
        # of the page (e.g. 'Summer Break 13.4')
        if len(re.findall("^Break [0-9]+$", chapter.title)) > 0:
            break_num = re.findall("[0-9]+$", chapter.title)[0]
            chapter.title = f"Summer Break 13.B{break_num}"
        elif chapter.title == "Summer Break":
            chapter.title = f"Summer Break 13.SB"
    
    # If the chapter arc is less than 2 characters, it's necessary to pad
    # the number with a 0 so the length is consistent.
    chapter.arc = re.findall("[0-9]+\.", chapter.title)[0][:-1]

    if len(chapter.arc) < 2:
        chapter.arc = "0"+chapter.arc
    
    entry_contents = soup.html.contents[5].contents[10].contents[4].contents[1].contents[1].contents[4].contents[4].contents

    # Populate chapter perspective, nex link, and chapter text.
    # 'Break' chapters get a special perspective rule.
    if "13.B" in chapter.title:
        break_chap_name = re.findall("B[0-9]+", chapter.title)[0]
        chapter.perspective = handle_interlude_perspective(break_chap_name, "")
    elif "SB" in chapter.title:
        chapter.perspective = "All-Jas"
    else:
        chapter.perspective, entry_contents = get_header(entry_contents, chapter.title)

    chapter.next_link, entry_contents = get_next_link(entry_contents)
    chapter.chapter_text = get_chapter_text(entry_contents)

def write_file(chapter):
    """Write chapter to Pale_Chapters/"""
    # Step 1: Create directory if it doesn't exist.
    dir = 'Pale_Chapters'
    if not os.path.exists(dir):
        os.mkdir(dir)
    if not os.path.exists(f"{dir}{os.path.sep}{chapter.arc}"):
        os.mkdir(f"{dir}{os.path.sep}{chapter.arc}")
    
    # Step 2: Pad chapter number to 3 characters.
    chap_num_str = str(chapter.chap_num)
    if chapter.chap_num < 100:
        chap_num_str = "0" + chap_num_str
    if chapter.chap_num < 10:
        chap_num_str = "0" + chap_num_str
    
    # Step 3: Write chapter contents.
    with open(f"{dir}{os.path.sep}{chapter.arc}{os.path.sep}({chap_num_str}) {chapter.title} ({chapter.perspective}).txt", 'w') as file:
        file.write(chapter.chapter_text)

def get_chap_num_from_context(page_text):
    """ Investigates the previous chapter to find its title, and looks
    for that chapter in the Pale_Chapters/ directory. If found, the
    chapter number of this chapter is 1 + the chapter number of the 
    previous chapter. If not found, the default assumption is that this is
    chapter one. """
    soup = bs4.BeautifulSoup(page_text, features="html.parser")
    entry = soup.html.contents[5].contents[10].contents[4].contents[1].contents[1].contents[4].contents[4]
    entry_contents = entry.contents
    
    # First, get the link to the previous chapter.
    link = None
    for i in range(len(entry_contents)):
        item = entry_contents[i]
        if type(item) == bs4.element.Tag:
            for child in item.findChildren("a" , recursive=True):
                if child.get_text().strip() in {"Previous Chapter", 
                                                "Previs Chaptr"}:
                    link =  child.get("href")
    if link is None:
        return 1 #this is chapter 1 since there's no previous chapter link

    # Parse the page text for the previous chapter to find the title
    # of that chapter (e.g. Lost For Words 1.3)
    resp = requests.get(link)
    page_text = resp.text
    soup = bs4.BeautifulSoup(page_text, features="html.parser")
    title = re.sub("[^A-Za-z\.0-9\ ]","",soup.title.get_text()
                          .split("|")[0]).strip().replace("  "," ")
    if "12a" in title:
        # Title changed or else this chapter will not be recognized in the
        # file system.
        title = "False Moves 12.a"
    elif "12.a" in title:
        # Hard-coded because the duplicate 12.a causes 12.8 to be mis-numbered.
        return 127
    elif len(re.findall("^Break [0-9]+$", title)) > 0:
        # Break chapter special case
        break_num = re.findall("[0-9]+$", title)[0]
        title = f"Summer Break 13.B{break_num}"

    # Since I'll be looking in a particular arc directory, I need to pad the
    # arc number with a 0 if it's < 10
    arc = re.findall("[0-9]+.", title)[0][:-1]
    if len(arc) < 2:
        arc = "0"+arc

    # look for the previous chapter in the file system and find its
    # chapter number to get the number of this chapter.
    if not os.path.exists(f"Pale_Chapters{os.path.sep}{arc}"):
        return 1 # no context found
    for filename in os.listdir(f"Pale_Chapters{os.path.sep}{arc}"):
        if title in filename:
            return int(filename.split(" ")[0].replace("(","").replace(")","")) + 1

def download_chapters(url):
    """Retrieve and write all Pale chapters starting at `url`."""
    start = True
    chap_num = None
    while url is not None:
        chapter = Chapter(url)
        resp = requests.get(url)
        page_text = resp.text
        if start:
            chap_num = get_chap_num_from_context(page_text)
            start = False
        chapter.chap_num = chap_num
        download_this_chapter(chapter, page_text)
        write_file(chapter)
        url = chapter.next_link
        chap_num += 1
        print("wrote " + chapter.title)
        # break

if __name__ == "__main__":
  download_chapters(START_LINK)
