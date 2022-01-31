# web_scraper

A collection of Python code to scrape websites.

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


