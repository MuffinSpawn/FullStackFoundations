import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

def main():
    if len(sys.argv) < 6:
        print('Usage: python add_menu_item.py NAME DESCRIPTION COURSE PRICE RESTAURANT_NAME...')
        quit()

    name = sys.argv[1]
    description = sys.argv[2]
    course = sys.argv[3]
    price = sys.argv[4]
    restaurant_name = sys.argv[5]

    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind = engine)
    session = DBSession()

    # find the named restaurant whose menu we should add the item to
    restaurants = session.query(Restaurant).filter_by(name=restaurant_name)
    if restaurants.count() == 0:
        print("Restaurant '{}' not found.".format(restaurant_name))
        quit()
    restaurant = restaurants[0]

    menu_item = MenuItem(name=name, description=description, course=course, price=price,
                         restaurant=restaurant)
    session.add(menu_item)

    session.commit()

if __name__ == '__main__':
    main()