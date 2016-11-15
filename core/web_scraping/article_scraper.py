import requests
from bs4 import BeautifulSoup


def scrape_article(url):
    ''' Fetches the full review text from NYTimes page

    @url: the url from which to scrape an article

    @return: the text from said article

    ## There are two different styles of NYTimes articles ##

    new style URL looks like:
        http://www.nytimes.com/2016/11/11/movies/oscar-winner-ang-lees-billy- ...
    old style URL looks like:
        http://www.nytimes.com/movie/review?res=9C05E5D81E3DE23ABC4950DFB766838F629EDE
    '''

    response = requests.get(url)
    url_tokens = url.split('/')
    if url_tokens[3] == 'movie': # OLD/ARCHIVE STYLE ARTICLE
        return __parse_old_article(response.text)
    else:
        return __parse_new_article(response.text)

def __parse_old_article(data):
    soup = BeautifulSoup(data, 'html.parser')
    article_body = soup.find_all(id='articleBody')

    article_text = ""
    for child in article_body:
        article_text += child.get_text()

    return article_text

def __parse_new_article(data):
    soup = BeautifulSoup(data, 'html.parser')
    article_paragraphs = soup.find_all('p', class_='story-body-text')

    article_text = ""
    for paragraph in article_paragraphs:
        article_text += paragraph.get_text()

    return article_text
