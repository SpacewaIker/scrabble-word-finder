import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_words_from_page(pageNumber):
    if pageNumber == 1:
        # page 1
        url = 'https://www.listesdemots.net/touslesmots.htm'
    else:
        # from page 2 to 918
        url = 'https://www.listesdemots.net/touslesmotspage{pageNumber}.htm'
        url = url.format(pageNumber=pageNumber)

    response = requests.get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    span = html_soup.find("span", "mot")

    words = span.text.split(" ")

    return words


if __name__ == "__main__":
    list_of_words = pd.Series([], dtype='object')

    for _ in range(1, 919):
        if _ % 10 == 0:
            print(_)  # to check progress
        words = pd.Series(get_words_from_page(_))
        list_of_words = list_of_words.append(words, ignore_index=True)

    list_of_words.to_csv(
        'projects/scrabble/sowpods_fr.csv',
        header=False,
        index=False
    )
