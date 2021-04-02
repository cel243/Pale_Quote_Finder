import requests
import bs4
import re
import os

"""
Downloads all chapters of Pale (none of the extra materials) and stores the 
raw text of the chapters in txt files labelled "Arc Name x.x (Perspective)" 
(ex: "Back Away 5.1 (Lucy).txt"), in a directory "Pale_Chapters/", created in 
the same directory the script is run in. Each arc of Pale gets its own 
subdirectory,

Chapter download begins with Blood Run Cold 0.0, but if you want to start later
you can replace the link below.
"""

START_LINK = "https://palewebserial.wordpress.com/2020/05/05/blood-run-cold-0-0/"

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
            # if "🟂" == item.get_text().strip():
            #     text += "~\n\n"
            else:
                text+=item.get_text()+"\n\n"
    return text

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
    if not os.path.exists(f"{dir}/{chapter.arc}"):
        os.mkdir(f"{dir}/{chapter.arc}")
    with open(f"{dir}/{chapter.arc}/{chapter.title} ({chapter.perspective}).txt", 'w') as file:
        file.write(chapter.chapter_text)

def download_chapters(url):
    """Retrieve and write all Pale chapters starting at `url`."""
    while url is not None:
        chapter = Chapter(url)
        resp = requests.get(url)
        page_text = resp.text
        download_this_chapter(chapter, page_text)
        write_file(chapter)
        url = chapter.next_link
        print("wrote " + chapter.title)

if __name__ == "__main__":
  download_chapters(START_LINK)
