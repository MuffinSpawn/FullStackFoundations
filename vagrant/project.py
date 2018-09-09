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
    output.append('<!DOCTYPE html>')
    output.append('<html lang="en"><head>')
    output.append('<style rel="stylesheet">')
    output.append('#entry { font-size: 16pt; }')
    output.append('p { font-size: 16pt; font-weight: bold }')
    output.append('</style>')
    output.append('</head>')

    output.append('<body>')
    output.append('<p><a href="/restaurants/new">Add New Restaurant</a></p>')
    restaurants = session.query(Restaurant).all()
    for restaurant in restaurants:
        output.append('<div id="entry">{}</div>'.format(restaurant.name))
        output.append('<a href="/restaurant/{}/">View Menu</a> '.format(restaurant.id))
        output.append('<a href="/restaurant/{}/edit/">Edit</a> '.format(restaurant.id))
        output.append('<a href="/restaurant/{}/delete/">Delete</a><br/>'.format(restaurant.id))
        output.append('<br/>')
    output.append('</body></html>')
    return ''.join(output)

@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id=0):
    session = DBSession()
    menu_items = None
    output = []

    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    output.append('<!DOCTYPE html>')
    output.append('<html lang="en"><head>')
    output.append('<style rel="stylesheet">')
    output.append('#entry { font-size: 16pt; }')
    output.append('p { font-size: 16pt; font-weight: bold }')
    output.append('</style>')
    output.append('</head>')

    output.append('<body>')
    output.append('<a href="/restaurants">Back</a><BR/>')
    output.append('<H1>{} Menu</H1>'.format(restaurant.name))
    output.append('<p><a href="/restaurant/{}/items/new">Add New Menu Item</a></p>'.format(restaurant.id))

    for menu_item in menu_items:
        output.append('{}<BR/>'.format(menu_item.name))
        output.append('{}<BR/>'.format(menu_item.price))
        output.append('{}<BR/>'.format(menu_item.description))
        output.append('<a href="/restaurant/{}/item/{}/edit/">Edit'.format(restaurant.id, menu_item.id))
        output.append('<BR/>')

    output.append('<BR/>')
    output.append('<a href="/restaurants">Back</a><BR/>')
    output.append('</body></html>')

    return ''.join(output)

@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant():
    if flask.request.method == 'POST':
        restaurant_name = flask.request.values.get('name')
        session = DBSession()
        restaurant = Restaurant(name = restaurant_name)
        session.add(restaurant)
        session.commit()
        return flask.redirect("/restaurants", code=301)

    output = []
    output.append('<!DOCTYPE html>')
    output.append('<html lang="en"><head>')
    output.append('<style rel="stylesheet"> #entry { font-size: 16pt; } </style>')
    output.append('</head>')

    output.append('<body>')
    output.append('<a href="/restaurants">Back</a><BR/>')
    output.append('<H1>Add New Restaurant</H1>')
    output.append('<form method="POST" enctype="multipart/form-data" action="/restaurants/new/">')
    output.append('Restaurant Name: <input name="name" type="text">')
    output.append('<input type="submit" value="Add"></form>')
    output.append('</body></html>')
    return ''.join(output)

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id=None):
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if flask.request.method == 'POST':
        restaurant_name = flask.request.values.get('name')
        restaurant.name = restaurant_name
        session.add(restaurant)
        session.commit()
        return flask.redirect("/restaurants", code=301)

    output = []
    output.append('<!DOCTYPE html>')
    output.append('<html lang="en"><head>')
    output.append('<style rel="stylesheet"> #entry { font-size: 16pt; } </style>')
    output.append('</head>')

    output.append('<body>')
    output.append('<a href="/restaurants">Back</a><BR/>')
    output.append('<a href="/restaurant/{}/">Back</a><BR/>'.format(restaurant_id))
    output.append('<H1>Rename Restaurant "{}"</H1>'.format(restaurant.name))
    output.append('<form method="POST" enctype="multipart/form-data" action="/restaurant/{}/edit/">'.format(restaurant.id))
    output.append('Restaurant Name: <input name="name" type="text">')
    output.append('<input type="submit" value="Rename"></form>')
    output.append('</body></html>')
    return ''.join(output)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id=None):
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if flask.request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        return flask.redirect("/restaurants", code=301)

    output = []
    output.append('<!DOCTYPE html>')
    output.append('<html lang="en"><head>')
    output.append('<style rel="stylesheet"> #entry { font-size: 16pt; } </style>')
    output.append('</head>')

    output.append('<body>')
    output.append('<a href="/restaurants">Back</a><BR/>')
    output.append('<H1>Delete Restaurant "{}"</H1>'.format(restaurant.name))
    output.append('<form method="POST" enctype="multipart/form-data" action="/restaurant/{}/delete/">'.format(restaurant.id))
    output.append('<input type="submit" value="Delete"></form>')
    output.append('</body></html>')
    return ''.join(output)

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

    output = []
    output.append('<!DOCTYPE html>')
    output.append('<html lang="en"><head>')
    output.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    output.append('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">')
    output.append('<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>')
    output.append('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>')
    output.append('<style rel="stylesheet"> #entry { font-size: 16pt; } </style>')
    output.append('</head>')

    output.append('<body>')
    output.append('<a href="/restaurants">Back</a><BR/>')
    output.append('<H1>Add New Menu Item at "{}"</H1>'.format(restaurant.name))
