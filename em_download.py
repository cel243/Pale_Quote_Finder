import requests
import bs4
import re
import os
import sys

"""
Downloads all extra materials.

It'll get any non-picture text from the page, along with the transcripts often 
provided in the comment sections. 

Some notes on the comment-section transcript:

  - I sometimes gets a bit more text than intended, since sometimes a 
    transcript will have extra text in the comment containing the 
    transcript. It's never a ton of extra text, though. 

  - I have a general rule that looks for comment section transcripts, 
    AND I handle the special cases that arise. Default behavior: if it finds
    a parent comment contaiing the desired keywords, it will download
    just that parent comment. 
    However, there are chapters where this doesn't work (ex: transcript 
    continues in the comment replies), and I use EXCEPTION_MAPPING below to 
    tell the script how to find those transcripts. Detailed instructions are 
    in those code comments. 

  - In the event that general rule I use fails on a future EM, just add that
    special case to the exception mapping below, manually. 

Default behavior of this script is to go to the page that lists all the
extra materials and download ALL EMs from there. If you only want only one
EM, pass as an argument to the script the chapter number for which this EM is
spoilers for. 

    EX: To download ONLY the borrowed eyes comic, run 
      `python em_download.py '7.3'`
      
    Sometimes it takes a few days for the EM to be added to the main EM page
    that links all the extra materials (which is where I go to look for the
    EM). If the script can't find the EM you're trying to download, that's
    probably why. 

    If you really want a specific EM and it hasn't been added to that page yet,
    uncomment the line at the bottom of the file after replacing the url, 
    name, and spoiler tag, and comment out the rest of the main method. 

Writes one file per extra material to ./Pale_Chapters/EM/<em_name>.txt
"""

## ADD EXCEPTIONS HERE   ###############################################
########################################################################

EXCEPTION_MAPPING = { '[0.0]' : (10, 1, {1 : [0]}, 1), 
                              # (<rank>, 
                              #  <transcript start depth>, 
                              #  <reply filtering at depth>, 
                              #  <max transcript depth>)
                              #
                              # <rank> 
                              #     The comment on the page that contains
                              #     the comment section transcript, 0-indexed.
                              # <transcript start depth> 
                              #    The number of levels deep into the 
                              #    replies of this comment to start recording 
                              #    the transcript.
                              # <reply filtering at depth> 
                              #    Maps a reply depth level to the 0-indexed
                              #    replies that we should collect at this 
                              #    level. This will be consistent across 
                              #    "branches" of the reply tree. 
                              # <max transcript depth>
                              #    The max depth of replies we consider.
                      '[3.1]' : None, 
                              # 'None' indicates I found a 'transcript', but 
                              # there actually isn't one for this EM. Writing
                              # None here prevent searching for a transcript
                              # for this EM
                      '[5.2]' : (6, 0, None, 3),
                              # a reply rank of "None" means we aren't 
                              # restricting which replies we consider for
                              # each level of collected replies
                              # Similarly, if a reply depth does not appear
                              # as a key in the mapping, but it *is* a reply
                              # depth we consider, then we don't restrict
                              # which comments we collect at that level
                      '[5.5]' : (0, 0, None, 3),
                      '[6.9]' : (8, 0, {1: [0,1]}, 1),
                              # EX: at reply depth 1, only take the first and
                              #     second comments
                      '[7.3]' : (0, 0, None, 3),
                      '[8.2]' : (0, 0, None, 2),
                      '[9.9]' : None,
                      '[12.7]': (2, 0, None, 0)
}

#######################################################################
#######################################################################

if len(sys.argv)<2:
    DOWNLOAD_ONE_EM = None
else:
    DOWNLOAD_ONE_EM = sys.argv[1]

class EM():
  def __init__(self, url, name, tag):
    self.url = url
    self.name = name
    self.tag = tag

def get_em_list():
  """Returns a list of EMs; all extra materials listed at 
  "https://palewebserial.wordpress.com/extra-material/" """
  em_page_link = "https://palewebserial.wordpress.com/extra-material/"
  em_page = requests.get(em_page_link).text
  soup = bs4.BeautifulSoup(em_page, features="html.parser")
  entry = soup.html.contents[5].contents[2].contents[4].contents[1].contents[1].contents[1].contents[4]
  ems = []
  em_num = 1
  for i in range(len(entry.contents)):
    item  = entry.contents[i]
    if type(item) == bs4.element.Tag and item.name == "p":
      spoiler_tags = re.findall("\[[0-9]+\.[0-9a-z]+\]",item.get_text())
      links = item.findChildren("a" , recursive=True)
      for j in range(len(links)):
        link = links[j]
        url = link.get("href")
        em_str = str(em_num) if em_num >= 10 else "0"+str(em_num)
        name = f"({em_str}) {spoiler_tags[j]} {link.get_text()}"
        tag = spoiler_tags[j]
        ems.append(EM(url, name, tag))
        em_num += 1
  return ems

