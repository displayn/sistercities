# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sistercities.parser.parser_declarative import Base, City, Sistercity, Wiki

engine = create_engine('sqlite:///localdev.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


#add new wiki
    #check if exist and when yes get ID
        new_wiki = Wiki(label='de')
        session.add(new_wiki)
        session.commit()
            #fetch last ID

# Insert a City in the city table
new_city = City(city_url='Berlin', city_rev=1234, city_quid='Q64')
session.add(new_city)
session.commit()

