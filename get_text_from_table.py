import bs4
import pandas as pd

# This parses a particular type of wikipedia page,
# for Billboard songs, which is represented by 'soup'.
# It finds the *first* table in the BeautifulSoup 'soup'.
# It grabs the first row and puts it into 'cols' (a list).
# It grabs the rest of the data and puts it into 'data' (2D list).
# As it processes the table info, it removes the HTML, 
# any <sup> tag (including the text within), and 
# extra spaces before and after the text.
#
# IN: add_song_url_column: default is false
#     If true, it adds an extra column for the song url.
#
# IN: table_class: a string, which gets passed to soup.find()
#     which identifies which table to select.  It looks for a 
#     table with CSS class attribute: table_class
#
# Returns (data, cols)
def get_text_from_table(soup, 
                        add_song_url_column=False,
                        table_class=None):

    data = []   # list of lists; 2D array

    # use the first table found, that matches the class, if specified
    if table_class:
        tab = soup.find("table", class_=table_class)
    else:
        tab = soup.find("table")

    has_class( tab, table_class)

    if not tab:
        print("WARNING: get_text_from_table(): Couldn't find a table")
        print(f"  with the class: {table_class}")
        return None, None

    # the first row has the header 
    header = tab.find("tr")

    #strip=True  removes whitespace from beginning and end of the string 
    cols = [ col.getText( strip=True) for col in header.find_all("th")]
    if add_song_url_column:
        cols.insert(1, 'Song URL')


    # The rest of the rows have the table data.
    table_data = tab.find_all("tr")[1:]

    for tr in table_data:
        row = build_row(tr, add_song_url_column)
        data.append(row)
    
    return data, cols


# if class_name is specified,
# then determine whether it's in the classes listed for the element.
# otherwise return it has any classes.
def has_class( element, class_name=None):
    if element:
        if "class" in element.attrs:
            classes = element.attrs["class"]
            print(f"This element has the CSS classes: {classes}")

            if class_name:   
                if class_name in classes:
                    print(f"Found {class_name} in classes.")
                    return True   # it has a matching class
                else:
                    print(f"Did NOT find {class_name} in classes.")
                    return False  # it has a class, but NOT matching
            return True  # it has at least 1 class
    return False   # it has no class attribute


def has_rowspan( td):
    return td and ("rowspan" in td.attrs)


# returns the row, as a list, but with just text (no html) of each td cell
def build_row(tr, add_song_url_column):
    row = []
    tds = tr.find_all("td")

    # This is the index in the list of tds we are looking at. 
    # This may be different than which column of the main table.
    index = 0  

    if has_rowspan(tds[0]):
        # sometimes the first td contains something like "50 (Tie)" 
        # and has rowspan="2"
        print("There's a tie!")
        # This will offset the index of the tds in the next row.

    if len(tds) == 2:
        # If there are only 2 columns in this row,
        # it's because there was a rowspan in the first td of previous row.
        # This happens when there's a tie in the rankings.
        prev_row = tr.find_previous_sibling('tr')    
        # FIXME: This assumes only a 2-way tie.
        rank = prev_row.find("td").getText()
    else:
        # remove the newline (eg in Billboard Top 100 in 2021) 
        rank = tds[index].getText(strip=True)
        index += 1

    row.append(rank)

    if add_song_url_column:
        link = None
        if tds[index].find("a"):
            link = tds[index].find("a").attrs["href"] 
        row.append(link)


    '''
    Sometimes there is an extra <sup> tag, as below.  Remove it.
    <td>"<a href="/wiki/Babe_(Styx_song)" title="Babe (Styx song)">Babe</a>"
    <sup id="cite_ref-Note1979_3-1" class="reference">
        <a href="#cite_note-Note1979-3">&#91;Notes 1&#93;</a>
    </sup>
    </td>

    Sometimes the title (or part of the title is not in an <a> tag.
    So we can NOT just select the text from the <a> tag.
    Instead remove the <sup> tag.
    '''
    if tds[index].sup:             # if there is a <sup> tag in tds[index],
        tds[index].sup.extract()   # remove it

    # The second td has an extra pair of quotes which encloses the title
    # like this...
    # <td>"<a href="/wiki/Call_Me_(Blondie_song)" 
    # title="Call Me (Blondie song)">Call Me</a>"</td>

    # Remove the extra quotes via the slice [1:-1].
    # Also extract() can add extra whitespace, so strip the whitespace.
    title = tds[index].getText(strip=True)[1:-1]

    # Sometimes there are 2 songs (both A-side and B-side of the record) 
    # listed in the Billboard songs of 1958. 
    # The other years only list 1 song per rank.
    # Each song has an extra pair of quotes, like this:
    # <td>"<a href="/wiki/Bird_Dog_(song)" title="Bird Dog (song)">Bird Dog</a>" / "<a href="/wiki/Devoted_to_You_(song)" title="Devoted to You (song)">Devoted to You</a>"</td>

    # remove inner quotes " that are next to the / that separates the 2 songs
    title = title.replace('" / "', ' / ')
    row.append(title)
    index += 1

    # The third td ends with an extra '\n' at the end.  Remove it.
    row.append(tds[index].getText()[:-1])
    return row


