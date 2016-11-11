import json

from core.web_scraping import movie_api_services as api


JSON_OUTPUT_FILE = 'movie_response.json'

def store_reviews():
    data = api.get_all_reviews()

    with open(JSON_OUTPUT_FILE, 'w') as outfile:
        json.dump(data, outfile)

if __name__ == '__main__':
    store_reviews()
