from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)



foursquare_client_id = 'PIZQJFH0SVN21OTCQAXQNANTXM10Y1EI4R2HWSVCBKC11UYM'

foursquare_client_secret = 'HMQFWLKWHMHTT4JQ0EDIXAKBGHGUO1YTLLSXYEJQ3O0DSDYH'

google_api_key = 'AIzaSyAe-NySTc8skLAh7KAGzoeP_8KHJVPyauA'


app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
	engine = create_engine('sqlite:///restaurants.db')
	Base.metadata.bind = engine
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
  #YOUR CODE HERE
	if request.method == 'GET':
		restaurants = session.query(Restaurant).all()
		#for r in restaurants:
	#		session.delete(r)
	#		session.commit()
		return jsonify(restaurants=[r.serialize for r in restaurants])

	elif request.method == 'POST':
		location = request.args.get('location', '')
		mealType = request.args.get('mealType', '')
		result = findARestaurant(mealType, location)
		new_restaurant = Restaurant(restaurant_name = result['name'], restaurant_address = result['address'], restaurant_image = result['image'])
		session.add(new_restaurant)
		session.commit()
		return jsonify(Restaurant = new_restaurant.serialize)

    
@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
	engine = create_engine('sqlite:///restaurants.db')
	Base.metadata.bind = engine
	DBSession = sessionmaker(bind=engine)
	session = DBSession()

	restaurant = session.query(Restaurant).filter_by(id = id).one()
	#YOUR CODE HERE
	if request.method == 'GET':
		
		return jsonify(Restaurant = restaurant.serialize)
	elif request.method == 'PUT':
		name = request.args.get('name', '')
		location = request.args.get('location', '')
		image = request.args.get('image', '')

		restaurant.restaurant_name = name
		restaurant.restaurant_address = location
		restaurant.restaurant_image = image
		session.add(restaurant)
		session.commit()
		return jsonify(Restaurant = restaurant.serialize)
	elif request.method == 'DELETE':
		session.delete(restaurant)
		session.commit()
		return jsonify(Restaurant = restaurant.serialize)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


  
