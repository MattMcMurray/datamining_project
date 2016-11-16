from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from core.database.models.movie import Base, Movie

class DatabaseServices(object):
    """ Methods to ease interfacing with ORM """

    def __init__(self, db_file_name):
        self.filename = db_file_name
        self.engine = None
        self.session = None

    def init_engine(self):
        """ Create the database engine."""

        # TODO: if db already exists, prompt to ask if it should be overwritten
        # appended, etc..
        self.engine = create_engine(
            'sqlite:///{0}.db'.format(self.filename)
            , echo=True)

        Base.metadata.create_all(self.engine)

    def get_session(self):
        """ Get a session for the database """

        if self.engine is None:
            self.init_engine()

        session = sessionmaker(bind=self.engine)

        self.session = session()

    def add_movie_review(self, byline, display_title, release_date, critics_pick,
                         mpaa_rating, link_url, link_type):
        """ Adds a movie review object to the db session and commits.
        If session doesn't exist, it will be created
        """

        if self.session is None:
            self.get_session()

        new_movie = Movie(
            byline=byline,
            display_title=display_title,
            release_date=release_date,
            critics_pick=critics_pick,
            mpaa_rating=mpaa_rating,
            link_url=link_url,
            link_type=link_type)

        try:
            self.session.add(new_movie)
            self.session.commit()
        except (IntegrityError, UnicodeEncodeError) as exc:
            print exc
            print '\n\n'
            print 'There was an error adding a movie to the db.'
            print 'Movie title is likely a duplicate; rolling back and moving on...'
            self.session.rollback()

    def get_review_by_title(self, movie_title):
        """ Gets a movie review by the title of the movie

        Returns the first item in the DB matching that title
        """

        if self.session is None:
            self.get_session()

        return self.session.query(Movie).filter_by(display_title=movie_title).first()

    def get_num_movies(self):
        """ Fetches the number of movie reviews stored in DB """
        if self.session is None:
            self.get_session()

        return self.session.query(func.count(Movie.movie_id)).scalar()
