import requests
from bs4 import BeautifulSoup
from pprint import pprint


def search_wiki(search_query):
    base_url = 'https://en.wikipedia.org/w/api.php'
    query_params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': search_query,
    }

    response = requests.get(base_url, params=query_params)

    return response.json()

def scrape_wiki(article_title):
    ''' Visit wikipedia, look for string "Box Office", grab next <td> element '''

    base_url = 'https://en.wikipedia.org/wiki/{article_title}'
    query_url = base_url.format(article_title=article_title)

    response = requests.get(query_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup
