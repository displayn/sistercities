import datetime
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class City(Base):
    __tablename__ = 'city'
    # Here we define columns for the table city
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    city_url = Column(String(250), nullable=True)
    city_qid = Column(String(250), nullable=False)
    city_rev = Column(Integer, nullable=False)
    city_checkdate = Column(DateTime, default=datetime.datetime.utcnow)
    wiki_id = Column(Integer)


class Sistercity(Base):
    __tablename__ = 'sistercity'
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('city.city_qid'))
    sister_qid = Column(Integer, ForeignKey('city.city_qid'))


class Wiki(Base):
    __tablename__ = 'wiki'
    id = Column(Integer, primary_key=True)
    label = Column(String(20), nullable=False)


# Create an engine that stores data in the local directory's
engine = create_engine('sqlite:///localdev.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
