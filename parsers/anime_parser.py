from bs4 import BeautifulSoup

from locators.anime_locators import AnimeLocators


class AnimeParser:
    def __init__(self, page_content, link):
        self.link = link
        self.page_content = page_content
        self.soup = BeautifulSoup(self.page_content, 'html.parser')

    def __repr__(self):
        return f'<{self.name} / {self.anime_type} / {self.episodes} / {self.studio} / {self.members} / {self.score} / {self.link}>'

    @property
    def name(self):
        locator = AnimeLocators.NAME_LOCATOR
        anime_name = self.soup.select_one(locator).get_text()
        return anime_name

    @property
    def score(self):
        locator = AnimeLocators.SCORE_LOCATOR
        anime_score = self.soup.select_one(locator).get_text()
        return float(anime_score) if anime_score != 'N/A' else 0

    @property
    def studio(self):
        locator = AnimeLocators.STUDIO_LOCATOR
        anime_studio = self.soup.select_one(locator).get_text()
        return anime_studio

    @property
    def anime_type(self):
        locator = AnimeLocators.TYPE_LOCATOR
        anime_type = self.soup.select_one(locator).get_text()
        return anime_type

    @property
    def members(self):
        locator = AnimeLocators.MEMBER_LOCATOR
        anime_members = self.soup.select_one(locator).strong.text
        return int(anime_members.replace(',', ''))

    @property
    def episodes(self):
        locator = AnimeLocators.EPISODE_COUNT_LOCATOR
        episode_count = self.soup.select_one(locator).get_text()
        return int(episode_count) if episode_count != '?' else 'N/A'
