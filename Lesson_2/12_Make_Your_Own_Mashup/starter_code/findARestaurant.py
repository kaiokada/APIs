from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "PIZQJFH0SVN21OTCQAXQNANTXM10Y1EI4R2HWSVCBKC11UYM"
foursquare_client_secret = "HMQFWLKWHMHTT4JQ0EDIXAKBGHGUO1YTLLSXYEJQ3O0DSDYH"


def findARestaurant(mealType,location):
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
	latitude, longitude = getGeocodeLocation(location)
	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
	url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s&intent=browse&radius=10000'% 
		(foursquare_client_id, foursquare_client_secret, latitude, longitude, mealType))
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])

	#3. Grab the first restaurant
	first_venue = result['response']['venues'][0]
	#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
	venue_id = first_venue['id']
	img_url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&client_secret=%s&v=20130815'% (venue_id, foursquare_client_id, foursquare_client_secret))
	img_result = json.loads(h.request(img_url, 'GET')[1])
	
	#5. Grab the first image
	#6. If no image is available, insert default a image url
	first_photo_url = ""
	if (img_result['meta']['code'] == 429): 
		first_photo_url = "Quota Exceeded"
	elif (img_result['response']['photos']['count'] != 0):
		first_photo = img_result['response']['photos']['items'][0]
		first_photo_url = first_photo['prefix'] + "300x300" + first_photo['suffix']
	else:
		first_photo_url = "Default Photo"
	
	#7. Return a dictionary containing the restaurant name, address, and image url	
	print("Restaurant Name: " + first_venue['name'])
	print("Restaurant Address: " + ', '.join(first_venue['location']['formattedAddress']))
	print("Image: " + first_photo_url)
	print

if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney, Australia")
