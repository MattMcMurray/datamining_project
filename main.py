import json
import os
import errno
import time
import re

from settings import DATABASE_NAME, JSON_OUTPUT_DIRNAME, JSON_FILENAME_PREFIX
from core.web_scraping import movie_api_services as api
from core.web_scraping import box_office_scraper as box_office
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

def start_box_office_crawl():
    ''' Fetch movies from the DB, then crawl the web for their box office gross

        There are two regexes that parse the box office gross from wikipedia

        r'^\$?(\d*(\.\d)?)( million| billion)'

            parses grosses that look like:
            - $14.5 million
            - $32 billion

        r'^\$?(\d*\,\d*)*'

            parses grosses that look like:
            - $2,400,000 (anything else following)
    '''
    import logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

    regex1 = re.compile(r'^\$?(\d*(\.\d)?)( million| billion)')
    regex2 = re.compile(r'^\$?(\d*\,\d*)*')


    database = DatabaseServices(DATABASE_NAME)
    num_movies = database.get_num_movies()

    for i in range(1, num_movies):
        sani_gross = None

        try:
            release_year = ""
            searchstr = "{title} {year} film"
            curr_movie = database.get_review_by_id(i)

            if curr_movie.release_date is not None:
                release_year = curr_movie.release_date[:4]

            searchstr = searchstr.format(
                title=curr_movie.display_title,
                year=release_year
                )

            print 'Searching for "' + searchstr + '"'
            search_result = box_office.search_wiki(searchstr)
            article_title = search_result['query']['search'][0]['title'].replace(' ', '_')

            article = box_office.scrape_wiki(article_title)

            box_office_gross = article.find(
                'th', text='Box office').next_sibling.next_sibling.get_text()

            if '.' in box_office_gross:
                sani_gross = regex1.match(box_office_gross)
            elif ',' in box_office_gross:
                sani_gross = regex2.match(box_office_gross)


        except AttributeError as exc:
            print 'No box office gross in article'
            print exc

        except IndexError as exc:
            print 'Search for movie failed'
            print exc

        except UnicodeEncodeError as exc:
            print 'Unicode error; moving on'

        except:
            print 'An uknown error occured; moving on'

        if sani_gross is not None:
            print 'Potential gross: ' + sani_gross.group(0)

        print '\n'

if __name__ == '__main__':
    print start_box_office_crawl()
