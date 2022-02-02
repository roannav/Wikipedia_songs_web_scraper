#! python3
# get_links_to_years.py - prints (and returns) just the links to each year's Billboard Year-End Hot 100 singles pages on Wikipedia.
# Run it: py get_links_to_years.py

# In summary, 
# 1) use requests.get() to download the web page that contains the links 
# 2) use BeautifulSoup to parse the HTML of the web page
# 3) print all the useful links 

import requests, bs4, re

def is_year(s):
    # matches 1900 - 2099
    reg = re.compile(r'(19|20)\d\d')

    # if it matches the pattern then it is a year, so return True
    return (reg.search(s) != None)


def get_links_to_years():
    # use local file, instead of grabbing it from the Internet
    USE_LOCAL_FILE = True

    url_base = "https://en.wikipedia.org"
    url_1980 = "/wiki/Billboard_Year-End_Hot_100_singles_of_1980"
    # All these wikipedia pages about Billboard Year End Hot 100 singles 
    # look similar.  So I just chose 1980 randomly.  They all have a table 
    # at the bottom that contains links to pages for every other year 
    # that is covered in Wikipedia (1946 to 2021).

    print(f'All the yearly Billboard links in {url_base + url_1980}:')

    if USE_LOCAL_FILE:
        f = open('html/Billboard_Top_in_1980.html')

        # Use the best HTML parser on my system ("lxml"). 
        soup = bs4.BeautifulSoup(f, features='lxml')

    else:  # retrieve file from Internet
        # We don't want to wait too long, so
        # if I don't get a response in 10 sec, then exit the request
        # and raise requests.exceptions.ReadTimeout
        res = requests.get(url_base + url_1980, timeout=10)
        print('Finished requests.get(url_base + url_1980)')
        res.raise_for_status()   # halt program here, if the request failed

        # Use the best HTML parser on my system ("lxml"). 
        soup = bs4.BeautifulSoup( res.text, features="lxml")

    link_elems = soup.select('table ul li a')

    link_list = []
    for lnk in link_elems:
        url = lnk.get('href')
        txt = lnk.getText()

        if not url:           
            # Don't print 'None' for this page's url (1980).
            # Instead add the correct url now, 
            # so it prints each year in numerical order.
            link_list.append(url_1980)
            print(url_1980) 

        elif is_year(txt):
            # A few of the links are not the ones we want,
            # so filter for just the links that look like a year
            link_list.append(url)
            print(url)

    return link_list


#get_links_to_years()
