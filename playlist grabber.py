#import packages
import os
import urllib.request
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import pandas as pd
import datetime

now = datetime.datetime.now()

#set working directory
os.chdir("c:\\Users\Yuri D'Agosto\Desktop\SlapScience")

api1 = "https://soundcloud.com/charts/top"

#url of soundcloud page to scrape + read from page using urllib
content = urllib.request.urlopen(api_url).read()

print(content)

