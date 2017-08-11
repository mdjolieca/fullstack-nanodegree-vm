#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///catalogue.db')
# Bind the engine to the metadata of the Base class 

DBSession = sessionmaker(bind=engine)
#create DB session for adding data to tables
session = DBSession()


# Create sample users
User0 = User(name="Marie-Denise Jolie ", email="mariedenisejolie@gmail.com",
             picture='https://lh3.googleusercontent.com/-yHl6O5IKj_k/AAAAAAAAAAI/AAAAAAAADb0/SW3OfQduSlc/photo.jpg')
session.add(User0)
session.commit()

User1 = User(name="The Force", email="yoda@starwars.com",
             picture='/static/yoda.jpg')
session.add(User1)
session.commit()

#generic Category description
description = "A great description of this category will go here but for now this is a Sample description."

# Create Sample Categories with 5 items in each,
# alternating between 2 user_ids for Category owner

for x in range(1, 10):
    if(x%2)==0:
       category = Category(user_id=User0.id, name='Sample Category '+str(x), description=description)
    else:
       category = Category(user_id=User1.id, name='Sample Category '+str(x), description=description)
    print('created category '+category.name+':\n')
    session.add(category)
    session.commit()
    items = []
    for i in range(1, 5):
       items.append(Item( name='Sample Item'+str(i), description="Sample Item description item number for testing is " + str((x-1)*5 + i),
       price="$0.00",  category_id=category.id))
       print(items)
    session.add_all(items)
    session.commit()


#close session and destroy engine 
session.close()
engine.dispose()


print "added sample data to catalogue tables!"