import sys, time, math
import pandas as pd
from pandas import DataFrame, Series
import wget
import urllib

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


for i in range(18,21):
    url_i = df.song_URL[i]
    print(url_i)
    if type(url_i) == type('') and url_i.startswith('/wiki/'): 
        url = url_base + url_i 
        print(url)
        try:
            # wget expects a file extension.  Else it raises 
            #   "ValueError: not enough values to unpack (expected 2, got 1)"
            filename = wget.download(url, 'html2' + url_i + '.html')
            #filename = wget.download(url, output='html2', bar=bar_thermometer)
            print(f"\nFinished downloading {filename}")
        except urllib.error.HTTPError as err:
            #urllib.error.HTTPError: HTTP Error 404: Not Found
            #urllib.error.HTTPError: HTTP Error 400: Bad Request
            print('\nurllib.error.HTTPError occurred.')
            print(err)
            print('\n')
        except Exception as err:
            print('\nException occurred.')
            print(err)
            print('\n')


        go_slow()

    elif math.isnan(url_i):
        print(f"INFO: no url given for {df.year[i]}'s"
            + f" \"{df.title[i]}\" sung by {df.artist[i]}")
    else:
        print("ERROR: url must be NaN or a string beginning with '/wiki/'")
        print(f"       for {df.year[i]}'s"
            + f" \"{df.title[i]}\" sung by {df.artist[i]}")
