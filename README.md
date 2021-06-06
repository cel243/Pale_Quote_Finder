# Quote Finder and Local Downlaod of Wildbow's Pale
This project is intended to be a more efficient and powerful way to search for quotes within Pale than Wordpress's built-in search feature. I don't own any of the materials downloaded by these scripts. Visit [palewebserial.wordpress.com](https://palewebserial.wordpress.com/) to learn more about Pale and support the author. 

## Setup
Ensure you have Python installed. Run `pip install -r requirements.txt` to ensure you have all the necessary packages. 

## File Downloads

Since the purpose of the file download is quote-finding, all downloaded files are text only, with no formatting beyond paragraph breaks. 

`python get_text.py` downloads a local copy of every chapter of Pale in a directory Pale_Chapters/. The arcs are separated out into separate folders. Or, you can download fewer chapters by starting from a different link (see the documentation in the file). Each chapter is labeled with number, arc title, absolute chapter number, and perspective. 

`python em_download.py` downloads all the extra materials as raw text in Pale_Chapters/EM (it downloads both the page text and comment section transcript text. No images). You can download all the extra materials for the story or just one extra material at a time, see the in-file documentation.  

**Run both of the above files with no arguments to download all of Pale. See the documentation in the files themselves to see other download options.**

## Pale Quote Search Engine
`open_pale` is just a script that makes opening chapters faster. EX: `./open_pale 1 4` opens 1.4 for example, and `./open_pale em 1 4` would open the extra material for 1.4. 

`search_pale` is a script that makes searching for quotes in Pale using regular expressions super easy!

**USE:** `./search_pale.sh <PATTERN> <FLAGS> <DIRECTORY> <GLOBAL PATTERN> <GLOBAL PATTERN FLAGS>`
- `PATTERN` is the regular expression that you want the returned lines to match (**required**)
- `FLAGS` are the flags you want `egrep` to use (**optional**)
- `DIRECTORY` is the directory you want to search in. Since chapters are grouped into folders by arc/extra material status, you can use this input to search only within a particular arc. Or, you can use this input to search only Avery chapters, or only interludes, etc. (**optional**)
- `GLOBAL PATTERN` restricts the egrep results to only search files that contain this pattern. (**optional**)
- `GLOBAL PATTERN FLAGS` are the flags you want to pass to egrep for this pattern (**optional**)

**EXAMPLES:**

`./search_pale.sh "Charles.*Cherrypop|Cherrypop.*Charles"` 
- finds every time Cherrypop and Charles were mentioned in the same line

**OUTPUT:**

<img src="https://user-images.githubusercontent.com/54676970/120935081-13f0a500-c6cf-11eb-82d9-dabb50f0fa42.png" alt="ex_1" width="700"/>

`./search_pale.sh "Snowdrop" "" "[01][0-9]/*Avery*"`
- finds all occurrences of the word "Snowdrop" in Avery chapters 

**OUTPUT:** (only some results shown for brevity) 

<img src="https://user-images.githubusercontent.com/54676970/120935121-3682be00-c6cf-11eb-8958-99435d01500b.png" alt="ex_2" width="700"/>

`./search_pale.sh "[^a-z]Oni[^a-z]" "i" "" "Tymon" "i"`
- finds all occurences of the word "Oni" (ignoring case, and ignoring words where 'oni' is emebedded in the middle) in chapters that also contain the word "Tymon" (also ignoring case)

**OUTPUT:** (only some results shown for brevity) 

<img src="https://user-images.githubusercontent.com/54676970/120935216-b01aac00-c6cf-11eb-8b19-13c30f508c63.png" alt="ex_3" width="700"/>

`./search_pale.sh " " "l" "EM/*.[a-z]*.*"`
- retrieves a list of all of the Extra Materials whose accompanying chapter was an interlude

**OUTPUT:**

<img src="https://user-images.githubusercontent.com/54676970/120935239-c7f23000-c6cf-11eb-8534-31f4326d6f99.png" alt="ex_3" width="700"/>