'''
<div class="container">
  <div class="row">
    <div class="col-sm-4">
      <h3>Column 1</h3>
      <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit...</p>
      <p>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris...</p>
    </div>
    <div class="col-sm-4">
      <h3>Column 2</h3>
      <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit...</p>
      <p>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris...</p>
    </div>
    <div class="col-sm-4">
      <h3>Column 3</h3>        
      <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit...</p>
      <p>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris...</p>
    </div>
  </div>
</div>
'''
    output.append('<form method="POST" enctype="multipart/form-data" action="/restaurant/{}/new/">'.format(restaurant_id))
    output.append('Name: <input name="name" type="text"><br/>')
    output.append('Description: <input name="description" type="text"><br/>')
    output.append('Course: <select name="course">')
    options = ['Appetizer', 'Beverage', 'Dessert', 'Entree']
    for option in options:
        output.append('  <option value="{0}">{0}</option>'.format(option))
    output.append('</select><br/>')
    output.append('Price: <input name="price" type="text"><br/>')
    output.append('<input type="submit" value="Add"><br/></form>')
    output.append('</body></html>')
    return ''.join(output)

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

    output = []
    output.append('<!DOCTYPE html>')
    output.append('<html lang="en"><head>')
    output.append('<style rel="stylesheet"> #entry { font-size: 16pt; } </style>')
    output.append('</head>')

    output.append('<body>')
    output.append('<a href="/restaurant/{}/">Back</a><BR/>'.format(restaurant_id))
    output.append('<H1>Edit Menu Item at "{}"</H1>'.format(restaurant.name))
    output.append('<form method="POST" enctype="multipart/form-data" action="/restaurant/{}/item/{}/edit/">'.format(restaurant_id, menu_item_id))
    output.append('Name: <input name="name" type="text" value="{}"><br/>'.format(menu_item.name))
    output.append('Description: <input name="description" type="text" value="{}"><br/>'.format(menu_item.description))
    output.append('Course: <select name="course">')
    options = ['Appetizer', 'Beverage', 'Dessert', 'Entree']
    for option in options:
        if menu_item.course == option:
            output.append('  <option value="{0}" selected>{0}</option>'.format(option))
        else:
            output.append('  <option value="{0}">{0}</option>'.format(option))
    output.append('</select><br/>')
    output.append('Price: <input name="price" type="text" value="{}"><br/>'.format(menu_item.price))
    output.append('<input type="submit" value="Add"><br/></form>')

    output.append('<br/>')
    output.append('<a href="/restaurant/{}/">Back</a><BR/>'.format(restaurant_id))
    output.append('</body></html>')
    return ''.join(output)


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)