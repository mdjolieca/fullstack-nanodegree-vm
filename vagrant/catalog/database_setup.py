#!/usr/bin/env python
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

#Running this file will Create database tables for catalouge 
#This class defines 3 Catalogue table Class (User, Category, Item)

#Users table
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    
    # When a user is deleted must also delete user's child objects
    categories = relationship("Category", cascade="all, delete-orphan")
  
    # User Helper Functions
    @staticmethod
    def createUser(login_session, dbSession):
       newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
       dbSession.add(newUser)
       dbSession.commit()
       user = dbSession.query(User).filter_by(email=login_session[
       'email']).one()
       return user

    @staticmethod
    def updateUser(user_id, login_session, dbSession):
    # checks is user picture or name has been updated 
    #  returns user.id

       user = User.getUser(user_id,dbSession);
       if user.name != login_session['username'] or user.picture != login_session['picture']:
          user.name = login_session['username']
          user.picture = login_session['picture']
          dbSession.add(user)
          dbSession.commit()
       return user.id

    @staticmethod
    def getUser(user_id, dbSession):
    # returns user obect if user exist else none
       try:
           user = dbSession.query(User).filter_by(id=user_id).one()
           return user
       except:
           return None

    @staticmethod
    def getUserID(email, dbSession):
    # returns user id if user exist else none
       try:
           user = dbSession.query(User).filter_by(email=email).one()
           return user.id
       except:
           return None


#Catalogue Categories
#Each category must be assigned to a user 
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(400))
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    # When a category is deleted also delete category's child item objects
    items = relationship("Item", cascade="all, delete-orphan")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
        }

    # Category Helper Functions
    @staticmethod
    def getCategories(dbSession): 
        # returns all categories in table, else None.
        try:
           categories = dbSession.query(Category).all()
           return categories
        except:
           return None

    @staticmethod
    def getCategory(category_id, dbSession):
        # retruns single category , else None
        try:
           category = dbSession.query(Category).filter_by(id=category_id).one()
           return category
        except:
           return None


#Catalogue items 
#each item must belong to a category 
class Item(Base):
    __tablename__ = 'item'

    name = Column(String(100), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(400))
    price = Column(String(8), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'),nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
        }

     # Category Helper Functions
    @staticmethod
    def getCategoryItems(category_id, dbSession):
        # retruns all items belonging to a single category, else None
        try:
           items = dbSession.query(Item).filter_by(category_id=category_id).all()
           return items
        except:
           return None

    @staticmethod
    def getItem(item_id, dbSession):
        # returns a single category, else None
        try:
           item = dbSession.query(Item).filter_by(id=item_id).one()
           return item
        except:
           return None

if __name__ == '__main__':
    engine = create_engine('sqlite:///catalogue.db')
    Base.metadata.create_all(engine)
    engine.dispose()