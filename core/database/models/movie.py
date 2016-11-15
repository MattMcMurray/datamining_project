from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Movie(Base):
    """ The ORM model for the movie table """
    __tablename__ = 'movies'

    movie_id = Column(Integer, primary_key=True)
    byline = Column(String)
    display_title = Column(String, unique=True)
    release_date = Column(String)
    critics_pick = Column(String)
    mpaa_rating = Column(String)
    link_url = Column(String)
    link_type = Column(String)
    box_office_earnings = Column(String)
    full_review = Column(String)
