import requests
import json
from pprint import pprint

from core.database import test
from settings import NY_TIMES_API_KEY

def get_all_reviews():
    assert(NY_TIMES_API_KEY != '')
    base_url = 'https://api.nytimes.com/svc/movies/v2/reviews/{resource_type}.json'
    params = '?api-key={api_key}'
    
    response = requests.get(
            base_url.format(resource_type='all') +
            params.format(api_key=NY_TIMES_API_KEY)
            )

    return response.json()

if __name__ == '__main__':
    data = get_all_reviews()

    with open('movie_response.json', 'w') as outfile:
        json.dump(data, outfile)

    print 'done'
