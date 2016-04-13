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
from geopy.geocoders.base import ERROR_CODE_MAP
import geopy

def get_coords(address):
    try:
#        geolocator = Nominatim(timeout=3, scheme='http')  # Nominatim seems to have stopped working, see github geopy
        geolocator = geopy.geocoders.GoogleV3(timeout=3)
#        geolocator = geopy.geocoders.GeocodeFarm(timeout=20)
        try:   
            location = geolocator.geocode(address, timeout=3, exactly_one=True)  # Only 1 location for this address
            if location == None:
                print "Geocoder Service timed out or Airfield: ", address, " not known by geocode locator service. Check settings"
                return False
            ele = geocoder.elevation(address)
            print "Geolocator worked"
            return location.latitude, location.longitude, ele.meters
        except ERROR_CODE_MAP[400]:
            print " ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[400]
        except ERROR_CODE_MAP[401]:
            print " ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[401]
        except ERROR_CODE_MAP[402]:
            print " ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[402]
        except ERROR_CODE_MAP[403]:
            print " ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[403]
        except ERROR_CODE_MAP[407]:
            print " ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[407]
        except ERROR_CODE_MAP[412]:
            print " ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[412]
        except ERROR_CODE_MAP[413]:
            print " ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[413]
        except ERROR_CODE_MAP[414]:
            print " ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[414]
        except ERROR_CODE_MAP[502]:
            print " ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[502]
        except ERROR_CODE_MAP[503]:
            print " ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[503]
        except ERROR_CODE_MAP[504]:
            print " ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[503]
        return False
    except GeocoderTimedOut as e:
        print "Geocoder Service timed out for Airfield: ", address
        return False
