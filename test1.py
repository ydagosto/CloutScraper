import os
import urllib.request
import yaml
import pandas as pd
from bs4 import BeautifulSoup



os.chdir("c:\\Users\Yuri D'Agosto\Desktop\SlapScience")

api_url = "https://soundcloud.com/charts/new?genre=hiphoprap&country=US"

content = urllib.request.urlopen(api_url).read()
soup = BeautifulSoup(content)

for article in soup.find_all('h2'):
    print("HTML", article, "TEXT" , article.text, article.next_sibling)
    
# =============================================================================
# print(soup.prettify())
# =============================================================================
