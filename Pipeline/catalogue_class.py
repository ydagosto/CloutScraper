"""
Class to organize catalogues of artists.
These are just pandas dataframes in standard format.
"""
class Catalogue:

	# Class object catalogue is a pandas dataframe -> self.catalogue.
	# run the constructor with nothing specified and it will generate
	# an empty catalogue dataframes with standard columns.
	def __init__(self, artist_catalogue = None):
		if artist_catalogue is None:
			self.catalogue = pd.DataFrame([], columns = [
			'artist_url',
			'artist_name',
            'song_url',
            'song_name',
            'country',
            'genre',
			'playlist_type',
            'run_date',
            'playlist'])
		else:
			self.catalogue = artist_catalogue
		
	
	# To print info on the dataframe
	def print_info_catalogue(self):
		
		pd.set_option('display.max_columns', None)
		
		print(self.catalogue.info())
		
		
	# To print the dataframe
	def print_catalogue(self):
		
		pd.set_option('display.max_columns', None)
		
		print(self.catalogue)
		
		return
	
	
	# Takes in catalogue, retuns tuple of max run_id and next run_id	
	def run_id_gen(self):
	
		max_run_id = self.catalogue['run_id'].max()
		next_run_id = max_run_id + 1

		return max_run_id, next_run_id
	
	# Concatenates to Catalogue objects vertically (Sql union)
	def union_catalogue(self, other):
		
		self.catalogue = pd.concat([self.catalogue, other.catalogue])

		return self
	
	# To rename index the catalogue based on given string variable
	def rename_index(self, string):
		
		self.catalogue = self.catalogue.rename_axis(string)
				
		return self
	
	# To add index or replace index of catalogue. Drop index replaces index
	def re_index_catalogue(self, drop = None):
		if drop is None:
			self.catalogue = self.catalogue\
					.reset_index(drop = False)\
					.rename_axis('unique_id')
		else:
			self.catalogue = self.catalogue\
					.reset_index(drop = True)\
					.rename_axis('unique_id')
				
		return self
		
	# To get disinct songs and artists with update stats
	def clean_up_catalogue(self):
		
		# This yields a warning: using dictionaries was removed because of 
		# its complexity and somewhat ambiguous nature. 
		# There is an ongoing discussion on how to improve this functionality
		aggregation = {
        "chart_num" : {"max_chart_num" : "max"},
        "run_date" : {"first_seen" : "min", 
		"last_seen": "max"}
        }
		
		repository = self.catalogue
		
		# Distinct artist repository
		artists = repository\
		.groupby(
		['artist_url', 'artist_name', 'genre', 'country']
		)\
		.agg(aggregation)\
		.reset_index()
		
		artists.columns = ['artist_url', 'artist_name',
		'genre', 'country',
		'max_chart_num', 'last_seen',
		'first_seen']
		
		artists = Catalogue(artists)
		
		# Distinct songs repository
		songs = repository\
		.groupby(
		['song_url', 'song_name', 
		'artist_url', 'artist_name' , 
		'country', 'genre', 
		'playlist_type']
		)\
		.agg(aggregation)\
		.reset_index()
		
		songs.columns = ['song_url', 'song_name', 
		'artist_url', 'artist_name' , 
		'country', 'genre', 
		'playlist_type', 'max_chart_num', 
		'last_seen','first_seen']
		
		songs = Catalogue(songs)
		
		return artists, songs
	
	# To save data to CSV based on working directory
	def save_data(self, file_name):
	
		file_to_save = self.catalogue
		
		file_to_save.to_csv(file_name)
		
		print('FILE SAVED TO DISK')
		
		return