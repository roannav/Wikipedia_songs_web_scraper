#! python3
# save_song_data.py - save song data from every year's 
# Billboard Year-End Hot 100 singles pages on Wikipedia.
# Run it: py save_song_data.py

# In summary, 
# 1) use get_links_to_years to get a list of urls of Wikipedia song pages
# Then for each Wikipedia Year-End songs page:
# 2) use requests.get() to download the web page that contains the data 
# 3) use BeautifulSoup to parse the HTML of the web page
# 4) output all the useful data to a csv file

import requests, bs4, time
import get_text_from_table, get_links_to_years

def go_slow():
    #https://api.wikimedia.org/wiki/Documentation/Getting_started/Rate_limits
    # says anonymous requests are limited to 500 / hr.
    # 3600 sec/hr / 500 req/hr = 7.2 sec/req
    time.sleep(8)

def get_soup( url, local_file, use_local_file):
    print(f'All the song data in {url}:')

    if use_local_file:
        f = open(local_file)

        # Use the best HTML parser on my system ("lxml"). 
        soup = bs4.BeautifulSoup(f, features='lxml')

    else:  # retrieve file from Internet
        # We don't want to wait too long, so
        # if I don't get a response in 10 sec, then exit the request
        # and raise requests.exceptions.ReadTimeout
        res = requests.get(url, timeout=10)
        print('Finished requests.get(url)')
        res.raise_for_status()   # halt program here, if the request failed
        go_slow()

        # Use the best HTML parser on my system ("lxml"). 
        soup = bs4.BeautifulSoup( res.text, features="lxml")

    return soup

def test_1980():
    # use local file, instead of grabbing it from the Internet
    USE_LOCAL_FILE = True 

    url_base = "https://en.wikipedia.org"
    url_1980 = "/wiki/Billboard_Year-End_Hot_100_singles_of_1980"
    # All these wikipedia pages about Billboard Year End Hot 100 singles 
    # look similar.  So I just chose 1980 randomly.  
    url = url_base + url_1980
    local_file = "html/Billboard_Top_in_1980.html"

    soup = get_soup( url, local_file, USE_LOCAL_FILE)

    # grab the first table that looks like...
    #   <table class="wikitable sortable" style="text-align: center">

    #song_table = soup.select('table.wikitable')[0] # first table

    #song_rows = soup.select('table.wikitable tr')  # all the rows in the table
    #print(song_rows[0])   # table header
    #print(song_rows[1])   # first row is the first song

    data, cols = get_text_from_table.get_text_from_table(soup, True, 
                                                         "wikitable") 
    get_text_from_table.convert_table_to_csv( data, cols, 'output_1980.csv')

#test_1980()


def save_every_years_song_data():
    year_links = get_links_to_years.get_links_to_years()

    url_base = "https://en.wikipedia.org"

    for year_link in year_links:
        year = year_link[-4:]   # the last 4 chars of the url is the year

        if int(year) != 2013:    # to test only this single year
            continue
        #if int(year) <= 1958:    # to test only after 1958 
        #    continue

        print(f'year is {year}')
        url = url_base + year_link 
        soup = get_soup( url, None, False)

        data, cols = get_text_from_table.get_text_from_table(soup, True, 
                                                         "wikitable") 
        get_text_from_table.convert_table_to_csv( data, cols, 
            f'output/songs_{year}.csv')


save_every_years_song_data()
