# DATAMINING PROJECT [![Build Status](https://travis-ci.org/MattMcMurray/datamining_project.svg?branch=develop)](https://travis-ci.org/MattMcMurray/datamining_project)

## Getting Started
1. Ensure you've got python (2.7), python-pip, and python-mysqldb installed
2. Install virtualenv 
  - `pip install virtualenv`
3. Create a virtualenv
  - e.g. `virtualenv venv`
4. Activate the virtualenv
  - on linux: `source venv/bin/activate`
5. Install requirements
  - `pip install -r requirements.txt`

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
