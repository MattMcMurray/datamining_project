import json
import os
import errno
import time

from core.web_scraping import movie_api_services as api

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

    json_output_file = 'movie_response_{suffix}.json'
    output_dir = 'json_output'

    create_output_dir(output_dir)

    data = api.get_all_reviews() # get initial dataset with no offset

    while data['num_results'] != '0'and data['status'] == 'OK'and data['has_more']:
        time.sleep(0.2) # Do not exceed NYTimes 5 requests/sec limit
        output_filename = json_output_file.format(suffix=offset)
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, 'w') as outfile:
            print 'Storing output in {0}'.format(output_path)
            json.dump(data, outfile)

        offset += 20
        data = api.get_all_reviews(offset=offset)

if __name__ == '__main__':
    store_reviews()
