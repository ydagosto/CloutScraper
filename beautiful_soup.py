#import packages
import os
import urllib.request
from bs4 import BeautifulSoup
from bs4 import SoupStrainer


#set working directory
os.chdir("c:\\Users\Yuri D'Agosto\Desktop\SlapScience")

#lists to pack with data
song_url_list = []#list containing song url soundcloud extensions
song_name_list = []#list containing song names as the appear on site
artist_url_list = []#list containing artist url soundcloud extensions
artist_name_list = []#list containing artist url as appear on site

#cycle variable for loop
i = 0 #track if song (=0) or artist (=1)

#url of soundcloud page to scrape + read from page using urllib
api_url = "https://soundcloud.com/charts/new?genre=hiphoprap&country=US"
content = urllib.request.urlopen(api_url).read()

## parse out article sections and pattern with second headers (h2) and 'a' child
only_tags_with_h2 = SoupStrainer("article")

soup = BeautifulSoup(content,
                     "html.parser",
                     parse_only=only_tags_with_h2)\
                     .select('h2 > a')

#
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
    

print(artist_url_list)

print(artist_name_list)

print(song_url_list)

print(song_name_list)
