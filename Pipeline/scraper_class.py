"""
Driver class to scrape pages on soundcloud.
Class object will be the string with the url. Class functions will be used to 
"""

class Sc_scraper:

	# Class object is the url to scrape. The constructor can take attributes to generate
	# different types of urls. For charts, if url string is charts, then uses attributes
	# to generate url.
	def __init__(self, url_string , url_type = None, genre = None, country = None):
		
		if url_string == "charts":
			url = "https://soundcloud.com/charts/"
			self.url = url + url_type + "?genre=" + genre + "&country=" + country
		else:
			self.url = str(url_string)
	
	
	# Simple print string url
	def print_url(self):
		
		print(self.url)
		
		return
	
	# Deconstruct the url back to the parameters.Will be used as part of the chart scraper
	# Outputs tuple of url_type, genre, country. These will be inputs for variables in df
	def deconstruct_charts_url(self):
	
		attributes = re.split('https://soundcloud.com/charts/', self.url)[1]
		
		url_type = re.split('\?genre=', attributes)[0]
		
		split1 = re.split('\?genre=', attributes)[1]
		
		split2 = re.split('&country=', split1)
		
		genre = split2[0]
		
		country = split2[1]
		
		return url_type, genre, country
		
	
	# Takes url of charts website and scrapes in catalogue type df -> see catalogue class
	def chart_scraper(self, run_number):
	
		# url of soundcloud page to scrape + read from page using urllib
		content = urllib.request.urlopen(self.url).read()
		url_type, genre, country = self.deconstruct_charts_url()
		run_time = datetime.datetime.now()
		
		# lists to pack with data
		song_url_list = []# list containing song url soundcloud extensions
		song_name_list = []# list containing song names as the appear on site
		artist_url_list = []# list containing artist url soundcloud extensions
		artist_name_list = []# list containing artist url as appear on site
		
		# cycle variable for loop
		i = 0 # track if song (=0) or artist (=1)
		
		# parse out article sections and pattern with second headers (h2) and 'a' child
		only_tags_with_h2 = SoupStrainer("article")
		
		soup = BeautifulSoup(content,
							 "html.parser",
							 parse_only=only_tags_with_h2)\
							 .select('h2 > a')
		
		# append scraped data to respective lists
		for article in soup:
		
			if i == 0 :
				column_name = "song"
				song_url_list.append(str(article.get('href', '/')))
				song_name_list.append(str(article.text))
				i = i + 1
			else:
				column_name = "artist"
				artist_url_list.append(str(article.get('href', '/')))
				artist_name_list.append(str(article.text))
				i = i - 1
		
		# dictionary of data scrapedo on page
		df = {"artist_url":artist_url_list, 
			  "artist_name" : artist_name_list,
			  "song_url" : song_url_list,
			  "song_name" : song_name_list,
			  "country" : country,
			  "genre" : genre,
			  "playlist_type" : url_type,
			  "run_date" : run_time,
			  "playlist": self.url,
			  "runID": run_number}
		
		#generate data frame
		data = pd.DataFrame(df, 
							columns = [
							"artist_url", "artist_name",
							"song_url", "song_name",
							"country", "genre",
							"playlist_type","run_date",
							"playlist", "runID"
							])
										   
		data.index = data.index + 1# chart num from 0 to 1
		
		return data
		
	
	