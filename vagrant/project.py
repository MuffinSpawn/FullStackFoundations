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
    for restaurant in restaurants:
        output.append('<a href="/restaurants/{}/">{}</a><br/>'.format(restaurant.id, restaurant.name))
    return ''.join(output)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id=0):
    session = DBSession()
    menu_items = None
    output = []

    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    output.append('<a href="/restaurants">Back</a><BR/>')
    output.append('<H1>{} Menu</H1>'.format(restaurant.name))

    for menu_item in menu_items:
        output.append('{}<BR/>'.format(menu_item.name))
        output.append('{}<BR/>'.format(menu_item.price))
        output.append('{}<BR/>'.format(menu_item.description))
        output.append('<BR/>')

    output.append('<a href="/restaurants">Back</a><BR/>')

    return ''.join(output)

@app.route('/restaurants/new/', methods=['GET', 'POST'])
def addRestaurant():
    output = []
    output.append('<a href="/restaurants">Back</a><BR/>')
    output.append('<H1>Add New Restaurant</H1>')

    if flask.request.method == 'POST':
        restaurant_name = flask.request.values.get('name')
        session = DBSession()
        restaurant = Restaurant(name = restaurant_name)
        session.add(restaurant)
        session.commit()
        return flask.redirect("/restaurants", code=301)

    output.append('<form method="POST" enctype="multipart/form-data" action="/restaurants/new/">')
    output.append('Restaurant Name: <input name="name" type="text">')
    output.append('<input type="submit" value="Add"></form>')
    return ''.join(output)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)