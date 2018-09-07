import urllib.request
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

# Trying to scrape Ronny J's soundcloud links
# End goal: Get all tracks and info about tracks by just giving the link to his soundcloud.

# Ronny J tracks page
ronnyj_tracks_url = 'https://soundcloud.com/ronnyjlistenup/tracks'
content = urllib.request.urlopen(ronnyj_tracks_url).read()

# tracks are loaded lazily so we need to automate scrolling
# experimenting with selenium
driver = webdriver.Chrome(executable_path='D:\\SlapScience\\chromedriver_win32\\chromedriver.exe')
driver.get(ronnyj_tracks_url)

# scrolling to the bottom of the page
lazy_soundList_loaded = 0
loaded_songs = len(driver.find_elements_by_class_name('soundList__item'))
except_count = 0

while lazy_soundList_loaded == 0:  # waits for the "paging-eof" class to appear when list is loaded
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        WebDriverWait(driver, 2).until((lambda x: len(driver.find_elements_by_class_name('soundList__item'))
                                        != loaded_songs))
    # couldn't figure out how to get it to break when it finds the eof element, just catching timeout instead
    except TimeoutException:
        except_count += 1
        if except_count == 2:
            break
    loaded_songs = len(driver.find_elements_by_class_name('soundList__item'))
    lazy_soundList_loaded = len(driver.find_elements_by_class_name('paging-eof'))
    print(lazy_soundList_loaded)
driver.quit()
