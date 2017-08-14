#!/usr/bin/env python

from flask import Flask, render_template, request, make_response
from flask import session as login_session
from flask import redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import json
import requests
import random
import string
import httplib2

# DB table objects
from database_setup import Base, Category, Item, User

'''This file contains all routes for the catalogue app
'''

app = Flask(__name__)

engine = create_engine('sqlite:///catalogue.db')
Base.metadata.bind = engine

DBSessionmaker = sessionmaker(bind=engine)
dbSession = DBSessionmaker()

SCOPES = 'https://www.googleapis.com/auth/plus.login'
CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = 'Catalogue App'


@app.route('/login')
def login():
    # Create anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        app.logger.error(reponse)
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        app.logger.error(response)
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        app.logger.error(response)
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        app.logger.error(response)
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        app.logger.error(response)
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        # udpate access token to new one from google.
        login_session['access_token'] = credentials.access_token
        app.logger.debug(response)
        # exit login here since user is already logged in
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Get user info from DB or add  or Update user
    dbUserID = User.getUserID(login_session['email'], dbSession)
    if not dbUserID:
        dbUserID = User.createUser(login_session, dbSession)
    else:
        dbUserID = User.updateUser(dbUserID, login_session, dbSession)

    login_session['user_id'] = dbUserID

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: '
    output += '150px;-webkit-border-radius: 150px; '
    output += '-moz-border-radius: 150px;">'
    return output


@app.route('/gdisconnect')
def gdisconnect():
    # get token for login_session
    access_token = login_session.get('access_token')

    # user not login redirect to home
    if access_token is None:
        app.logger.debug('gdisconnect user not loggin in.')
        flash('User was not logged Redirected to Homepage.')
        return goHome()

    # revoke google oauth token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    # log response code from google for debug
    if result['status'] == '200':
        app.logger.debug('Successfully disconnected. user Session Ended')
    else:
        app.logger.error('Failed to revoke google token. User session ended')

    # Always clear the login_session of all data on log out, for
    # all response codes from google. This is ok because google
    # is only oauth provider implemented.
    login_session.clear()

    # flash and redirect to home
    flash('User was logged out')
    return goHome()


# Show all Catalogue Categories
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = Category.getCategories(dbSession)
    userStatus = getUserStatus(None)
    welcomeFlash(userStatus)
    # userStatus determines public vs logged in user page view
    return render_template('catalog.html', categories=categories,
                           user=userStatus)


# Show a category with its items listed
@app.route('/category/<int:category_id>/')
def showCategory(category_id):
    category = Category.getCategory(category_id, dbSession)

    if category is None:
        # only directly accessing url, with bad data,
        # causes this ignore and return to home.
        return goHome()

    items = Item.getItems(category_id, dbSession)
    creator = User.getUser(category.user_id, dbSession)

    userStatus = getUserStatus(category.user_id)
    welcomeFlash(userStatus)
    # userStatus determines public vs logged in user page view
    return render_template('category.html', items=items,
                           category=category, creator=creator, user=userStatus)


# Show an item
@app.route('/Item/<int:item_id>/')
def showItem(item_id):
    item = Item.getItem(item_id, dbSession)

    if item is None:
        # only directly accessing url, with with bad data,
        # causes this ignore and return to home.
        return goHome()

    category = Category.getCategory(item.category_id, dbSession)
    userStatus = getUserStatus(category.user_id)
    welcomeFlash(userStatus)
    # userStatus determines public vs logged in user page view
    return render_template('item.html', item=item, user=userStatus)


# Create a new category
@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if not isLoggedIn():
        notloggedInFlash()
        return goHome()

    if request.method == 'POST':
        newCategory = Category.createCategory(
                      request.form, login_session, dbSession)
        actionFlash(newCategory, 'Added')
        return goHome()
    else:
        welcomeFlash(getUserStatus(None))
        return render_template('newCategory.html')


@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    categoryToEdit = Category.getCategory(category_id, dbSession)

    if categoryToEdit is None:
        # only directly accessing url, with with bad data,
        # causes this ignore and return to home.
        return goHome()

    userStatus = getUserStatus(categoryToEdit.user_id)
    if userStatus != 2:
        notOwnerFlash()
        return goHome()

    if request.method == 'POST':
        categoryToEdit = Category.updateCategory(
                         request.form, categoryToEdit, dbSession)
        actionFlash(categoryToEdit, 'edited')
        return redirect(url_for('showCategory', category_id=categoryToEdit.id))
    else:
        welcomeFlash(userStatus)
        return render_template(
            'editCategory.html', category=categoryToEdit)


