import requests
import bs4
import re
import os
import sys

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

if len(sys.argv)<2:
    START_LINK = "https://palewebserial.wordpress.com/2020/05/05/blood-run-cold-0-0/"
else:
    START_LINK = sys.argv[1]

class Chapter():
  def __init__(self, url):
    self.url = url

def get_next_link(entry_contents):
    """Returns the link to the next chapter, or None if there is no next
    chapter. Also returns the remainder of the page's contents after the
    first occurrence of the 'Next Chapter' link. """
    for i in range(len(entry_contents)):
        item = entry_contents[i]
        if type(item) == bs4.element.Tag:
            for child in item.findChildren("a" , recursive=True):
                if child.get_text().strip() == "Next Chapter":
                    return child.get("href"), entry_contents[i+1:]
    return None, entry_contents

def get_header(entry_contents):
    """Returns the perspective of this chapter (e.g. 'Interlude', 'Lucy').
    If no perspective is found, returns an empty string. Also returns
    the remainder of the page's contents after the perspective is found.
    """
    for i in range(len(entry_contents)):
        item = entry_contents[i]
        if item.name == "h1":
            return item.get_text().strip(), entry_contents[i+1:]
        elif item.name == "p":
            if "Avery" in item.get_text().strip() \
                or "Lucy" in item.get_text().strip() \
                or "Verona" in item.get_text().strip() \
                or "Interlude" in item.get_text().strip():
                return item.get_text().strip(), entry_contents[i+1:]
    return "", entry_contents

def get_chapter_text(entry_contents):
    """Returns the text of the chapter. Stylistics markings like itallics
    won't be encoded. There may be some leading or trailing new line
    characters. """
    text=""
    for item in entry_contents:
        if item.name == "p":
            if item.get_text().strip() in {"Next Chapter","Previous Chapter"}\
                or "Last Thursday" in item.get_text():
                continue
            else:
                text+=item.get_text()+"\n\n"
    return text.replace('’', "'").replace("”", '"').replace("“", '"')

def download_this_chapter(chapter, page_text):
    """Given the raw html of the chapter page, populates the 
    `chapter` passed in with the chapter's title, perspective, the link
    of the next chapter, and the text of the chapter. Returns nothing
    but modifies `chapter`. """
    soup = bs4.BeautifulSoup(page_text, features="html.parser")
    chapter.title = re.sub("[^A-Za-z\.0-9\ ]","",soup.title.get_text().split("|")[0]).strip().replace("  "," ")
    chapter.arc = re.findall("[0-9]+.", chapter.title)[0][:-1]
    if len(chapter.arc) < 2:
        chapter.arc = "0"+chapter.arc
    
    entry = soup.html.contents[5].contents[2].contents[4].contents[1].contents[1].contents[4].contents[4]
    chapter.perspective, entry_contents = get_header(entry.contents)
    chapter.next_link, entry_contents = get_next_link(entry_contents)
    chapter.chapter_text = get_chapter_text(entry_contents)

def write_file(chapter):
    """Write chapter to Pale_Chapters/"""
    dir = 'Pale_Chapters'
    if not os.path.exists(dir):
        os.mkdir(dir)
    if not os.path.exists(f"{dir}{os.path.sep}{chapter.arc}"):
        os.mkdir(f"{dir}{os.path.sep}{chapter.arc}")
    chap_num_str = str(chapter.chap_num)
    if chapter.chap_num < 100:
        chap_num_str = "0" + chap_num_str
    if chapter.chap_num < 10:
        chap_num_str = "0" + chap_num_str
    with open(f"{dir}{os.path.sep}{chapter.arc}{os.path.sep}({chap_num_str}) {chapter.title} ({chapter.perspective}).txt", 'w') as file:
        file.write(chapter.chapter_text)

def get_previous_chap_num(page_text):
    """  """
    soup = bs4.BeautifulSoup(page_text, features="html.parser")
    entry = soup.html.contents[5].contents[2].contents[4].contents[1].contents[1].contents[4].contents[4]
    entry_contents = entry.contents

    link = None
    for i in range(len(entry_contents)):
        item = entry_contents[i]
        if type(item) == bs4.element.Tag:
            for child in item.findChildren("a" , recursive=True):
                if child.get_text().strip() == "Previous Chapter":
                    link =  child.get("href")
    if link is None:
        return 1

    resp = requests.get(link)
    page_text = resp.text
    soup = bs4.BeautifulSoup(page_text, features="html.parser")
    title = re.sub("[^A-Za-z\.0-9\ ]","",soup.title.get_text().split("|")[0]).strip().replace("  "," ")
    arc = re.findall("[0-9]+.", title)[0][:-1]
    if len(arc) < 2:
        arc = "0"+arc
    if not os.path.exists(f"Pale_Chapters{os.path.sep}{arc}"):
        return 1
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
            chap_num = get_previous_chap_num(page_text)
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
