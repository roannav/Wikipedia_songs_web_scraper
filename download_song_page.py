import sys, time, math
import pandas as pd
from pandas import DataFrame, Series
import wget
import urllib
import logging

FIRST_YEAR = 1946
LAST_YEAR = 2021

f = 'output/Billboard_1946_to_2021.csv'
# columns are ['year', 'rank', 'title', 'artist', 'song_URL']
# header=0   ==> use the first row as the column headers
df = pd.read_csv(f, header=0)

#if sys.argv >= 2: 
#print(df.song_URL)  # Series
#print(df.song_URL[0])  # first song 


url_base = "https://en.wikipedia.org"


def go_slow():
    print('pausing...\n')
    #https://api.wikimedia.org/wiki/Documentation/Getting_started/Rate_limits
    # says anonymous requests are limited to 500 / hr.
    # 3600 sec/hr / 500 req/hr = 7.2 sec/req
    time.sleep(8)

    # if using OAuth 2.0 or a personal API token to do authentication, 
    # then requests are limited to 5000 / hr.


def progress_bar(current, total, width=80):
    # IN: 'total' can not be 0 (to avoid ZeroDivisionError)
    # IN: 'width' is number of open spaces in the progress bar
    # Returns a string, that looks like a progress bar
    # that begins as a dark bar and becomes a light bar as it progresses.

    lit_spaces = int(float(current) / total * width)
    return '\u2593' * lit_spaces + '\u2591' * (width - lit_spaces)


for i in range(18,21):
    url_i = df.song_URL[i]
    print(url_i)
    if type(url_i) == type('') and url_i.startswith('/wiki/'): 
        url = url_base + url_i 
        print(url)
        try:
            # wget.download(file_to_download, output_dir_filename, progress_bar)
            # wget expects a file extension.  Else it raises 
            #   "ValueError: not enough values to unpack (expected 2, got 1)"
            # Need to assign 'bar' a value or None
            #   or else it prints "-1 / unknown"
            #filename = wget.download(url, 'html2' + url_i + '.html', bar=None)
            filename = wget.download(url, 'html2' + url_i + '.html',
                bar=progress_bar)
            print(f"\nFinished downloading {filename}")
        except urllib.error.HTTPError as err:
            #urllib.error.HTTPError: HTTP Error 404: Not Found
            #urllib.error.HTTPError: HTTP Error 400: Bad Request
            print('\nurllib.error.HTTPError occurred.')
            print(err)
            print('\n')
            logging.exception('\nurllib.error.HTTPError occurred.')
        except Exception as err:
            print('\nException occurred.')
            print(err)
            print('\n')
            logging.exception('\nException occurred.')


        go_slow()

    elif math.isnan(url_i):
        print(f"INFO: no url given for {df.year[i]}'s"
            + f" \"{df.title[i]}\" sung by {df.artist[i]}")
    else:
        print("ERROR: url must be NaN or a string beginning with '/wiki/'")
        print(f"       for {df.year[i]}'s"
            + f" \"{df.title[i]}\" sung by {df.artist[i]}")
