import sys
import pandas as pd
from pandas import DataFrame, Series
from wget import download

FIRST_YEAR = 1946
LAST_YEAR = 2021

f = 'output/Billboard_1946_to_2021.csv'
# columns are ['year', 'rank', 'title', 'artist', 'song_URL']
# header=0   ==> use the first row as the column headers
df = pd.read_csv(f, header=0)

#if sys.argv >= 2: 
 

print(df.song_URL)  # Series
print(df.song_URL[0])  # first song 


url_base = "https://en.wikipedia.org"
url = url_base + df.song_URL[0]
print(url)
try:
    download(url, out='html2')
except err:
    print(err)   #urllib.error.HTTPError:  # HTTP Error 404: Not Found
