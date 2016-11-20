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
    regex1 = re.compile(r'^\$?(\d*(\.\d)?)( million| billion)')
    regex2 = re.compile(r'^\$?(\d*\,\d*)*')


    database = DatabaseServices(DATABASE_NAME)
    num_movies = database.get_num_movies()

    for i in range(1, num_movies):
        sani_gross = None

        try:
            release_year = ''
            searchstr = '{title} {year}film'
            curr_movie = database.get_review_by_id(i)

            if curr_movie.release_date is not None:
                release_year = curr_movie.release_date[:4] + ' '

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

        except IndexError as exc:
            print 'Search for movie failed; this happens when the film is too old/obscure'

        except UnicodeEncodeError as exc:
            print 'Unicode error; moving on'

        except:
            print 'An uknown error occured; moving on'

        if sani_gross is not None:
            try:
                if len(sani_gross.group(0)):
                    parsed_gross_str = parse_box_office_gross_str(sani_gross.group(0))
                    database.add_box_office_gross(curr_movie.movie_id, parsed_gross_str)
            except Exception as exc:
                print 'An unknown error occured; moving on'
                print exc
        else:
            'Sanitized gross is None'

        print '\n'

def parse_box_office_gross_str(gross_str):
    ''' Preps a string pulled from wikipedia to be stored in the database

    @str: the string to be 'santitized

    @return: an integer representing gross in dollars
    '''

    ## First, remove the '$' at the beginning of the str
    gross_str = gross_str[1:]

    ## Second, convert the words 'million' and 'billion' to zeroes
    ## We need to count how many numbers there are after the decimal point and only add the
    ## appropriate amount of zeroes
    num_decimal_pts = 0
    if '.' in gross_str:
        index = gross_str.find('.')

        while gross_str[index+1].isdigit():
            index += 1
            num_decimal_pts += 1

    gross_str = gross_str.replace('.', '')
    gross_str = gross_str.replace(' ', '')
    gross_str = gross_str.replace(',', '')

    zeroes = ''
    if ('million' in gross_str) or ('millions' in gross_str):
        zeroes = generate_zeroes(num_decimal_pts, million=True, billion=False)
    elif ('billion' in gross_str) or ('billions' in gross_str):
        zeroes = generate_zeroes(num_decimal_pts, million=False, billion=True)

    gross_str = gross_str.replace('million', zeroes)
    gross_str = gross_str.replace('millions', zeroes)
    gross_str = gross_str.replace('billion', zeroes)
    gross_str = gross_str.replace('billions', zeroes)


    return gross_str

def generate_zeroes(offset, million=False, billion=False):
    num_zeroes_million = 6
    num_zeroes_billion = 9
    num_zeroes = None

    if million:
        num_zeroes = num_zeroes_million - offset
    elif billion:
        num_zeroes = num_zeroes_billion - offset

    zero_str = ''
    for i in range(0, num_zeroes):
        zero_str += '0'

    return zero_str

if __name__ == '__main__':
    print start_box_office_crawl()
