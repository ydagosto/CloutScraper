"""
Script to scrape artists urls from all charts page on SoundCloud.
Cycle through all combinations of country and genre, for top50 and new.
The data pulled is going to be a catalogue of artists we are going to find
urls for and pull streaming data for. 
This will include data for artist, track url and name. Keeping only distincts
"""

parameters = open("parameters.py", 'r').read()
exec(parameters)

#==============================================================================

current_catalogue = Catalogue(pd.read_csv(catalogue_name, index_col = 0))

max_run_id, next_run_id = Catalogue.run_id_gen(current_catalogue)

appended_data = Catalogue()

# Loop through all combinations and append the data
for chart_type, genre, country in api_genre_country_combos:
    chart_url = Sc_scraper("charts", chart_type, genre, country)
    data = Catalogue(Sc_scraper.chart_scraper(chart_url, next_run_id))
    
    appended_data = Catalogue.union_catalogue(appended_data, data)


# reset index and rename indez
appended_data = Catalogue.rename_index(appended_data, 'chart_num')
appended_data = Catalogue.re_index_catalogue(appended_data)

new_data = Catalogue.union_catalogue(current_catalogue, appended_data)
new_data = Catalogue.re_index_catalogue(new_data, 'drop index')

Catalogue.save_data(new_data, catalogue_name)
