import requests

from core.web_scraping.settings import NY_TIMES_API_KEY

def get_all_reviews(offset=0):
    """ Gets a json object of movie reviews

    @offset: must be multiple of 20.

    @return: a json object containing the response from the api.
    """

    assert offset % 20 == 0
    assert NY_TIMES_API_KEY != ''

    base_url = 'https://api.nytimes.com/svc/movies/v2/reviews/{resource_type}.json'
    params = '?api-key={api_key}'

    if offset > 0:
        params += '&offset={offset}'

    response = requests.get(
        base_url.format(resource_type='all') +
        params.format(api_key=NY_TIMES_API_KEY,
                      offset=offset)
        )

    return response.json()
