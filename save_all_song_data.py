# html2/wiki contains the Wikipedia pages about individual songs.
# Scans the song pages for the attributes listed in ALL_ATTRS. 
# Outputs and saves all the data found to the output_all_filename.

import bs4
import os
from get_text_from_infobox import get_text_from_infobox
from get_text_from_table import convert_table_to_csv

output_all_filename = 'output/Billboard_all.csv'

def get_more_data_for_all_songs():
    # Look at a Wikipedia page, which usu. has these attributes in an infobox
    ALL_ATTRS = ['A-side', 'B-side', 'from the album',
        'Recorded', 'Studio',
        'Released', 'Published', 'Label',
        'Genre', 'Length',
        'Songwriter(s)', 'Producer(s)',
        'Composer(s)', 'Lyricist(s)',
        'Music video'
    ]
    
    # make a list of all songs in the directory
    dir_list = os.listdir("html2/wiki")

    # prefix the path
    html_filenames = ["html2/wiki/" + f for f in dir_list]

    table = []
    for f in html_filenames[:10]:
        #print(f)
        soup = bs4.BeautifulSoup(open(f), features='html.parser')
        values = [f]
        for att in ALL_ATTRS:
            value = get_text_from_infobox(soup, att)
            values.append(value)

        #print(values,'\n')
        table.append(values)

    print(table[:5])  # first 5 rows
    cols = ["URL"] + ALL_ATTRS
    print(cols)
    convert_table_to_csv( table, cols, output_all_filename)


get_more_data_for_all_songs()
