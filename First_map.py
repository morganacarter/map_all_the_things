import time
from geopy.geocoders import GoogleV3
geolocator=GoogleV3()

with open("schools_zero.txt","r") as schoolfile:
	schools=schoolfile.read().splitlines()

resources=[]

for name in schools:
	time.sleep(1)
	try:
		address, (latitude,longitude) = geolocator.geocode(name)

		#print address, latitude, longitude
	except:
		print "Unable to find location for ", name

	else: 
		item={
      		"type": "Feature",
      		"geometry": {
        		"type": "Point",
        		"coordinates": [
          			longitude,
          			latitude
        		]
      		},
      		"properties": {
        		"marker-symbol": "rocket",
        		"name": name,
        		"address": address
      		}
    	}
    	resources.append(item)

geo={
	"type":"FeatureCollection",
	"features": resources
}

import json

with open("schools_zero.json","w") as jsonfile:
	jsonfile.write(json.dumps(geo, indent=4,sort_keys=True))