
# import packages
import os
import pandas as pd
from bokeh.plotting import *

# Select working Directory
os.chdir("../Data")

# Read in Dataset to do QC on 
catalogue_name = "sc_hot_and_top.csv"

current_catalogue = pd.read_csv(catalogue_name, index_col = 0)

# Unique observations of each column to display
genre_per_run = pd.DataFrame(current_catalogue\
                             .groupby(['runID'])\
                             .genre\
                             .nunique())

countries_per_run = pd.DataFrame(current_catalogue\
                                 .groupby(['runID'])\
                                 .country\
                                 .nunique())

artists_per_run = pd.DataFrame(current_catalogue\
                               .groupby(['runID'])\
                               .artist_name\
                               .nunique())

songs_per_run = pd.DataFrame(current_catalogue\
                             .groupby(['runID'])\
                             .song_name\
                             .nunique())


# Generate Bokeh graphs to display -
# One for Genre and Countries
# Another for songs and artists

# First one is a step line graph of country and genre
# Scrape fixed number of charts -> step 
genre_country = figure(plot_width=600, 
                       plot_height=500,
                       title = "Genres and Country Charts scraped per run",
                       x_axis_label = "Run Number")

genre_country.step(genre_per_run.index.values,
                   genre_per_run['genre'].values,
                   legend = 'Genre',
                   color = 'green',
                   line_width=2)

genre_country.step(countries_per_run.index.values,
                   countries_per_run['country'].values,
                   legend = 'Country',
                   line_width=2)

genre_country.legend.location = "bottom_left"



# Second one is a line graph of artists and songs per run
artist_song = figure(plot_width=600,
                     plot_height=500,
                     title = "Songs and Artists scraped per run",
                     x_axis_label = "Run Number")

artist_song.line(artists_per_run.index.values,
                 artists_per_run['artist_name'].values,
                 legend = 'Artists',
                 line_width=2)

artist_song.line(songs_per_run.index.values,
                 songs_per_run['song_name'].values,
                 legend = 'Songs',
                 color = 'green',
                 line_width=2)


artist_song.legend.location = "bottom_left"

# Put both charts in a GridPlot
qc = gridplot([[genre_country,artist_song]])

#display QC
show(qc)