def convert_table_to_csv( data, cols, csv_filename):
    # convert lists into Pandas DataFrame
    df = pd.DataFrame(data = data, columns = cols)

    # convert DataFrame into csv 
    # index=False  means to not add an extra index column
    df.to_csv(csv_filename, index=False)

    # NOTE: some of the titles in the csv will have quotes around them.
    # That's because there is a comma in the title.
    # So we need quotes around the whole title to show that they are not
    # separate entries in the csv.

    # NOTE: the Wikipedia links to the song pages will often contain 
    # URL Encoding (eg %20 replaces a space.   %27 replaces a '  )


def run_tests():
    '''
    html_filename = 'html/Billboard_Top_in_1980.html'
    soup = bs4.BeautifulSoup(open(html_filename), features='html.parser')
    data, cols = get_text_from_table(soup, True)
    convert_table_to_csv( data, cols, 'output/output.csv')

    html_filename = 'html/Billboard_Top_in_1980.html'
    soup = bs4.BeautifulSoup(open(html_filename), features='html.parser')
    data, cols = get_text_from_table(soup, False)
    convert_table_to_csv( data, cols, 'output/output2.csv')

    html_filename = 'html/Billboard_Top_in_1980.html'
    soup = bs4.BeautifulSoup(open(html_filename), features='html.parser')
    data, cols = get_text_from_table(soup, True, "wikitable")
    convert_table_to_csv( data, cols, 'output/output3.csv')
    '''

    html_filename = 'html/Billboard_Top50_in_1958.html'
    soup = bs4.BeautifulSoup(open(html_filename), features='html.parser')
    data, cols = get_text_from_table(soup, True, "wikitable")
    convert_table_to_csv( data, cols, 'output/output4.csv')
    
    html_filename = 'html/Billboard_Top100_in_2012.html'
    soup = bs4.BeautifulSoup(open(html_filename), features='html.parser')
    data, cols = get_text_from_table(soup, True, "wikitable")
    convert_table_to_csv( data, cols, 'output/output5.csv')

    html_filename = 'html/Billboard_Top100_in_2020.html'
    soup = bs4.BeautifulSoup(open(html_filename), features='html.parser')
    data, cols = get_text_from_table(soup, True, "wikitable")
    convert_table_to_csv( data, cols, 'output/output6.csv')

    '''
    html_filename = 'html/Billboard_Top100_in_2021.html'
    soup = bs4.BeautifulSoup(open(html_filename), features='html.parser')
    data, cols = get_text_from_table(soup, True, "wikitable")
    convert_table_to_csv( data, cols, 'output/output7.csv')
    '''

#run_tests()
