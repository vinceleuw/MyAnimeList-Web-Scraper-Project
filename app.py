import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.list_page import ListPage


SCROLL_PAUSE_TIME = 5


def main():
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('–-allow-running-insecure-content')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    chrome.get("https://myanimelist.net/animelist/Jlin2?status=6")

    # Get scroll height
    last_height = chrome.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        chrome.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = chrome.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    page = ListPage(chrome)
    anime = page.anime_info

    for i, x in enumerate(anime):
        anime[i] = repr(x).strip('<>').split(' / ')

    print(anime)
    df = pd.DataFrame(anime, columns=[
                      'Name', 'Type', 'Episodes', 'Studio', 'Members', 'Score', 'Link'])
    print(df)

    df.to_csv('anime.csv')

    print(df.dtypes)


if __name__ == '__main__':
    main()
