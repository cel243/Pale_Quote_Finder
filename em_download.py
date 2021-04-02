import requests
import bs4
import re
import os

"""
Downloads all extra materials, as best as it can, given some EMs are just
pictures. It'll get any non-picture text from the page, and I also tried
to get the transcript text that is sometimes in the comment section. This...
quite possibly will get more text than intended in many cases. I decided too much text was better than missing important things.

It does miss the transcript entirely on the Kennet Brochure EM. 
If you care about that, I guess you can get that text by hand. The
comment-section transcripts just don't follow a consistent enough rule to
identify them 100% of the time, and this code probably won't have 100%
hit rate on future EM's either, but it can always be adapted later, so there's
that.

Default behavior of this script is to go to the page that lists all the
extra materials and download them all from there. If you only want one
page, indicate that in DOWNLOAD_THIS_EM below (replace None with an EM
object).

Writes one file per extra material to ./Pale_Chapters/EM/<em_name>.txt
"""
class EM():
  def __init__(self, url, name):
    self.url = url
    self.name = name

### EDIT THIS IF YOU WANT TO DOWNLOAD ONLY ONE PAGE  #############

DOWNLOAD_THIS_EM = None #EM("<link>", "<file name>")

##################################################################

def get_em_list():
  """Returns a list of EMs, including all extra materials listed at 
  "https://palewebserial.wordpress.com/extra-material/" """
  em_page_link = "https://palewebserial.wordpress.com/extra-material/"
  em_page = requests.get(em_page_link).text
  soup = bs4.BeautifulSoup(em_page, features="html.parser")
  entry = soup.html.contents[5].contents[2].contents[4].contents[1].contents[1].contents[1].contents[4]
  ems = []
  for i in range(len(entry.contents)):
    item  = entry.contents[i]
    if type(item) == bs4.element.Tag and item.name == "p":
      spoiler_tags = re.findall("\[[0-9]+\.[0-9a-z]+\]",item.get_text())
      links = item.findChildren("a" , recursive=True)
      for j in range(len(links)):
        link = links[j]
        url = link.get("href")
        name = spoiler_tags[j] +" "+ link.get_text()
        ems.append(EM(url, name))
  return ems

def get_em_text(contents):
    """Returns any text on the page, or the empty string if it's just
    pictures."""
    text=""
    for item in contents:
        # if item.name == "p":
        if type(item) == bs4.element.Tag and item.get("id") is None:
            text+=item.get_text()+"\n\n"
    return text.strip()

def get_author_of_comment(comment):
    """Returns author of comment"""
    comment_author = comment[1].contents[1].contents[1].contents[2].get_text()
    return comment_author

def get_text_of_comment(comment):
    """Returns the text of a comment."""
    comment = comment[1].contents[3].contents
    comment_text = ""
    for i in range(len(comment)):
        item = comment[i]
        if type(item) == bs4.element.Tag and item.get("id") is None:
            comment_text += item.get_text() + "\n\n"
    return comment_text

def get_all_reply_text(comment_element):
    """Recursively gets all of the text in all the replies on this comment."""
    children = None
    try:
        children = comment_element[4].contents
    except:
        return ""
    reply_text = ""
    for i in range(len(children)):
        item = children[i]
        if type(item) == bs4.element.Tag:
            reply_text += get_text_of_comment(item.contents)
            reply_text += get_all_reply_text(item.contents)
    return reply_text

def get_transcript(comments):
    """Looks for an extra material transcript in the comment section. 
    Returns the empty string if no transcript is found."""
    for i in range(len(comments)):
        item = comments[i]
        if type(item) == bs4.element.Tag:
            comment_text = get_text_of_comment(comments[i].contents)
            comment_author = get_author_of_comment(comments[i].contents)
            if "Transcript" in comment_text or "transcript:" in comment_text.lower() or "unofficial transcript" in comment_text.lower() or "text:" in comment_text.lower() or comment_author.lower() in {"wildbow"}:
                if comment_author.lower() == "jeffery mewtamer":
                    continue
                comment_text += get_all_reply_text(comments[i].contents)
                return comment_text
    return ""

def download_em(em):
    """Goes to the url em.url, finds as much text as it can, and writes
    that text to a file."""
    em_page_text = requests.get(em.url).text
    soup = bs4.BeautifulSoup(em_page_text, features="html.parser")

    em.text = get_em_text(soup.html.contents[5].contents[2].contents[4].contents[1].contents[1].contents[4].contents[4].contents)

    em.transcript = get_transcript(soup.html.contents[5].contents[2].contents[4].contents[1].contents[1].contents[7].contents[3].contents)

    write_file(em)

def write_file(em):
    """Write extra material text to Pale_Chapters/EM/<em_name>.txt"""
    dir = 'Pale_Chapters'
    if not os.path.exists(dir):
        os.mkdir(dir)
    if not os.path.exists(f"{dir}/EM"):
        os.mkdir(f"{dir}/EM")
    with open(f"{dir}/EM/{em.name}.txt", 'w') as file:
        file.write(em.text + "\n\n~~ transcript ~~\n\n" + em.transcript)
    print(f"Wrote {em.name}")

if __name__ == "__main__":
  if DOWNLOAD_THIS_EM is not None:
    download_em(DOWNLOAD_THIS_EM)
  else:
    ems = get_em_list()
    for em in ems:
      download_em(em)
