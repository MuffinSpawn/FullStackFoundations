import logging
logging.basicConfig()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

import flask
app = flask.Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

@app.route('/')
@app.route('/restaurants/')
def listRestaurants():
    session = DBSession()
    output = []

    restaurants = session.query(Restaurant).all()
    return flask.render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/<int:restaurant_id>/')
def listMenuItems(restaurant_id=0):
    session = DBSession()
    menu_items = None
    output = []

    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return flask.render_template('menu.html', restaurant=restaurant, menu_items=menu_items)

@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant():
    if flask.request.method == 'POST':
        restaurant_name = flask.request.values.get('name')
        session = DBSession()
        restaurant = Restaurant(name = restaurant_name)
        session.add(restaurant)
        session.commit()
        return flask.redirect("/restaurants", code=301)

    return flask.render_template('new_restaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id=0):
    if flask.request.method == 'POST':
        session = DBSession()
        restaurant = session.query(Restaurants).filter_by(id=restaurant_id).one()
        session.delete(restaurant)
        session.commit()
        return flask.redirect("/restaurants", code=301)

    return flask.render_template('edit_restaurant.html')

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id=0):
    if flask.request.method == 'POST':
        session = DBSession()
        restaurant = session.query(Restaurants).filter_by(id=restaurant_id).one()
        session.delete(restaurant)
        session.commit()
        return flask.redirect("/restaurants", code=301)

    return flask.render_template('delete_restaurant.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)