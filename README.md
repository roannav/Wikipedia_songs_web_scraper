# web_scraper

A collection of Python code to scrape websites.

### requirements.txt

### get_text_from_html.py
Takes any HTML, even a snippet from a web page,
and returns just the text contained between any of the tags,
not including the <head>, <style>, and <script> sections.

### get_text_from_infobox.py
Given the HTML of a Wikipedia page about a song,
and given an attribute, it will search the Wikipedia infobox
for the attribute and return the value.

### get_links_to_years.py
Given the HTML of a Wikipedia page about Billboard Top Songs in Year X,
it will print the link to all other similar pages.

### get_text_from_table.py
Given the HTML of a Wikipedia page about Billboard Top Songs in Year X,
it finds and reads a table with the Top Songs of the Year, then it returns a 2D array of the data and a column titles array.  Finally, saves the data to csv.

### save_song_data.py
For every year available, 
given the url of a Wikipedia page about Billboard Top Songs in Year X,
it gets table data about the Top Songs of the Year and finally outputs 
to output/songs_{year}.csv

### fix_and_concat_datasets.py
Takes all the data for that year&apos;s songs in output/songs_{year}.csv
and combines it into 1 file output/Billboard_1946_to_2021.csv 

### download_song_page.py
output/Billboard_1946_to_2021.csv contains a list of Wikipedia urls to songs.  For the specified sublist of songs, it downloads those web pages.

