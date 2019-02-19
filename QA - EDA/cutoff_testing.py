### Testing to find hard cut off for artists not to scrape. 
#When an artist posts too many tracks, it will become inefficient for us to scrape their tracks.
# I try to find out what is the ideal cutoff that allows to capture the majority of artists and not 
# scrape outliers with too many tracks posted. 
#we use one run of the scraper where we scraped fully almost 3000 artsits.

import pandas as pd
import matplotlib.pyplot as plt

#data
sample_data = "../../Data/song_metrics.csv"

df = pd.read_csv(sample_data, index_col = 0)

#find songs per artsit
songs_by_artist = df\
.groupby('artist_name')\
.song_name\
.nunique()\
.reset_index()

songs_by_artist.columns = ['artist_name', 'total_songs']

#distribution of total tracks uploaded by artist
plt.hist(songs_by_artist['total_songs'].values, bins=75)
plt.show()


#Number of Channels with over 750 songs
large_channels = songs_by_artist[songs_by_artist['total_songs'] >= 750]\
.artist_name\
.count()

print("Artists with over 750 tracks uploaded: " + str(large_channels))

#Total number of channels
total_channels =  songs_by_artist\
.artist_name\
.count()

print("Total Artists: " + str(total_channels))

#Percent of scraped Artists at cutoff
pct_colletcted = round(1 - large_channels/total_channels, 3)

print("Percent of Channels Captured: " + str(pct_colletcted))