def get_this_em(spoiler_tag):
  """Returns a single EM, where the spoiler tag is the same as what's
  passed in. """
  em_list = get_em_list()
  for em in em_list:
      if spoiler_tag in em.tag:
          return em

def get_em_text(contents):
    """Returns any text on the page, or the empty string if it's just
    pictures."""
    text=""
    for item in contents:
        if type(item) == bs4.element.Tag and item.get("id") is None:
            text+=item.get_text()+"\n\n"
    return text.strip().replace('’', "'").replace("”", '"').replace("“", '"')

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

def get_all_reply_text(comment_element, start=1, rank=None, max_depth=0,curr=1):
    """ Gets all the replies to a comment subject to the constraints
    passed in. Starts collecting comment text at reply depth `start`. Only 
    collects the replies indicated by the `rank` mapping, and only
    continues down a branch up to `max_depth`. """
    if curr > max_depth:
        return ""
    children = None
    try:
        children = comment_element[4].contents
    except:
        return ""
    reply_text = ""
    replies = 0
    for i in range(len(children)):
        item = children[i]
        if type(item) == bs4.element.Tag:
            if rank is not None and curr in rank and replies not in rank[curr]:
                replies += 1
                continue
            replies += 1
            if curr >= start:
                reply_text += get_text_of_comment(item.contents)
            reply_text += get_all_reply_text(item.contents, start=start, rank=rank, max_depth=max_depth, curr=curr+1)
    return reply_text

def get_transcript_exception(comments, comment_rank, reply_depth, reply_rank, max_depth):
    """Looks for the extra material comment section, given instructions. """
    num_comments = 0
    for i in range(len(comments)):
        item = comments[i]
        if type(item) == bs4.element.Tag:
            if num_comments == comment_rank:
                comment_text = ""
                if reply_depth == 0:
                    comment_text = get_text_of_comment(comments[i].contents)
                comment_text += get_all_reply_text(comments[i].contents, start=reply_depth, rank=reply_rank, max_depth=max_depth)
                return comment_text
            num_comments += 1
    return ""

def get_transcript(comments):
    """Looks for an extra material transcript in the comment section. 
    Returns the empty string if no transcript is found."""
    for i in range(len(comments)):
        item = comments[i]
        if type(item) == bs4.element.Tag:
            comment_text = get_text_of_comment(comments[i].contents)
            comment_author = get_author_of_comment(comments[i].contents)
            ## GENERAL TRANSCRIPT-FINDING RULE
            if "Transcript" in comment_text \
                or "transcript:" in comment_text.lower() \
                or "unofficial transcript" in comment_text.lower() \
                or "text:" in comment_text.lower() \
                or comment_author.lower() in {"wildbow"}:
                return comment_text
    return ""

def download_em(em):
    """Goes to the url em.url, finds as much text as it can, and writes
    that text to a file."""
    em_page_text = requests.get(em.url).text
    soup = bs4.BeautifulSoup(em_page_text, features="html.parser")

    em.text = get_em_text(soup.html.contents[5].contents[2].contents[4].contents[1].contents[1].contents[4].contents[4].contents)

    comments = soup.html.contents[5].contents[2].contents[4].contents[1].contents[1].contents[7].contents[3].contents
    if em.tag in EXCEPTION_MAPPING:
        if EXCEPTION_MAPPING[em.tag] is None:
            em.transcript = ""
        else:
            comment_rank, reply_depth, reply_rank, max_depth = EXCEPTION_MAPPING[em.tag]
            em.transcript = get_transcript_exception(comments, comment_rank, reply_depth, reply_rank, max_depth)
    else:
        em.transcript = get_transcript(comments)

    em.transcript = em.transcript.replace('’', "'").replace("”", '"').replace("“", '"')
    write_file(em)

def write_file(em):
    """Write extra material text to Pale_Chapters/EM/<em_name>.txt"""
    dir = 'Pale_Chapters'
    if not os.path.exists(dir):
        os.mkdir(dir)
    if not os.path.exists(f"{dir}{os.path.sep}EM"):
        os.mkdir(f"{dir}{os.path.sep}EM")
    with open(f"{dir}{os.path.sep}EM{os.path.sep}{em.name}.txt", 'w') as file:
        if len(em.transcript.strip()) > 0:
            file.write(em.text + "\n\nTRANSCRIPT \n\n" + em.transcript)
        else:
            file.write(em.text)
    print(f"Wrote {em.name}")

if __name__ == "__main__":
    if DOWNLOAD_ONE_EM is not None:
        em = get_this_em(DOWNLOAD_ONE_EM)
        download_em(em)
    else:
        ems = get_em_list()
        for em in ems:
            download_em(em)
    # download_em(EM("https://palewebserial.wordpress.com/2021/11/05/15-2-spoilers-keeping-tabs-kennet/","(40) [15.2] Keeping Tabs, Kennet", "[15.2]"))
