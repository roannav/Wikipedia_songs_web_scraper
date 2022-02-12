import bs4
import unicodedata

# Grab certain text, specified by 'att',  from the infobox in the soup
# of a Wikipedia song page.
#
# Looks at the Wikipedia webpage, which is represented by soup.
# It finds the *first* infobox in the page.
# The infobox has many attribute-value pairs. 
# It searches for the specified att attribute,
# and then prints and returns the matching value
# or None, if no match.
def get_text_from_infobox( soup, att):

    # get infobox     <table class="infobox">
    tab = soup.find("table", class_='infobox')   
    #tab = soup.find('table', {'class': 'infobox'}) # WORKS ALSO!
    #tab = soup.select(".infobox")[0]               # WORKS ALSO! 

    # infobox may include content that is not displayed.
    # <td class="infobox-data plainlist">October&#160;7,&#160;2019
    # <span style="display:none">&#160;(<span class="bday dtstart
    # published updated">2019-10-07</span>)</span></td>

    hidden = tab.find_all(style="display:none")
    for h in hidden:
        h.extract()   # don't scrape content that is hidden

    rows = tab.find_all("tr")


    # look for the row, which has the <th> containing the attribute we want
    for row in rows:
        # Note in the infobox for the Wikipedia page on 'Funkytown.html',
        # some rows have <th> and some don't:
        # first row: <th> title
        # second row: image
        # third row: <th> description
        attribHTML = row.find("th")
        if attribHTML:
            if attribHTML.getText(strip=True) == att:
                # found the row we want.
                # row may look like...
                # <tr><th class="infobox-label" scope="row">Released</th>
                #   <td class="infobox-data plainlist">March 1980
                #     <sup class="reference" id="cite_ref-1">
                #     <a href="#cite_note-1">[1]</a></sup></td></tr>
                while row.sup:          # if there are <sup> tags in the row,
                    row.sup.extract()   # remove them

                value = ""
                # get the text from the <td> element only, not from <th>

                # if there is a list, inside of the <td>, then separate 
                # the list items by adding a comma
                if row.find("li"):
                    lis = row.find_all("li")
                    for li in lis:
                        value += li.getText( strip=True) + ", "
                    value = value[:-2]    # remove comma and space for last one

                else:
                    # if there are items, separated by <br>, then
                    # separate them by adding a comma.
                    # <td><a href="">Burt</a><br /><a href="">Hal</a></td>
                    # ===> Burt, Hal
                    brs = row.find_all("br")
                    for br in brs:
                        br.replaceWith(', ')

                    # only get rid of white space at beginning and end of <td>
                    value = row.find("td").getText().strip()

                    # NOTE: getText( strip=True) removes whitespace from 
                    # the children too...
                    # <td><a href="">Paul</a> and <a href="">Lee</a></td>
                    # ===> PaulandLee

                # replace Unicode \xa0 (non-breaking space) with a space
                value = unicodedata.normalize("NFKD", value)

                #print(value)
                return value

    #print(f"Couldn't find attribute '{att}' in the Wikipedia infobox.")
    return None


def run_local_tests():
    # Look at a Wikipedia page, which usu. has these attributes in an infobox
    ATTRS = ['A-side', 'B-side',
        'Recorded', 'Studio',
        'Released', 'Published', 'Label',
        'Genre', 'Length',
        'Songwriter(s)', 'Producer(s)',
        'Composer(s)', 'Lyricist(s)'
    ]
    
    html_filenames = [
        'html/Funkytown.html',
        'html/Upside_Down.html',
        'html/Catch_a_Falling_Star1958.html',
        'html/Magic_Moments1958.html',
        'html/Stood_Up1958.html',
        'html/Heartaches1947.html',
        'html/I_Hope_Youre_Happy_Now2020.html'
    ]

    for f in html_filenames:
        soup = bs4.BeautifulSoup(open(f), features='html.parser')
        values = []
        for att in ATTRS:
            value = get_text_from_infobox(soup, att)
            if value == None:
                #value = '\u00D8'  # null symbol
                value = '\u2588'  # white block;  make it easily visible
            values.append(value)

        print(list(zip(ATTRS, values)),'\n')

    # Test failing case
    soup = bs4.BeautifulSoup(open(html_filenames[0]), features='html.parser')
    get_text_from_infobox(soup, 'DoesNotExist')


run_local_tests()
