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

api_genre_country_combos = list(product(api_types, genres, countries))


#function to take api url and take all songs with publisher and urls
def eager_playlist_scraper(api_url, api_type, genre ,country):
    
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
          "playlist": api_url}
    
    data = pd.DataFrame(df, columns = ['artist_url',
                                       'artist_name',
                                       'song_url',
                                       'song_name',
                                       'country',
                                       'genre',
                                       "playlist_type",
                                       'run_date',
                                       'playlist'])
    
    
    pd.set_option('display.max_columns', None)
    
    return data

appended_data = pd.DataFrame([], columns = ['artist_url', 
                             'artist_name',
                             'song_url',
                             'song_name',
                             'country',
                             'genre',
                             'playlist_type'
                             'run_date',
                             'playlist'])

for api_type, genre, country in api_genre_country_combos:
    api_url = api1 + api_type +"genre=" + genre +"&country=" + country
    data = eager_playlist_scraper(api_url, api_type, genre ,country)
    
    appended_data = pd.concat([appended_data, data])
    
print(appended_data)


appended_data.to_csv("hot_new.csv")
