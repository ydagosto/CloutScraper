
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

catalogue = pd.read_csv("sc_hot_and_top.csv")

pd.set_option('display.max_columns', None)

print(catalogue)
#catalogue['runID'] = 1

#catalogue.to_csv("sc_hot_and_top.csv")

value = catalogue['runID'].max()

next_runID = value + 1


