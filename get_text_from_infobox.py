import bs4
import unicodedata
import os

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

    if not tab:       # There is no infobox
        return None

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
            # for every row, remove the <sup> and <style> tags 
            while row.sup:          # if there are <sup> tags in the row,
                row.sup.extract()   # remove them

            while row.style:          # if there are <style> tags in the row,
                row.style.extract()   # remove them

            if att == "from the album":
                if attribHTML.getText(strip=True).startswith("from the album"):
                    return get_from_the_album( attribHTML)

            elif attribHTML.getText(strip=True) == att:
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


def get_from_the_album( attribHTML):
    #print("Calling get_from_the_album")
    #print(attribHTML)
    #print("found the row with 'from the album'")

    # the album title is contained within <i><a> tags
    album_title = attribHTML.find("i")
    if album_title:
        # only get rid of white space at beginning and end
        value = album_title.getText().strip()

        # replace Unicode \xa0 (non-breaking space) with a space
        value = unicodedata.normalize("NFKD", value)
        #print(f"The album title is {value}")
        return value
    else:
        print("ERROR: didn't find <i> tag around the album title")
        return None


def run_fail_tests():
    # Test failing case
    soup = bs4.BeautifulSoup(open('html/Funkytown.html'),
        features='html.parser')
    get_text_from_infobox(soup, 'DoesNotExist')


def run_local_tests(html_filenames, ATTRS):
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


def run_local_tests1():
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

    run_local_tests(html_filenames, ATTRS)


def run_local_tests2():
    ATTRS = ['from the album'
    ]

    html_filenames = [
        'html2/wiki/Cars_(song).html',
        'html2/wiki/Dancing_Queen.html',
        'html2/wiki/Always_on_Time.html',

        # special cases
        # These add a <style> tag that adds unwanted text
        'html2/wiki/Quit_Playing_Games_(With_My_Heart).html',
        'html2/wiki/Back_in_Time_(Pitbull_song).html',
        'html2/wiki/Baby_Boy_(Beyoncé_Knowles_song).html',
        'html2/wiki/Try_Again_(Aaliyah_song).html'
    ]

    run_local_tests(html_filenames, ATTRS)


def run_local_tests3():
    ATTRS = ['from the album'
    ]

    # make a list of all songs in the directory
    dir_list = os.listdir("html2/wiki")

    # make a list with only every nth song
    n = 1   # use 1 to use ALL songs
    html_filenames = ["html2/wiki/" + x
        for i, x in enumerate(dir_list) if i%n==0]

    run_local_tests(html_filenames, ATTRS)


#run_fail_tests()
#run_local_tests1()
#run_local_tests2()
run_local_tests3()
