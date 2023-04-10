import time

from selenium.webdriver.common.by import By

from locators.list_locators import ListLocator
from parsers.anime_parser import AnimeParser


class ListPage:
    def __init__(self, browser):
        self.browser = browser

    @property
    def anime_info(self):
        return [
            AnimeParser((self.browser, time.sleep(5)), link)
            for link in self.links
        ]

    @property
    def links(self):
        return [a.get_attribute('href') for a in self.browser.find_elements(By.CSS_SELECTOR, ListLocator.LIST_LOCATOR)]
