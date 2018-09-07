import cgi
import logging
import sys
import urlparse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

logging.basicConfig()

if sys.version_info[0] < 3:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
else:
    from http.server import BaseHTTPRequestHandler, HTTPServer


class WebServerHandler(BaseHTTPRequestHandler):
    class WebServerException(Exception):
        def __init__(self, message):
            if sys.version_info[0] < 3:
                super(Exception, self).__init__(message)
            else:
                super().__init__(message)
            
    @property
    def logger(self):
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.DEBUG)
        return logger

    def do_GET(self):
        try:
            output = ["<!DOCTYPE html>"]
            if self.path == "/restaurants":
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output.append("<html>")
                output.append("<head><style>\
                                 body { font-size: 110%; }\
                                 #entry { font-size: 130%; }\
                                 #new { font-size: 130%; }\
                                 </style></head>")
                output.append("<body>")

                engine = create_engine('sqlite:///restaurantmenu.db')
                Base.metadata.bind = engine
                DBSession = sessionmaker(bind = engine)
                session = DBSession()
                entries = session.query(Restaurant).all()
                for restaurant in entries:
                    output.append('<p>')
                    output.append('<div id="entry">{}</div>'.format(restaurant.name))
                    output.append('<a href="edit_restaurant?name={}">Edit</a> '.format(restaurant.name))
                    output.append('<a href="delete_restaurant?name={}">Delete</a>'.format(restaurant.name))
                    output.append('</p>')

                output.append('<div id="new"><a href="new_restaurant">Add a new restaurant</a></div>')
            elif self.path == "/new_restaurant":
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output.append("<html>")
                output.append("<head><style> body { font-size: 120%; }</style></head>")
                output.append("<body>")

                output.append('<H1>Add a New Restaurant</H1>')
                output.append("<form method='POST' enctype='multipart/form-data' action='/add_restaurant'>\
                              Restaurant Name: <input name='name' type='text'>\
                              <input type='submit' value='Add'></form>")
            elif self.path.startswith("/edit_restaurant?"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output.append("<html>")
                output.append("<head><style> body { font-size: 120%; }</style></head>")
                output.append("<body>")


                path_parts = urlparse.urlparse(self.path)
                self.logger.debug('Path Parts: {}'.format(path_parts))
                self.logger.debug('Query: {}'.format(path_parts.query))
                query_parameters = urlparse.parse_qs(path_parts.query)
                self.logger.debug('Query Parameters: {}'.format(query_parameters))
                restaurant_name = query_parameters['name'][0]
                output.append('<H1>Rename Restaurant "{}"</H1>'.format(restaurant_name))
                output.append("<form method='POST' enctype='multipart/form-data' action='/rename_restaurant'>\
                              New Restaurant Name: <input name='name' type='text'>\
                              <input type='submit' value='Rename'>\
                              <input type='hidden' name='old_name' value='{}'></form>".format(restaurant_name))

            else:
                raise self.WebServerException('Unsupported route.')


            output.append("</body</html>")
            output = ''.join(output)
            self.wfile.write(output)
            self.logger.debug(output)
        except (IOError, self.WebServerException) as e:
            self.logger.error(e)
            self.send_error(404, "File Not Found {}".format(self.path))

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            content_type, parameters = cgi.parse_header(self.headers.getheader('content-type'))
            if content_type == 'multipart/form-data':
                self.logger.debug('Processing multipart/form-data')
                fields = cgi.parse_multipart(self.rfile, parameters)

                output = []
                if self.path == "/add_restaurant":
                    restaurant_name = fields.get('name')[0]
                    self.logger.debug(restaurant_name)

                    output.append("<html><body>")

                    engine = create_engine('sqlite:///restaurantmenu.db')
                    Base.metadata.bind = engine
                    DBSession = sessionmaker(bind = engine)
                    session = DBSession()
                    restaurants = session.query(Restaurant).filter_by(name=restaurant_name)
                    if restaurants.count() > 0:
                        output.append("  <h2> Restaurant {} already exists. </h2>".format(restaurant_name))
                    else:
                        restaurant = Restaurant(name = restaurant_name)
                        session.add(restaurant)
                        session.commit()
                        output.append('  <h2> Added restaurant "{}". </h2>'.format(restaurant_name))
                    output.append('<a href="restaurants">View Restaurants</a>')
                elif self.path == "/rename_restaurant":
                    self.logger.debug('Fields: {}'.format(fields))
                    restaurant_name = fields.get('old_name')[0]
                    self.logger.debug(restaurant_name)

                    output.append("<html><body>")

                    engine = create_engine('sqlite:///restaurantmenu.db')
                    Base.metadata.bind = engine
                    DBSession = sessionmaker(bind = engine)
                    session = DBSession()
                    restaurants = session.query(Restaurant).filter_by(name=restaurant_name)
                    if restaurants.count() < 0:
                        output.append("  <h2> Restaurant {} does not exists. </h2>".format(restaurant_name))
                    else:
                        restaurant = restaurants[0]
                        restaurant.name = fields.get('name')[0]
                        session.add(restaurant)
                        session.commit()
                        output.append('  <h2> Renamed restaurant "{}" to "{}". </h2>'.format(restaurant_name, restaurant.name))
                    output.append('<a href="restaurants">View Restaurants</a>')

                output.append("</body</html>")
                output = ''.join(output)
                self.wfile.write(output)
                self.logger.debug(output)
            self.logger.debug('Done with POST processing.')
        except IOError as e:
            self.logger.error(e)

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("Web server running on port {}".format(port))
        server.serve_forever()
    except KeyboardInterrupt:
        print("^C entered. Stopping web server...")
        server.socket.close()

if __name__ == '__main__':
    main()
