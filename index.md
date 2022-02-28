

The [repository on GitHub](https://github.com/roannav/Wikipedia_songs_web_scraper) contains all the Python scripts.

### A web scraper for Wikipedia pages containing Billboard Top Songs for each year.

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



<!--
Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [Basic writing and formatting syntax](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/roannav/Wikipedia_songs_web_scraper/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.

-->
