
parameters = open("parameters.py", 'r').read()
exec(parameters)

# =============================================================================
#current_catalogue = Catalogue(pd.read_csv(catalogue_name, index_col = 0))

#max_run_id, next_run_id = Catalogue.run_id_gen(current_catalogue)

appended_data = Catalogue()
# =============================================================================

chrome_options = Options()  
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(executable_path='../CloutScraper/chromedriver_win32/chromedriver.exe', chrome_options = chrome_options)

artists_urls = list(pd.read_csv(artist_repository, index_col = 0)['artist_url'])

for artist_name in artists_urls:
    artist_url = Sc_scraper("artist", artist_name)
    data = Catalogue(Sc_scraper.artist_scraper(artist_url))\
    .re_index_catalogue()
    
   # appended_data = Catalogue.union_catalogue(appended_data, data)

driver.quit()

appended_data = Catalogue.re_index_catalogue(appended_data)

# =============================================================================

#new_data = Catalogue.union_catalogue(current_catalogue, appended_data)
#new_data = Catalogue.re_index_catalogue(new_data, 'drop index')
	
#Catalogue.save_data(data, song_metrics_data)

# =============================================================================
