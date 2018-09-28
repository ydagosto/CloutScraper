
"""
Script to scrape artists urls from all charts page on SoundCloud.
Cycle through all combinations of country and genre, for top50 and new.
The data pulled is going to be a catalogue of artists we are going to find
urls for and pull streaming data for. 
This will include data for artist, track url and name. Keeping only distincts
"""

#import packages
import os
import urllib.request
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import pandas as pd
import datetime
from itertools import product

now = datetime.datetime.now()

#set working directory
os.chdir("c:\\Users\Yuri D'Agosto\Desktop\SlapScience")

#==========================================================================
#Set run parameters

catalogue_name = "sc_hot_and_top.csv"
url = "https://soundcloud.com/charts/"

#charts will be new and top and for each available country and genre
api_types = ["top", "new"]

countries = ['AU', 'CA', 'FR', 
             'DE', 'IE', 'NL', 
             'NZ', 'GB', 'US', 
             'all-countries']

genres = ['alternativerock', 'ambient', 'classical',
              'country', 'danceedm', 'dancehall',
              'deephouse', 'disco', 'drumbass',
              'dubstep', 'electronic','folksingersongwriter',
              'all-music', 'all-audio']
			  
#generate all combinations of api type, genre, and country
api_genre_country_combos = list(product(api_types, genres, countries))

#==========================================================================
#read in current catalogue and find max RunID
#generate new runID

current_catalogue = pd.read_csv(catalogue_name, index_col = 0)

max_runID = current_catalogue['runID'].max()

next_runID = max_runID + 1

#==========================================================================
#function to take api url and take all songs with publisher and urls
def eager_playlist_scraper(api_url, api_type, genre ,country, run_number):
    
    #url of soundcloud page to scrape + read from page using urllib
    content = urllib.request.urlopen(api_url).read()
    
    #lists to pack with data
    song_url_list = []#list containing song url soundcloud extensions
    song_name_list = []#list containing song names as the appear on site
    artist_url_list = []#list containing artist url soundcloud extensions
    artist_name_list = []#list containing artist url as appear on site
    
    #cycle variable for loop
    i = 0 #track if song (=0) or artist (=1)
    
    ## parse out article sections and pattern with second headers (h2) and 'a' child
    only_tags_with_h2 = SoupStrainer("article")
    
    soup = BeautifulSoup(content,
                         "html.parser",
                         parse_only=only_tags_with_h2)\
                         .select('h2 > a')
    
    for article in soup:
    
        if i == 0 :
            column_name = "song"
            song_url_list.append(str(article.get('href', '/')))
            song_name_list.append(str(article.text))
            i = i + 1
        else:
            column_name = "artist"
            artist_url_list.append(str(article.get('href', '/')))
            artist_name_list.append(str(article.text))
            i = i - 1
    
    df = {"artist_url":artist_url_list, 
          "artist_name" : artist_name_list,
          "song_url" : song_url_list,
          "song_name" : song_name_list,
          "country" : country,
          "genre" : genre,
          "playlist_type" : api_type,
          "run_date" : now,
          "playlist": api_url,
          "runID": run_number}
    
    data = pd.DataFrame(df, columns = ['artist_url',
                                       'artist_name',
                                       'song_url',
                                       'song_name',
                                       'country',
                                       'genre',
                                       "playlist_type",
                                       'run_date',
                                       'playlist',
                                       'runID'])
    
    
    pd.set_option('display.max_columns', None)
    
    return data

#==========================================================================
#implement function, loop it over all possible combnations for catalogue

#generare empty data set, this will be the catalugue
appended_data = pd.DataFrame([], columns = ['artist_url', 
                             'artist_name',
                             'song_url',
                             'song_name',
                             'country',
                             'genre',
                             'playlist_type',
                             'run_date',
                             'playlist',
                             'runID'])

#Loop through all combinations and append the data
for api_type, genre, country in api_genre_country_combos:
    api_url = url + api_type +"?genre=" + genre +"&country=" + country
    data = eager_playlist_scraper(api_url, api_type, genre ,country, next_runID)
    data.index = data.index + 1
    
    appended_data = pd.concat([appended_data, data])\
                      .rename_axis("chart_num")

#reset index and rename indez
appended_data = appended_data\
                .reset_index()\
                .rename_axis('index')
    
#append to larger table
current_catalogue = pd.concat([current_catalogue, appended_data])\
                      .reset_index(drop = True)\
                      .rename_axis('index')


#save the data sets
current_catalogue.to_csv("sc_hot_and_top.csv")
