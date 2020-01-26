"""
Script to scrape artists urls from all charts page on SoundCloud.
Cycle through all combinations of country and genre, for top50 and new.
The data pulled is going to be a catalogue of artists we are going to find
urls for and pull streaming data for. 
This will include data for artist, track url and name. Keeping only distincts
"""

parameters = open("parameters.py", 'r').read()
exec(parameters)

log = open(r"./chart_scraper_run_log.log", 'a')
log.write('execution started at ' + str(datetime.datetime.now()))
log.write('\n')
log.close()

# =============================================================================
current_catalogue = Catalogue(pd.read_csv(catalogue_name, index_col = 0))

appended_data = Catalogue()

# Error handling: Attempt to run the scraper
try:
    # Loop through all combinations and append the data
    for chart_type, genre, country in api_genre_country_combos:
        chart_url = Sc_scraper("charts", chart_type, genre, country)
        data = Catalogue(Sc_scraper.chart_scraper(chart_url))
        
        appended_data = Catalogue.union_catalogue(appended_data, data)
    
    # Reset and rename index
    appended_data = Catalogue.rename_index(appended_data, 'chart_num')
    appended_data = Catalogue.re_index_catalogue(appended_data)
    
    # ==========================================================================
    # Union to catalogue, clean up, and save
    new_data = Catalogue.union_catalogue(current_catalogue, appended_data)
    new_data = Catalogue.re_index_catalogue(new_data, 'drop index')
    
    Catalogue.save_data(new_data, catalogue_name)
    
    clean_up_artists, clean_up_songs = Catalogue.clean_up_catalogue(
            Catalogue(pd.read_csv(catalogue_name, index_col = 0))
            )
            
    Catalogue.save_data(clean_up_artists, artist_repository)
    Catalogue.save_data(clean_up_songs, song_repository)

	# ==========================================================================
    # Log Run
    log = open(r"./chart_scraper_run_log.log", 'a')
    
    # Write date/time
    log.write('execution successful at ' + str(datetime.datetime.now()))
    log.write('\n')
    log.close()


# If fails then log that the run failed
except:
    # Log Run
    log = open(r"./chart_scraper_run_log.log", 'a')
    
    # Write date/time
    log.write('execution failed at ' + str(datetime.datetime.now()))
    log.write('\n')
    log.close()
