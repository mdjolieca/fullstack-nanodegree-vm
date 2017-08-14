#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, Item, User

#This script is for testing purposes only. 

engine = create_engine('sqlite:///catalogue.db')
# Bind the engine to the metadata of the Base class 

DBSessionMaker = sessionmaker(bind=engine)
#create DB session for adding data to tables
dbSession = DBSessionMaker()

#print all users. 

users = dbSession.query(User).all()
for user in users:
   print(user.id)
   print(user.name)
   print(user.picture)
   print(user.email)
#close session and destroy engine 
dbSession.close()
engine.dispose()