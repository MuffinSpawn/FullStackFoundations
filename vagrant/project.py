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
    restaurants = session.query(Restaurant).all()
    return flask.render_template('restaurants.html', restaurants=restaurants)

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

@app.route('/restaurant/<int:restaurant_id>/')
def listMenuItems(restaurant_id=0):
    session = DBSession()
    menu_items = None
    output = []

    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return flask.render_template('menu.html', restaurant=restaurant, menu_items=menu_items)

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id=0):
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if flask.request.method == 'POST':
        restaurant.name = flask.request.values.get('name')
        session.add(restaurant)
        session.commit()
        return flask.redirect("/restaurants", code=301)

    return flask.render_template('edit_restaurant.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id=0):
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if flask.request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        return flask.redirect("/restaurants", code=301)

    return flask.render_template('delete_restaurant.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/items/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if flask.request.method == 'POST':
        name = flask.request.values.get('name')
        description = flask.request.values.get('description')
        course = flask.request.values.get('course')
        price = flask.request.values.get('price')
        menu_item = MenuItem(name=name, description=description, course=course, price=price, restaurant_id=restaurant_id)
        session.add(menu_item)
        session.commit()
        return flask.redirect("/restaurant/{}/".format(restaurant_id), code=301)

    courses = ['Appetizer', 'Beverage', 'Dessert', 'Entree']

    return flask.render_template('new_menu_item.html', restaurant=restaurant, courses=courses)

@app.route('/restaurant/<int:restaurant_id>/item/<int:menu_item_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_item_id):
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_item = session.query(MenuItem).filter_by(id=menu_item_id).one()
    if flask.request.method == 'POST':
        menu_item.name = flask.request.values.get('name')
        menu_item.description = flask.request.values.get('description')
        menu_item.course = flask.request.values.get('course')
        menu_item.price = flask.request.values.get('price')
        session.add(menu_item)
        session.commit()
        return flask.redirect("/restaurant/{}/".format(restaurant_id), code=301)

    courses = ['Appetizer', 'Beverage', 'Dessert', 'Entree']

    return flask.render_template('edit_menu_item.html', restaurant=restaurant, menu_item=menu_item, courses=courses)

@app.route('/restaurant/<int:restaurant_id>/item/<int:menu_item_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_item_id):
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_item = session.query(MenuItem).filter_by(id=menu_item_id).one()
    if flask.request.method == 'POST':
        session.delete(menu_item)
        session.commit()
        return flask.redirect("/restaurant/{}/".format(restaurant_id), code=301)

    return flask.render_template('delete_menu_item.html', restaurant=restaurant, menu_item=menu_item)


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)