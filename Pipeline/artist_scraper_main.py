
parameters = open("parameters.py", 'r').read()
exec(parameters)

# Trying to scrape Ronny J's soundcloud links
# End goal: Get all tracks and info about tracks by just giving the link to his soundcloud.

chrome_options = Options()  
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(executable_path='../chromedriver_win32/chromedriver.exe', chrome_options = chrome_options)

artists_urls = list(pd.read_csv(artist_repository, index_col = 0)['artist_url'])

def scrape_artist_page(artist_extension):
    
    url = 'https://soundcloud.com' + artist_extension + '/tracks'
    
    #Start Driver
    driver.get(url)
    
    try:
        WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.lazyLoadingList__list")))
    
        # scrolling to the bottom of the page
        lazy_soundList_loaded = 0
        loaded_songs = len(driver.find_elements_by_class_name('soundList__item'))
        except_count = 0
     
        while lazy_soundList_loaded == 0:  # waits for the "paging-eof" class to appear when list is loaded
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                WebDriverWait(driver, 2).until((lambda x: len(driver.find_elements_by_class_name('soundList__item'))!= loaded_songs))
                
         # couldn't figure out how to get it to break when it finds the eof element, just catching timeout instead
            except TimeoutException:
                except_count += 1
                if except_count == 2:
                    break
            loaded_songs = len(driver.find_elements_by_class_name('soundList__item'))
            lazy_soundList_loaded = len(driver.find_elements_by_class_name('paging-eof'))
            
        #Grab elements in the page
        item_path = "//*[@class='userMain__content']//li[@class='soundList__item']"
        song_name_path = "//*[@class='userMain__content']//div[@class='soundTitle__usernameTitleContainer']/a[1]/span"
        artist_name_path = "//*[@class='userMain__content']//span[@class='soundTitle__usernameText']"
        publish_date_path = "//*[@class='userMain__content']//time[@class='relativeTime']"
        plays_path = "//*[@class='userMain__content']//div[@class='sound__soundStats']/ul/li[1]"
        comment_path = "//div[@class='sound__soundStats']/ul/li[2]"
        likes_path = "//*[@class='userMain__content']//button[@class='sc-button-like sc-button sc-button-small sc-button-responsive']"
        repost_path = "//*[@class='userMain__content']//button[@class='sc-button-repost sc-button sc-button-small sc-button-responsive']"
        followers_path = "//a[@class='infoStats__statLink sc-link-light']"
        
        song_list = [item.text for item in driver.find_elements_by_xpath(song_name_path)]
        
        artist_list = [item.text for item in driver.find_elements_by_xpath(artist_name_path)]
        
        publish_date_list = [
                datetime.datetime.strptime(item.get_attribute('datetime').replace('T',':')[0:-5],'%Y-%m-%d:%H:%M:%S') 
                for item in driver.find_elements_by_xpath(publish_date_path)]
    
        
        comment_list = []
        plays_list = []
        
        for item in  driver.find_elements_by_xpath(item_path):
            stats = item.find_elements_by_class_name('sc-ministats-item')
            num_stats = len(stats)
            
            if num_stats == 0:
                plays, comments = 0, 0
                
            elif num_stats == 1:
                plays = int((re.split(" " ,stats[0].get_attribute('title'))[0]).replace(',',''))
                comments = 0
            
            else:
                for stat in stats:
                     plays = int((re.split(" " ,stats[0].get_attribute('title'))[0]).replace(',',''))
                     comments = int((re.split(" " ,stats[1].get_attribute('title'))[0]).replace(',',''))
                     
            plays_list.append(plays)
            comment_list.append(comments)
                    
            
        likes_list = [item.text for item in driver.find_elements_by_xpath(likes_path)]
        
        repost_list = [item.text for item in driver.find_elements_by_xpath(repost_path)]
        
        artist_followers = int((re.split(" " ,driver.find_element_by_xpath(followers_path)\
                                         .get_attribute('title'))[0]).replace(',',''))
        
        run_time = datetime.datetime.now()
        
        print('songs: ' + str(len(song_list)))
        print('artists: '+ str(len(artist_list)))
        print('plays: '+ str(len(plays_list)))
        print('comments: ' + str(len(comment_list)))
        print('likes: ' + str(len(likes_list)))
        print('reposts: ' + str(len(repost_list)))
        
        artist_data = {'song_name': song_list,
                       'artist_name': artist_list,
                       'publish_date': publish_date_list,
                       'plays': plays_list,
                       'comments':comment_list,
                       'likes': likes_list,
                       'repost': repost_list,
                       'artist_followers': artist_followers,
                       'run_date': run_time}
        
        
        pd.set_option('display.max_columns', None)
        
        artist_df = pd.DataFrame(artist_data)
    
    except TimeoutException:
        print("artist does not exist")
        artist_
    
    return(artist_df)


appended_data = pd.DataFrame()

x = 0
for url in artists_urls:
    x = x+1
    print()
    print(str(x), url)
    
    try:
        data = scrape_artist_page(url)
        appended_data = pd.concat([appended_data, data])
    except ValueError:
        print(url + "---------------------------> length error")

driver.quit()

appended_data = appended_data\
.reset_index(drop = True)\
.rename_axis('index')

data = Catalogue(appended_data)

Catalogue.save_data(data, song_metrics_data)

