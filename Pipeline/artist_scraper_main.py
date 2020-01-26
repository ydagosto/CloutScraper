
parameters = open("parameters.py", 'r').read()
exec(parameters)

log = open(r"./artist_scraper_run_log.log", 'a')
log.write('execution started at ' + str(datetime.datetime.now()))
log.write('\n')
log.close()

# =============================================================================
current_catalogue = Catalogue(pd.read_csv(song_metrics_data, index_col = 0))

empty_df = pd.DataFrame([])
appended_data = Catalogue(empty_df)

# =============================================================================
try:
    chrome_options = Options()  
    chrome_options.add_argument("--headless")
    
    driver = webdriver.Chrome(executable_path='../CloutScraper/chromedriver_win32/chromedriver.exe', chrome_options = chrome_options)
    
    artist_df = pd.read_csv(artist_repository, index_col = 0)
    
    artist_df = artist_df.loc[artist_df['genre'].isin(main_categories)]
    
    artists_urls = list(set(artist_df['artist_url']))
    
    for artist_name in artists_urls:
    	artist_url = Sc_scraper("artist", artist_name)
    	data = Catalogue(Sc_scraper.artist_scraper(artist_url))
    		
    	appended_data = Catalogue.union_catalogue(appended_data, data)
    
    driver.quit()
    
    appended_data = Catalogue.re_index_catalogue(appended_data, 'drop')

# =============================================================================

    new_data = Catalogue.union_catalogue(current_catalogue, appended_data)
    new_data = Catalogue.re_index_catalogue(new_data, 'drop index')
    		
    Catalogue.save_data(new_data, song_metrics_data)

# ==========================================================================
    # Log Run
    log = open(r"./artist_scraper_run_log.log", 'a')
    
    # Write date/time
    log.write('execution successful at ' + str(datetime.datetime.now()))
    log.write('\n')
    log.close()


# If fails then log that the run failed
except:
    # Log Run
    log = open(r"./artist_scraper_run_log.log", 'a')
    
    # Write date/time
    log.write('execution failed at ' + str(datetime.datetime.now()))
    log.write('\n')
    log.close()