# delete a category and all child items
@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = Category.getCategory(category_id, dbSession)
    if categoryToDelete is None:
        # only directly accessing url, with with bad data,
        # causes this ignore and return to home.
        return goHome()

    userStatus = getUserStatus(categoryToDelete.user_id)
    if userStatus != 2:
        notOwnerFlash()
        return goHome()

    if request.method == 'POST':
        Category.deleteCategory(categoryToDelete, dbSession)
        actionFlash(categoryToDelete, 'deleted')
        return goHome()
    else:
        welcomeFlash(userStatus)
        return render_template(
            'deleteCategory.html', category=categoryToDelete)


# create a new item for a specific category
@app.route('/category/<int:category_id>/item/new/', methods=['GET', 'POST'])
def newItem(category_id):
    itemCategory = Category.getCategory(category_id, dbSession)

    if itemCategory is None:
        # only directly accessing url, with with bad data,
        # causes this ignore and return to home.
        return goHome()

    userStatus = getUserStatus(itemCategory.user_id)
    if userStatus != 2:
        notOwnerFlash()
        return goHome()

    if request.method == 'POST':
        newItem = Item.createItem(request.form,
                                  itemCategory.id, dbSession)
        actionFlash(newItem, 'added')
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        welcomeFlash(userStatus)
        return render_template('newItem.html', category_id=category_id)


# edit an item then display it
@app.route('/item/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(item_id):

    itemToEdit = Item.getItem(item_id, dbSession)

    if itemToEdit is None:
        # only directly accessing url, with bad data,
        # causes this ignore and return to home.
        return goHome()

    itemCategory = Category.getCategory(itemToEdit.category_id, dbSession)

    userStatus = getUserStatus(itemCategory.user_id)
    if userStatus != 2:
        notOwnerFlash()
        return goHome()

    if request.method == 'POST':
        itemToEdit = Item.updateItem(request.form,
                                     itemToEdit, dbSession)
        actionFlash(itemToEdit, 'edited')
        return redirect(url_for('showItem', item_id=itemToEdit.id))
    else:
        welcomeFlash(userStatus)
        return render_template('editItem.html', item=itemToEdit)


# Delete and item then return to  parent category page
@app.route('/item/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(item_id):
    itemToDelete = Item.getItem(item_id, dbSession)

    if itemToDelete is None:
        # only directly accessing url, with with bad data,
        # causes this ignore and return to home.
        return goHome()

    itemCategory = Category.getCategory(itemToDelete.category_id, dbSession)

    userStatus = getUserStatus(itemCategory.user_id)
    if userStatus != 2:
        notOwnerFlash()
        return goHome()

    if request.method == 'POST':
        deleted = Item.deleteItem(itemToDelete, dbSession)
        actionFlash(deleted, 'deleted')
        return redirect(url_for('showCategory',
                                category_id=itemToDelete.category_id))
    else:
        welcomeFlash(userStatus)
        return render_template('deleteItem.html', item=itemToDelete)


# helper functions
def goHome():
    '''Homepage redirect'''
    return redirect(url_for('showCatalog'))


def getUserStatus(user_id):
    '''Returns 0 for loggged out,  1 for logged in
       2 for owner     '''
    status = 0
    if isLoggedIn():
        status = 1
    if isOwner(user_id):
        status = 2
    return status


def isLoggedIn():
    if 'username' not in login_session:
        return False
    return True


def isOwner(user_id):
    '''parameter user_id is object.user_id
       from database table'''
    if (user_id is None or
       user_id != login_session.get('user_id')):
        return False
    return True


def welcomeFlash(userStatus):
    if userStatus > 0:
        return flash("Logged in as %s" % login_session['username'])
    return None


def notOwnerFlash():
    return flash('You must be logged in as Category Owner to change' +
                 ' an item or category ! Redirecting to Homepage...')


def notloggedInFlash():
    return flash('You must be logged in to add a category!' +
                 ' Redirecting to Homepage...')


def actionFlash(object, action):
    if object is None:
        return flash(action + " failed. Try again later.")
    return flash(object.name + " was " + action)

if __name__ == '__main__':
        app.secret_key = 'super_secret_key'
        app.debug = True
        app.run(host='0.0.0.0', port=5000)
