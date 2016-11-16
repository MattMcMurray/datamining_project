import json
import os
import errno
import time

from settings import DATABASE_NAME, JSON_OUTPUT_DIRNAME, JSON_FILENAME_PREFIX
from core.web_scraping import movie_api_services as api
from core.web_scraping import article_scraper
from core.database.db_services import DatabaseServices

def create_output_dir(dirname):
    """ Creates an output directory within the module.

    @dirname: the name of the directory to be created.
    """

    if not os.path.exists(os.path.dirname(dirname)):
        try:
            os.makedirs(dirname)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def store_reviews(offset=0):
    """ Fetches the reviews from the NYTimes API and stores them in flat
    JSON files that have the offset appended to the filename.
    """

    json_output_file = JSON_FILENAME_PREFIX + '{suffix}.json'
    output_dir = 'json_output'

    create_output_dir(output_dir)

    data = api.get_all_reviews() # get initial dataset with no offset

    while data['num_results'] != '0'and data['status'] == 'OK'and data['has_more']:
        time.sleep(0.5) # Do not exceed NYTimes 5 requests/sec limit
        output_filename = json_output_file.format(suffix=offset)
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, 'w') as outfile:
            print 'Storing output in {0}'.format(output_path)
            json.dump(data, outfile)

        offset += 20
        data = api.get_all_reviews(offset=offset)

def parse_json_into_db():
    ''' Takes the data stored by store_reviews() and populates the DB '''

    database = DatabaseServices(DATABASE_NAME)

    for filename in os.listdir(JSON_OUTPUT_DIRNAME):
        if filename.startswith(JSON_FILENAME_PREFIX):

            filepath = os.path.join(JSON_OUTPUT_DIRNAME, filename)

            print filepath
            with open(filepath, 'r') as infile:
                data = json.load(infile)

                for item in data['results']:
                    database.add_movie_review(
                        byline=item['byline'],
                        display_title=item['display_title'],
                        release_date=item['opening_date'],
                        critics_pick=item['critics_pick'],
                        mpaa_rating=item['mpaa_rating'],
                        link_url=item['link']['url'],
                        link_type=item['link']['type']
                        )

def fetch_full_articles(start_from=1):
    ''' Use web scraping to fetch full article text and add it to the db

    @start_from: Optionally don't start from the beginning. This is good if the process was
    interrupted while running and you want to pick up from where it left off instead of restarting.

    '''
    database = DatabaseServices(DATABASE_NAME)

    num_movies = database.get_num_movies()

    for i in range(start_from, num_movies):
        try:
            curr_movie = database.get_review_by_id(i)
            full_review = article_scraper.scrape_article(curr_movie.link_url)
            database.add_review_full_text(curr_movie.movie_id, full_review)
        except Exception as exc:
            print 'SOMETHING WENT WRONG:'
            print exc

if __name__ == '__main__':
    fetch_full_articles()
