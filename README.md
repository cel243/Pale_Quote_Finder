# Quote Finder and Local Download of Wildbow's Pale
This project is intended to be an efficient and powerful way to search for quotes within Pale, to get around deficiencies in Wordpress's built in search feature (slow retrieval, inability to see the matching quote without clicking the chapter link, etc.). I don't own any of the materials downloaded by these scripts. Visit [palewebserial.wordpress.com](https://palewebserial.wordpress.com/) to learn more about Pale and support the author. 

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

## Other Scripts

`./chapter_perspective_count.sh` Gives as overviews of the number of chapters per arc from each character's perspective, and the number of words per arc from each perspective, as well as story-level stats. 

**SAMPLE OUTPUT**

```
----- CHAPTERS ---- WORDS ----
----|----------|-------------
 L: |    33    |   316114
 V: |    33    |   329579
 A: |    34    |   313332
 I: |    21    |   229607

- ARC -- PERSECTIVE CHAP COUNT ------------- PERSPECTIVE WORD COUNT---------
------|--------------------------||-----------------------------------------
  01: | L (2) V (3) A (3) I (1)  ||  L (16457) V (26559) A (27839) I (11738) 
  02: | L (3) V (3) A (3) I (1)  ||  L (34210) V (34338) A (32480) I (15668) 
  03: | L (4) V (2) A (3) I (1)  ||  L (41496) V (21988) A (25175) I (12770) 
  04: | L (3) V (3) A (4) I (1)  ||  L (32643) V (29639) A (36772) I (8640) 
  05: | L (1) V (3) A (1) I (4)  ||  L (10861) V (29213) A (10245) I (42673) 
  06: | L (4) V (2) A (3) I (1)  ||  L (36740) V (19372) A (27762) I (11347) 
  07: | L (2) V (3) A (4) I (2)  ||  L (16398) V (33785) A (36992) I (20994) 
  08: | L (3) V (4) A (3) I (1)  ||  L (19139) V (32759) A (27255) I (9185) 
  09: | L (5) V (3) A (4) I (1)  ||  L (47424) V (29958) A (36579) I (9938) 
  10: | L (2) V (1) A (1) I (6)  ||  L (21203) V (13675) A (11540) I (67732) 
  11: | L (4) V (6) A (5) I (1)  ||  L (39543) V (58293) A (40693) I (11745) 
```

**Note that these word counts are different than the official spreadsheet. This is because I'm a bit less careful about what constitutes a "word." The word counts should be approximately correct.**

`./word_count.sh` Gives total word counts per arc and total EM word count, as well as total story word count. 

**SAMPLE OUTPUT**

```
-ARC-|--WORDS-----|
-----|------------|
 00  |  7177
 01  |  82593
 02  |  116696
 03  |  101429
 04  |  107694
 05  |  92992
 06  |  95221
 07  |  108169
 08  |  88341
 09  |  123899
 10  |  114150
 11  |  150280
 EM  |  107099
-----------------------
TOTAL WORDS: 1295740
```

**You can also pass an arc number to this script as an argument.**

For example: `./word_count.sh 10` outputs:

```
---CHAP---|---WORDS---|
----------|-----------|
   10.1   |  11540
   10.a   |  13656
   10.b   |  9026
   10.c   |  9736
   10.2   |  12334
   10.d   |  9895
   10.e   |  11348
   10.3   |  8869
   10.4   |  13675
   10.z   |  14071
----------------------
ARC TOTAL: 114150
```

When passing in arc numbers, do **NOT** pad the arc numbers with zeros. For example, use `./word_count.sh 2` instead of `./word_count.sh 02`. 