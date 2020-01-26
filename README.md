# CloutScraper

## Summary
Personal project to explore data collection, analysis, and visualization by webscraping data on songs posted to SoundCloud.com. To do this, I will be using Beautiful Soup and Selenium to collect statitcs for songs of a growing catalogue of artists. Ultimately, I will be tracking plays, comments, and reposts over time, using these features to gauge traction on the platform and forecast whether a track is going to be the next hit.

## Web-Scraping Methodology
By scraping playlists, I generate a growing catalogue of artists and their links. After that, I iterate over artis page urls and scrape information on plays, comments, likes, and reposts for each song. Iterating over artist pages allows me to scrape data for tracks over time.

### Generating a Catalogue of Artists
To collect artist urls, I scrape SoundCould charts for Top50 and for New & Hot tracks for the USA and all music genres. These charts are udated daily and allow us to generate a growing catalogue of urls of artists. 
These pages are static and easily scraped using Beautiful Soup. The Sc_scraper class, constructs a class object that is the url of the page to be scraped based on parameters (url type, genre, and country). By looping through specified parameters in parameters.py, I use the class function chart_scraper to scrapes the page and return a pandas dataframe. Using the Catalogue class, I manage dataframes in the data collection process by creating class functions that perform standard operations.  

### Scraping Artists' Pages
Once I have a catalogue of artist urls, I loop over them to scrape data for artist followers, song plays, comments, likes, and reposts. 
Using the Sc_scraper class I create an object that is the url of the artists'  page based on specified parameters (url type, and artist name). SoundCould's artists' tracks pages use lazy loading, so I use Selenium webdriver to open a Chrome Browser. The scrolling class function, scrolls to the bottom of the page until the EOF mark. 
The collect_artist_info class function uses Selenium to find elements on the page based on xpath and class name, collects relevant data, and returns a dataframe for the artist. 

#### Notes
- To run this you will need to download a chromedriver to run on selenium. Include the path to your chrome driver at line 21 of the artist_scraper_main.py script - driver = webdriver.Chrome(executable_path='/yourpath/chromedriver.exe', options = chrome_options
- The data is going to be generated in the ../Data folder which includes empty csv's to be populated at the first run of the scraper
