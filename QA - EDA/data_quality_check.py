
# import packages
import os
import pandas as pd
import pathlib
import datetime as dt
from bokeh.plotting import *
from bokeh.models import Div

dashboard_title = Div(text='<h1> Artist Catalog Scraper QA</h1>',
                      width=1500,
                      height=15,
                      style={'textAlign': 'center'})

# Read in Dataset to do QC on
catalogue_name = "../../Data/sc_hot_and_top.csv"

current_catalogue = pd.read_csv(catalogue_name, index_col = 0)

aggregation = {"genre" : {"genre" : "nunique"}
,"country" : {"country" : "nunique"}
,"artist_name" : {"artist_name" : "nunique"}
,"song_name" : {"song_name" : "nunique"}
}

dataframe = pd.DataFrame(current_catalogue)

# Unique observations of each column to display
stats_per_run = dataframe\
.groupby(['run_id'])\
.agg(aggregation)\
.reset_index()

stats_per_run.columns = ['run_id', 'genre', 'country', 'artist_name','song_name']

# Generate Bokeh graphs to display -
# One for Genre and Countries
# Another for songs and artists

# First one is a step line graph of country and genre
# Scrape fixed number of charts -> step 
genre_country = figure(plot_width=750, 
                       plot_height=295,
                       title = "Genres and Country Charts scraped per run",
                       x_axis_label = "Run Number")

genre_country.step(stats_per_run['run_id'].values,
                   stats_per_run['genre'].values,
                   legend = 'Genre',
                   color = 'red',
                   line_width=2)

genre_country.step(stats_per_run['run_id'].values,
                   stats_per_run['country'].values,
                   legend = 'Country',
                   line_width=2)

genre_country.legend.location = "bottom_left"



# Second one is a line graph of artists and songs per run
artist_song = figure(plot_width=750,
                     plot_height=295,
                     title = "Songs and Artists scraped per run",
                     x_axis_label = "Run Number",
                     x_range = genre_country.x_range)

artist_song.line(stats_per_run['run_id'].values,
                 stats_per_run['artist_name'].values,
                 legend = 'Artists',
                 line_width=2)

artist_song.line(stats_per_run['run_id'].values,
                 stats_per_run['song_name'].values,
                 legend = 'Songs',
                 color = 'red',
                 line_width=2)


artist_song.legend.location = "bottom_left"

##### First and Last Seen by Distinct Artist
## last seen artist

run_id_agg = {
        'run_id':{'frist_seen': 'min',
                 'last_seen' : 'max'}
        }
    
ids_per_artist = dataframe\
.groupby(['artist_name'])\
.agg(run_id_agg)\
.reset_index()

ids_per_artist.columns = ['artist_name', 'first_seen', 'last_seen']

artists_per_max_date = ids_per_artist\
.groupby(['last_seen'])\
.artist_name\
.count()\
.reset_index(drop = False)\
.rename_axis('index')\
.sort_values('last_seen')

# first seen artists

artists_per_min_date = ids_per_artist\
.groupby(['first_seen'])\
.artist_name\
.count()\
.reset_index(drop = False)\
.rename_axis('index')\
.sort_values('first_seen')

found_chart = figure(plot_width=750,
                          plot_height=295,
                          title = "Number of Distinct Artists First and Last Seen",
                          x_axis_label = "Run Number",
                          x_range = genre_country.x_range)

found_chart.line(x = artists_per_min_date['first_seen'].values,
                     y = artists_per_min_date['artist_name'].values,
                     line_width=2,
                     legend = 'First Seen')

found_chart.line(x = artists_per_max_date['last_seen'].values,
                     y = artists_per_max_date['artist_name'].values,
                     line_width = 2,
                     color='red',
                     legend = 'Last Seen')

found_chart.legend.location = "bottom_left"



# Put both charts in a GridPlot
qc = gridplot([[dashboard_title],
               [genre_country,artist_song],
               [found_chart]])




#display QC
show(qc)




