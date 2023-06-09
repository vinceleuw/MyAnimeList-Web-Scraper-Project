import asyncio
import time

import aiohttp
from aiolimiter import AsyncLimiter
from selenium.webdriver.common.by import By
from cachetools import cached, TTLCache

from locators.list_locators import ListLocator
from parsers.anime_parser import AnimeParser


class ListPage:
    """
    Initializes a ListPage object that takes in a Chrome webdriver as parameter.
    """

    def __init__(self, browser):
        self.browser = browser
        self.loop = asyncio.get_event_loop()
        # Limits number of a requests to 1 every 3 seconds
        self.rate_limit = AsyncLimiter(1, 3)
        self.page_content = self.loop.run_until_complete(
            self.get_multiple_pages(self.loop, self.links))

    @property
    @cached(cache=TTLCache(maxsize=1, ttl=3600))
    def anime_info(self):
        """
        Returns a List of parsed anime information. Caches result for up to an hour.
        """
        return [
            AnimeParser(page, link)
            for page, link in zip(self.page_content, self.links)
        ]

    @property
    def links(self):
        """
        Returns a list of links to the pages of all anime entries on the current page.
        """
        return [a.get_attribute('href') for a in self.browser.find_elements(By.CSS_SELECTOR, ListLocator.LIST_LOCATOR)]

    async def fetch_page(self, session, link):
        page_start = time.time()
        async with self.rate_limit:
            async with session.get(link) as response:
                print(f'{link} took {time.time() - page_start}')
                return await response.text()

    async def get_multiple_pages(self, loop, links):
        tasks = []
        async with aiohttp.ClientSession(loop=loop) as session:
            for link in links:
                tasks.append(self.fetch_page(session, link))
            return await asyncio.gather(*tasks)
