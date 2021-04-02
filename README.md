# Download Pale

`python get_text.py` downloads a local copy of every chapter of Pale in a directory Pale_Chapters/

`python em_download.py` downloads all the extra materials as raw text (it tries to get the comment section unofficial transcript when the EM is just pictures) 

`open_pale` is just a script that makes opening chapters faster. `./open_pale 1 4` opens 1.4 for example, and `./open_pale em 1 4` would open the extra material for 1.4. 

`search_pale` is a script that makes grepping through Pale really easy. also formats the results, sort of. 
- first argument is a regular expression to search for
- second argument specifies a directory (arc, extra materials folder, etc.); can be left blank, default is just to search everything
- third argument is any flags to pass to `grep`; can be left blank
