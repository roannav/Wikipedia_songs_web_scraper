# Take all the csv files: output/songs_####.csv    (1946 - 2021)
# Add a column for the year and move the song_URL column to the end.
# Finallly concat all the files together into 1 large file

import pandas as pd
from pandas import DataFrame, Series

FIRST_YEAR = 1946
LAST_YEAR = 2021

input_files = [ "output/songs_" + str(year) + ".csv" 
                for year in range(FIRST_YEAR, LAST_YEAR + 1)] 

columns = ['rank', 'song_URL', 'title', 'artist']

df_list = []
for f in input_files:
    # header=0   ==> use the first row as the column headers
    # names=columns ==> replace the headers from the csv file
    #                   with the values in 'columns'
    df_list.append( pd.read_csv(f, header=0, names=columns))

# Originally the columns were ['No.', 'Song URL', 'Title', 'Artist(s)']
# But I've renamed the columns to ['rank', 'song_URL', 'title', 'artist']
# print("Columns are", df_list[0].columns) 
# print(len(df_list[0]))    # 41 
# print("First title is", df_list[0].title[0])


# fix the datasets.
# add a column at the column 0 location for the year.
for year in range(FIRST_YEAR, LAST_YEAR + 1):
    i = year - FIRST_YEAR 
    num_rows = len(df_list[i])
    new_column = [year] * num_rows   # an array with the same year repeated
    df_list[i].insert(0, "year", new_column, True)

# columns are ['year', 'rank', 'song_URL', 'title', 'artist']

# move the 2nd column 'song_URL' to the end
for i, df in enumerate(df_list):
    cols = df.columns.tolist()
    cols2 = cols[0:2] + cols[3:] + [cols[2]]
    df_list[i] = df[cols2]

# columns are ['year', 'rank', 'title', 'artist', 'song_URL']


full_df = pd.concat(df_list)

# convert DataFrame into csv 
# index=False  means to not add an extra index column
filename = f"output/Billboard_{FIRST_YEAR}_to_{LAST_YEAR}.csv"
full_df.to_csv(filename, index=False)
