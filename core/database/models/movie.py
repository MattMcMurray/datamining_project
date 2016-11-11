from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'

    movie_id = Column(Integer, primary_key=True)
    byline = Column(String)
    display_title = Column(String)
    critics_pick = Column(String)
    mpaa_rating = Column(String)
    link_url = Column(String)
    link_type = Column(String)
