# Quote Finder for Wildbow's Pale
This project is intended to be an efficient way to search for quotes within Pale, to get around deficiencies in Wordpress's built in search feature (slow retrieval, inability to see the matching quote without clicking the chapter link, etc.). I don't own any of the materials downloaded by these scripts. Visit [palewebserial.wordpress.com](https://palewebserial.wordpress.com/) to learn more about Pale and support the author. 

## Setup
Ensure you have Python installed. Run `pip install -r requirements.txt` to ensure you have all the necessary packages. 

## File Downloads

Since the purpose of the file download is quote-finding, all downloaded files are text only, with no formatting beyond paragraph breaks. 

```$ python get_text.py``` 

Downloads a local copy of every chapter of Pale in a directory `Pale_Chapters/`. This download will take a minute or so, so wait for the program to stop outputting text before checking to make sure the files downloaded successfully. The arcs are separated out into separate folders. You can download fewer chapters by starting from a different link (see the documentation in the file).

Pale chapters are downloaded into `Pale_Chapters/<ARC_NUM>/(<ABSOLUTE_CHAP_NUM>) <ARC_NAME> <ARC_NUM>.<ARC_CHAP_NUM> (<PERSPECTIVE>).txt`. For example, chapter "False Moves 12.1" would be downloaded as `Pale_Chapters/12/(118) False Moves 12.1 (Verona).txt`.

```$ python em_download.py``` 

Downloads all the extra materials as raw text in `Pale_Chapters/EM` (it downloads both the page text and comment section transcript text. No images since the goal of this download is to find quotes). As with `get_text`, this download will take a minute. You can download all the extra materials for the story or just one extra material at a time, see the in-file documentation. 

Extra Materials are downloaded as `Pale_Chapters/EM/(<EM NUMBER>) [<CHAPTER>] <TITLE>.txt`. For example, the "Path Practicalities" extra material will be downloaded as `Pale_Chapters/EM/(35) [9.3] Path Practicalities.txt`.

**Run both of the above commands with no arguments to download all of Pale. See below to explore other download options.**

### Adding New Chapters and Extra Materials

When a new chapter is released, there's no need to download all of Pale again. Simply run the following command to get the most recent chapter:

```
python get_text.py <link-to-chapter>
```

**NOTE:** The absolute chapter numbering relies on the "Previous Chapter" link working. If you download a chapter and notice that it's been numbered as chapter "001" instead of 1 + the number of the previous chapter, this is probably because the link is broken. You can rename the file to number the chapter correctly, or wait until the link is fixed and run the script again for this chapter.

**IMPORTANT:** If the new chapter is an interlude, the download will fail unless you add the perspective of that interlude to the `INTERLUDE_PERSPECTIVES` mapping first, in `get_text.py` (this variable is clearly marked near the top of the file, just add an entry mapping the chapter title to the perspective the chapter is from).

When a new extra material is released, run the following command to download it:

```
python em_download.py 'X.X'
```

Replace `'X.X'` with the chapter number that the extra material was for (e.g., the argument `'7.3'` downloads the 'Borrowed Eyes Comic' extra material). 

**NOTE:** Unlike the chapter download script, this script fetches extra materials from the extra material table of contents page. Sometimes it takes a few days for this page to be updated with new releases, in which case the script will not be able to find the content. If you want the EM before that time, follow the instructions in the documentation inside the `em_download.py` file.

## Pale Quote Search Engine

`search_pale` is a script that makes searching for quotes in Pale using regular expressions super easy!

**USE:** `./search_pale.sh <PATTERN> <FLAGS> <DIRECTORY> <GLOBAL PATTERN> <GLOBAL PATTERN FLAGS>`
- `PATTERN` is the regular expression that you want the returned lines to match (**required**)
- `FLAGS` are the flags you want `egrep` to use (**optional**)
- `DIRECTORY` is the directory you want to search in. Since chapters are grouped into folders by arc/extra material status, you can use this input to search only within a particular arc. Or, you can use this input to search only Avery chapters, or only interludes, etc. (**optional**)
- `GLOBAL PATTERN` restricts the egrep results to only search files that contain this pattern. (**optional**)
- `GLOBAL PATTERN FLAGS` are the flags you want to pass to egrep for the global pattern (**optional**)

### First, a Simple Workflow Example to Get Started

(There will be more input/output examples below)

Let's say I want to find the moment that Nicolette Belanger brings Seth under her protection after he's forsworn. I remember that she used the word 'protect' (or possibly 'protection'?) as she made her declaraion, but I don't remember what order those words occurred in, and I don't remember what chapter it was, just that it occured somewhere in Arc 6, 7, or 8. 

In this case, I could run the following command to search for lines in Arcs 6, 7, or 8 than contain both "Seth" and "protect": 

```
./search_pale.sh "Seth.*protect|protect.*Seth" "" "0[678]"
```

This will bring up the following results:

<img src="https://user-images.githubusercontent.com/54676970/123558064-5bb09c80-d762-11eb-9f07-131acec89c27.png" alt="ex_1" width="700"/>

From these results, I can easily see that the first result was what I was looking for!

Now let's say that I want to read the rest of the conversation surrounding this moment. Since the results are dispalyed with chapter numbers, I see that my quote occurs 6.z. Then, I can then run:

```
./open_pale.sh 6 z
```

Which opens chapter 6.z in a text file. Since the search results told me exactly the wording of the quote, I can simply `cmmd+F` to find the place in the chapter that I'm looking for.  


### Tips for Effective Quote-Finding

**Use Regular Expressions to Search:**

If you're not familiar with the syntax of regualr expressions, you can find a handy cheat sheet [here](https://web.mit.edu/hackl/www/lab/turkshop/slides/regex-cheatsheet.pdf). Some key tips:
- First of all, if you aren't comfortable with regular expressions and don't want to learn, verbatim search (simply searching for the quote you want) works just fine
- Use `.*` to match any sequence of characters. If you know that some keywords appear in a quote but you're not sure what happens between them, this comes in handy
- Use `\b` to match words boundaries, for example, if you were looking for information on plicate spirits, a search for `plicate` would also match the word `implicate`, but `\bplicate\b` will match only `plicate`. 

**Use Flags to Customize your Search:**

The flags I use the most often are:
- `i`: makes your search case-insensitive
- `l` displays only the chapters matched, and not the lines themselves. This is a good way to get a sense for how many results your search will return, or which arcs to start looking in

**Filter by Arc:**

All of the pale chapters are placed in a directory per arc. For example, all of the Arc 1 chapters are in a directory `01/`. To search only for results in Arc 1, simply pass `"01"` as the third flag to `./search_pale`. 

To search through multiple arcs at a time, you can use shell expansion. Ex: `./search_pale "<pattern>" "" "0[123]"` searches arcs 1, 2, and 3 for `<pattern>`. Brace exansion like `{01,02,03}` instead of `0[123]` will also work.

**Filter by Perspective:**

Every chapter file is annotated with the perspective (e.g. 'Verona', 'Interlude'). Then, you can use the 'directory' argument to filter by a particular persepctive. For example, to only search for quotes in chapters from Avery's perspective, use `./search_pale "<pattern>" "" "[01][0-9]/*Avery*"` (the `[01][0-9]` searches every arc, and the `*Avery*` matches only Avery chapters).

**Search Only Within a Chapter:**

Similarly, you can use the "directory" argument to search only witin a chapter or chapters, for example: `./search_pale "<pattern>" "" "01/*1.[56]*"` will search only chapters 1.5 and 1.6. You can also use brace expansion, like `./search_pale "<pattern>" "" "[01][0-9]/*{1.3,9.10}]*"`

**(IMPORTANT) A Note on Searches Involving Double-Quotes:**

While you can use `'` to your heart's content, the character `"` can be a little weird and cause `EOF` errors. If you want to search for a line including the `"` character:
- Escape the symbol with a `\`
- Pass in a space character as the `GLOBAL PATTERN` argument

**EX:** Instead of `./search_pale.sh '" Charles'`, do `./search_pale.sh '\" Charles' '' '' ' '` (note that in order to use the `GLOBAL PATTERN` argument, you have to pass in the `FLAGS` and `DIRECTORY` arguments, too)

This will give you the expected results, since restricting your search to files containing a space is the same as searching all files. Introducing the space as global pattern simply forces the script to invoke the global pattern handler, which is implemented in a way that nullifies the problems introduced by the `"`. 

If there are known errors with normal searching that are fixed by the global search method, why isn't the global search method default? Unfortunately, that method is noticeably slower, and I thought it wasn't worth slowing down all searches to handle one use case. 

### Input/Output Examples

**INPUT:**

```
./search_pale.sh "Seal of Solomon" "" "[01][0-9]/*Interlude*"
```
- Finds all occurrences of the phrase "Seal of Solomon" in interludes

**OUTPUT:**

<img src="https://user-images.githubusercontent.com/54676970/123557731-99142a80-d760-11eb-9ee1-9738e5f25d31.png" alt="ex_2" width="700"/>

**INPUT:**

```
./search_pale.sh "[^a-z]Oni[^a-z]" "i" "" "Tymon" "i"
```
- Finds all occurences of the word "Oni" (ignoring case, and ignoring words where 'oni' is emebedded in the middle) in chapters that also contain the word "Tymon" (also ignoring case). Note that I could have used `\b` instead of `[^a-z]`. 

**OUTPUT:** (only some results shown for brevity) 

<img src="https://user-images.githubusercontent.com/54676970/120935216-b01aac00-c6cf-11eb-8b19-13c30f508c63.png" alt="ex_3" width="700"/>

**INPUT:**

```
./search_pale.sh " " "l" "EM/*.[a-z]*.*"
```
- Retrieves a list of all of the Extra Materials whose accompanying chapter was an interlude

**OUTPUT:**

<img src="https://user-images.githubusercontent.com/54676970/120935239-c7f23000-c6cf-11eb-8534-31f4326d6f99.png" alt="ex_3" width="700"/>

## Other Scripts

### Open Pale

`open_pale` is just a script that makes opening chapters faster than finding and clicking on the files by hand.
- `./open_pale.sh 1 4` opens 1.4
- `./open_pale.sh em 1 4` would open the **extra material** for 1.4

### Chapter Perspective Count

`./chapter_perspective_count.sh` gives as overviews of the number of chapters per arc from each character's perspective, and the number of words per arc from each perspective, as well as story-level stats. 

**SAMPLE OUTPUT**

```
$ ./chapter_perspective_count.sh

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

### Word Count

`./word_count.sh` Gives total word counts per arc and total EM word count, as well as total story word count. 

**SAMPLE OUTPUT**

```
$./word_count.sh

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

### Individual Counts

`./individual_counts.sh` prints the word count for every know chapter and extra material, in the form `<word_count> -- <file_name>`, not sorted in any particular order.

The idea behind this script is that it can be fed to other commands to easily get information about word count stats in Pale that aren't covered by the other two scripts listed above.

**EXAMPLES:**

```
./individual_counts.sh | grep "Verona" | sort -n -r | head -3
```

This will print the top 3 longest Verona chapters:

```
   13679 -- (109) Dash to Pieces 11.6 (Verona).txt
   13675 -- (102) One After Another 10.4 (Verona).txt
   12973 -- (026) Out on a Limb 3.6 (Verona).txt
```

To get the top extra materials, we can cheat, and use the knowledge that all extra materials are save as files that contain the chapter they were posted after in square brackets (for example,  `(15) [3.9] SunnyDay Logs.txt`). So, we can do:

```
./individual_counts.sh | grep "\[" | sort -n -r | head -3
```

To get the top 3 longest extra materials. 
