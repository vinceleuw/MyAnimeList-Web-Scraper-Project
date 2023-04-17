import time
import pandas as pd
import sqlite3
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.list_page import ListPage


SCROLL_PAUSE_TIME = 5
'''
Link to User's anime list in format of https://myanimelist.net/animelist/USER_NAME?status=STATUS_NUMBER
1 - Currently Watching
2 - Completed
3 - On Hold
4 - Dropped
6 - Plan to Watch
7 - All Anime
'''
LIST_LINK = 'https://myanimelist.net/animelist/Moonlit_Lilium?status=3'


def main():
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('–-allow-running-insecure-content')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    chrome = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    chrome.get(LIST_LINK)

    user = re.search('animelist\/([\w]+)', LIST_LINK).group(1)

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

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('INSERT OR IGNORE INTO users(user) VALUES(?)', (user,))
    connection.commit()
    cursor.execute('SELECT userid FROM users WHERE user = ?', (user,))
    test = cursor.fetchone()[0]

    for i in anime:
        cursor.execute('INSERT OR IGNORE INTO on_list VALUES(?, ?)', (i.mal_id, test))
        connection.commit()
    connection.close()

    for i, x in enumerate(anime):
        anime[i] = repr(x).strip('<>').split(' / ')

    print(anime)
    df = pd.DataFrame(anime, columns=[
                      'MALID', 'Name', 'Type', 'Episodes', 'Studio', 'Members', 'Score', 'Link'])
    print(df)

    df.to_csv('anime.csv')

    print(df.dtypes)

    print(page.anime_info)


if __name__ == '__main__':
    main()
