from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.database.models.movie import Base, Movie

ENGINE = None
MY_SESSION = None

def init_engine(debug=False):
    """ Create the database engine.

    If in debug mode, use a sqlite db as a pseudo-stub
    """
    global ENGINE

    if debug:
        ENGINE = create_engine('sqlite:///test.db', echo=True)
    else:
        raise ValueError('Prod db not yet implemented; run with debug=True')

    Base.metadata.create_all(ENGINE)

def get_session():
    """ Get a session for the database """
    global MY_SESSION, ENGINE

    if ENGINE is None:
        init_engine(debug=True)

    session = sessionmaker(bind=ENGINE)

    MY_SESSION = session()

def add_movie_review(byline, display_title, critics_pick, mpaa_rating,
                     link_url, link_type):
    """ Adds a movie review object to the db session and commits.
    If session doesn't exist, it will be created
    """
    global MY_SESSION

    if MY_SESSION is None:
        get_session()

    new_movie = Movie(
        byline=byline,
        display_title=display_title,
        critics_pick=critics_pick,
        mpaa_rating=mpaa_rating,
        link_url=link_url,
        link_type=link_type)

    MY_SESSION.add(new_movie)
    MY_SESSION.commit()

def get_review_by_title(movie_title):
    global MY_SESSION

    if MY_SESSION is None:
        get_session()

    return MY_SESSION.query(Movie).filter_by(display_title=movie_title).first()
