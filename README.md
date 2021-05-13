# Download Pale
## Setup
Run `pip install -r requirements.txt` to ensure you have all the necessary packages. 

## File Downloads

`python get_text.py` downloads a local copy of every chapter of Pale in a directory Pale_Chapters/. The arcs are separated out into separate folders. Or, you can download fewer chapters by starting from a different link (see the documentation in the file).

`python em_download.py` downloads all the extra materials as raw text in Pale_Chapters/EM (it downloads both the page text and comment section transcript text). You can download all the extra materials for the story or just one extra material at a time, see the in-file documentation.  

**Run both of the above files with no arguments to download all of Pale. See the documentation in the files themselves to see other download options.**

## Pale Search Engine
`open_pale` is just a script that makes opening chapters faster. EX: `./open_pale 1 4` opens 1.4 for example, and `./open_pale em 1 4` would open the extra material for 1.4. 

`search_pale` is a script that makes searching for quotes in Pale super easy.

**USE:** `./search_pale.sh <PATTERN> <FLAGS> <DIRECTORY> <GLOBAL PATTERN> <GLOBAL PATTERN FLAGS>`
- `PATTERN` is the regular expression that you want the returned lines to match (**required**)
- `FLAGS` are the flags you want `egrep` to use (**optional**)
- `DIRECTORY` is the directory you want to search in. Since chapters are grouped into folders by arc/extra material status, you can use this input to search only within a particular arc. Or, you can use this input to searh conly Avery chapters, or only interludes, etc. (**optional**)
- `GLOBAL PATTERN` restricts the egrep results to only search files that contain this pattern. (**optional**)
- `GLOBAL PATTERN FLAGS` are the flags you want to pass to egrep for this pattern (**optional**)

**EXAMPLES:**

`./search_pale.sh "Charles.*Cherrypop|Cherrypop.*Charles"` 
- finds every time Cherrypop and Charles were mentioned in the same line

`./search_pale.sh "Snowdrop" "" "[01][0-9]/*Avery*"`
- finds all occurrences of the word "Snowdrop" in Avery chapters 

`./search_pale.sh "[^a-z]Oni[^a-z]" "i" "" "Tymon" "i"`
- finds all occurences of the word "Oni" (ignoring case, and ignoring words where 'oni' is emebedded in the middle) in chapters that also contain the word "Tymon" (also ignoring case)

`./search_pale.sh " " "l" "EM/*.[a-z]*.*"`
- retrieves a list of all of the Extra Materials whose accompanying chapter was an interlude
