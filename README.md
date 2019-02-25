# CloutScraper

## Summary
Personal project to explore data collection, analysis, and visualization by webscraping data on songs posted to SoundCloud.com. To do this, I will be using Beautiful Soup and Selenium to collect statitcs for songs of a growing catalogue of artists. Ultimately, I will be tracking plays, comments, and reposts over time, using these features to gauge traction on the platform and forecast whether a track is going to be the next viral hit before it reaches the masses.

## Web-scraping Methodology
To scrape data for tracks over time through artists pages, it is necessary to collect artist urls and then iterate over them. That said, before being able to collect information on plays, comments, likes, and reposts per song, I need repositories of artists' urls that I can scrape. By scraping playlists, I am able to generate a growing catalogue of artists and their links.

### Generating a Catalogue
To collect artist urls, I scrape SoundCould charts for Top50 and for New & Hot tracks for the USA and all music genres. These charts are udated daily and allow us to generate a growing catalogue of urls of artists. 
These pages are static and easily scraped using Beautiful Soup. The Sc_scraper class, constructs a class object that is the url of the page to be scraped based on parameters (url type, genre, and country). By looping through specified parameters in parameters.py, I use the class function chart_scraper to scrapes the page and return a pandas dataframe. Using the Catalogue class, I manage dataframes in the data collection process by creating class functions that perform standard operations.  

### Scraping Artist Pages
Once I have a catalogue of artist urls, I loop over them to scrape data for artist followers, song plays, comments, likes, and reposts. 
Using the Sc_scraper class I create an object that is the url of the artists'  page based on specified parameters (url type, and artist name). SoundCould's artists' tracks pages use lazy loading, so I use Selenium webdriver to open a Chrome Browser. The scrolling class function, scrolls to the bottom of the page until the EOF mark. 
The collect_artist_info class function uses Selenium to find elements on the page based on xpath and class name, collects relevant data, and returns a dataframe for the artist. 

## Visualization
I use Bokeh to make interactive dashboard to monitor the quality of the data scraped at each run of the scraper.

### Data Quality Assurance

