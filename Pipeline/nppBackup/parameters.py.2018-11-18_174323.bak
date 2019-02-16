# import packages
import os
import urllib.request
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import pandas as pd
import datetime
from itertools import product
import re

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Class with webscraping driver based on api url
scraper_class = open("scraper_class.py", 'r').read()
exec(scraper_class)

# Class managing catalogue dataframes
catalogue_class = open("catalogue_class.py", 'r').read()
exec(catalogue_class)

# set working directory where you'll be saving data and name of data file in store or to create
# In this case this is going to be outside of pipeline folder and inside the slapscience master
os.chdir("../../Data")

catalogue_name = "sc_hot_and_top.csv"
artist_repository = "artist_repository.csv"
song_repository = "song_repository.csv"
song_metrics_data = "song_metrics.csv"

# ==============================================================================
# === CHARTS URLS
# charts will be new and top and for each available country and genre
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
			  
# generate all combinations of api type, genre, and country
api_genre_country_combos = list(product(api_types, genres, countries))

# ==============================================================================