
parameters = open("parameters.py", 'r').read()
exec(parameters)

# Trying to scrape Ronny J's soundcloud links
# End goal: Get all tracks and info about tracks by just giving the link to his soundcloud.

chrome_options = Options()  
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(executable_path='../chromedriver_win32/chromedriver.exe', chrome_options = chrome_options)

artist_extension = '/6omino'
url = 'https://soundcloud.com' + artist_extension + '/tracks'
    
#Start Driver
driver.get(url)

WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.lazyLoadingList__list")))
