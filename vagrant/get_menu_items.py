import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

def main():
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind = engine)
    session = DBSession()

    entries = session.query(MenuItem).all()
    for item in entries:
        restaurant_id = item.restaurant_id
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id)[0]
        print('{} ({})'.format(item.name, restaurant.name))

if __name__ == '__main__':
    main()