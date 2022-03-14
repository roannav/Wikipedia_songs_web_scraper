The [repository on GitHub](https://github.com/roannav/Wikipedia_songs_web_scraper) contains all the Python scripts.
The [website](https://roannav.github.io/Wikipedia_songs_web_scraper/) for this GitHub repository.

### A web scraper for Wikipedia pages containing Billboard Top Songs for each year.

![Wikipedia logo](Wikipedia-logo-v2-en.svg)

### [requirements.txt](/../main/requirements.txt)

### [get_text_from_html.py](/../main/get_text_from_html.py)
Takes any HTML, even a snippet from a web page,
and returns just the text contained between any of the tags,
not including the \<head\>, <style>, and <script> sections.

### [get_text_from_infobox.py](/../main/get_text_from_infobox.py)
Given the HTML of a Wikipedia page about a song,
and given an attribute, it will search the Wikipedia infobox
for the attribute and return the value.

### [get_links_to_years.py](/../main/get_links_to_years.py)
Given the HTML of a Wikipedia page about Billboard Top Songs in Year X,
it will print the link to all other similar pages.

### [get_text_from_table.py](/../main/get_text_from_table.py)
Given the HTML of a Wikipedia page about Billboard Top Songs in Year X,
it finds and reads a table with the Top Songs of the Year, then it returns a 2D array of the data and a column titles array.  Finally, saves the data to csv.

### [save_song_data.py](/../main/save_song_data.py)
For every year available, 
given the url of a Wikipedia page about Billboard Top Songs in Year X,
it gets table data about the Top Songs of the Year and finally outputs 
to output/songs_{year}.csv

### [fix_and_concat_datasets.py](/../main/fix_and_concat_datasets.py)
Takes all the data for that year&apos;s songs in output/songs_{year}.csv
and combines it into 1 file output/Billboard_1946_to_2021.csv 

### [download_song_page.py](https://github.com/roannav/Wikipedia_songs_web_scraper/blob/main/download_song_page.py)
output/Billboard_1946_to_2021.csv contains a list of Wikipedia urls to songs.  For the specified sublist of songs, it downloads those web pages.

#### Credits
Wikipedia Logo By Wikimedia Foundation, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=10309782
