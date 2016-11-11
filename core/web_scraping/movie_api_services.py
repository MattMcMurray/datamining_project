import requests

from core.web_scraping.settings import NY_TIMES_API_KEY

def get_all_reviews():
    """ Return a json object containing reviews.

        TODO: be able to iterate through ALL the reviews
    """
    assert NY_TIMES_API_KEY != ''

    base_url = 'https://api.nytimes.com/svc/movies/v2/reviews/{resource_type}.json'
    params = '?api-key={api_key}'

    response = requests.get(
        base_url.format(resource_type='all') +
        params.format(api_key=NY_TIMES_API_KEY)
        )

    return response.json()
