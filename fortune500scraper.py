from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Fortune500Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='D:\\SlapScience\\chromedriver_win32\\chromedriver.exe')
        self.wait = WebDriverWait(self.driver, 10)

    def get_last_line_number(self):
        """Get the line number of last company loaded into the list of companies."""
        return int(self.driver.find_element_by_css_selector("ul.company-list > li:last-child > a > span:first-child").text)

    def get_links(self, max_company_count=1000):
        """Extracts and returns company links (maximum number of company links for return is provided)."""
        self.driver.get('http://fortune.com/fortune500/list/')
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.company-list")))

        last_line_number = 0
        while last_line_number < max_company_count:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            self.wait.until(lambda driver: self.get_last_line_number() != last_line_number)
            last_line_number = self.get_last_line_number()

        return [company_link.get_attribute("href")
                for company_link in self.driver.find_elements_by_css_selector("ul.company-list > li > a")]

    def get_company_data(self, company_link):
        """Extracts and prints out company specific information."""
        self.driver.get(company_link)

        return {
            row.find_element_by_css_selector(".company-info-card-label").text: row.find_element_by_css_selector(".company-info-card-data").text
            for row in self.driver.find_elements_by_css_selector('.company-info-card-table > .columns > .row')
        }

if __name__ == '__main__':
    scraper = Fortune500Scraper()

    company_links = scraper.get_links(max_company_count=100)
    for company_link in company_links:
        company_data = scraper.get_company_data(company_link)
        pprint(company_data)
        print("------")