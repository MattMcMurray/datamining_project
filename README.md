# DATAMINING PROJECT [![Build Status](https://travis-ci.org/MattMcMurray/datamining_project.svg?branch=develop)](https://travis-ci.org/MattMcMurray/datamining_project)

## Getting Started
1. Ensure you've got python (2.7) and python-pip installed
  - e.g., on ubuntu/debian: `sudo apt-get install -y python python-pip`
2. Install virtualenv 
  - `pip install virtualenv`
3. Create a virtualenv
  - e.g. `virtualenv venv`
4. Activate the virtualenv
  - on linux: `source venv/bin/activate`
5. Install requirements
  - `pip install -r requirements.txt`
  
*Note: every time you use `pip` to install a new module, you must run `pip freeze > requirements.txt` to save the new module to the requirements file*

## Running Tests
1. Ensure you've activated your virtualenv (see [Getting Started](#Getting-Started))
2. Ensure `pytest` is installed in virtualenv by running `pytest --version`
3. Run `pytest tests/`

## To Fetch Data from NYTimes API
*Note: The output has already been stored in the repo. But here's the instructions in case you want to run it again.*

1. `cd` into main project directory
2. Ensure you've activated your virtualenv (see [Getting Started](#Getting-Started))
3. Activate the python interactive shell by running the `python` command
4. Run the following commands:
```
import main
main.store_reviews()

## Optionally, `store_reviews()` can take an offset. 
## Offset must be a multiple of 20 or exception will be thrown
```

## To Populate Database
1. `cd` into main project directory
2. Ensure you've activated your virtualenv (see [Getting Started](#Getting-Started))
3. Activate the python interactive shell by running the `python` command
4. Run the following commands:
```
import main
main.parse_json_into_db()

## You may get an exception thrown here or there. 
## This is because NYTimes provides some duplicates and the DB rejects duplicates.
```

## To Browse/Inspect the Database
- I've decided to use SQLite because it's more than enough for our needs and the flat file can be stored in the repo
- There is an incomplete version of the DB in the repo right now
- To look at what the DB contains, you can download the [SQLite DB Browser](http://sqlitebrowser.org/)
