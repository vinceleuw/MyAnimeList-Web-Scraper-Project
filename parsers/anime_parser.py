from bs4 import BeautifulSoup

from locators.anime_locators import AnimeLocators


class AnimeParser:
    """
    Initializes an AnimeParser object which parses through and returns information on the page. Takes in HTML of page content and links to the page as parameters.
    """

    def __init__(self, page_content, link):
        self.link = link
        self.page_content = page_content
        self.soup = BeautifulSoup(self.page_content, 'html.parser')

    def __repr__(self):
        return f'<{self.name} / {self.anime_type} / {self.episodes} / {self.studio} / {self.members} / {self.score} / {self.link}>'

    @property
    def name(self):
        """
        Returns the name of the anime on the page.
        """
        locator = AnimeLocators.NAME_LOCATOR
        anime_name = self.soup.select_one(locator).get_text()
        return anime_name

    @property
    def score(self):
        """
        Returns the score of the anime on the page.
        """
        locator = AnimeLocators.SCORE_LOCATOR
        anime_score = self.soup.select_one(locator).get_text()
        return float(anime_score) if anime_score != 'N/A' else 0

    @property
    def studio(self):
        """
        Returns the studio that created the anime on the page.
        """
        locator = AnimeLocators.STUDIO_LOCATOR
        anime_studio = self.soup.select_one(locator).get_text()
        return anime_studio

    @property
    def anime_type(self):
        """
        Returns the anime type on the page. (TV, MOVIE, OVA, ONA)
        """
        locator = AnimeLocators.TYPE_LOCATOR
        anime_type = self.soup.select_one(locator).get_text()
        return anime_type

    @property
    def members(self):
        """
        Returns the number of members that follow the anime.
        """
        locator = AnimeLocators.MEMBER_LOCATOR
        anime_members = self.soup.select_one(locator).strong.text
        return int(anime_members.replace(',', ''))

    @property
    def episodes(self):
        """
        Returns the total number of episodes of the anime, or ? if unknown.
        """
        locator = AnimeLocators.EPISODE_COUNT_LOCATOR
        episode_count = self.soup.select_one(locator).get_text()
        return int(episode_count) if episode_count != '?' else 'N/A'
