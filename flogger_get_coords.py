#
# Function to determine latitude, longitude and elevation given location place name details.
# Details are returned as a list.
# For example if called as:
# loc = get_coords("My Gliding Club UK")
#   then:
#        latitude = loc[0], longitude = loc[1], elevation = loc[2]
#
#
from geopy.geocoders import Nominatim
import geocoder
from geopy.exc import GeocoderTimedOut
import time

def get_coords(address):
    while True:
        try:
            geolocator = Nominatim()
            location = geolocator.geocode(address)
            ele = geocoder.elevation(address)
            break
        except GeocoderTimedOut as e:
            time.sleep(1)
            print 'Geocoder Service timed out'
    
    return location.latitude, location.longitude, ele.meters
# loc = get_coords("Yorkshire Gliding Club UK")
# print "latitude: ", loc[0], " longitude: ", loc[1], " elevation: ", loc[2]
