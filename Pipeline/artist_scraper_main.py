
parameters = open("parameters.py", 'r').read()
exec(parameters)

# =============================================================================
#current_catalogue = Catalogue(pd.read_csv(catalogue_name, index_col = 0))

#max_run_id, next_run_id = Catalogue.run_id_gen(current_catalogue)

empty_df = pd.DataFrame([])
appended_data = Catalogue(empty_df)
# =============================================================================

chrome_options = Options()  
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(executable_path='../CloutScraper/chromedriver_win32/chromedriver.exe', chrome_options = chrome_options)

artist_df = pd.read_csv(artist_repository, index_col = 0)

artist_df = artist_df.loc[artist_df['genre'].isin(main_categories)]

artists_urls = list(set(artist_df['artist_url']))

for artist_name in artists_urls:
    artist_url = Sc_scraper("artist", artist_name)
    data = Catalogue(Sc_scraper.artist_scraper(artist_url, 0))
    
    appended_data = Catalogue.union_catalogue(appended_data, data)

driver.quit()

appended_data = Catalogue.re_index_catalogue(appended_data, 'drop')

# =============================================================================

#new_data = Catalogue.union_catalogue(current_catalogue, appended_data)
#new_data = Catalogue.re_index_catalogue(new_data, 'drop index')
	
Catalogue.save_data(appended_data, song_metrics_data)

# =============================================================================
