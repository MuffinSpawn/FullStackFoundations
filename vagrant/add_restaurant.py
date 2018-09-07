import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

def main():
    if len(sys.argv) <= 1:
        print('Usage: python add_restaurant.py NAME [NAME ]...')
        quit()

    restaurant_name = sys.argv[1]

    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind = engine)
    session = DBSession()

    restaurant = Restaurant(name = "Pizza Palace")
    session.add(restaurant)

    session.commit()

if __name__ == '__main__':
    main()