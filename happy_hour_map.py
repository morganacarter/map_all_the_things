import time
from geopy.geocoders import GoogleV3
geolocator=GoogleV3()

def csv_to_dict(filename,delimiter=","):
	'''
	A function that opens a csv file and turns it into a nested dictionary 
	with items in each row as a dictionary.
	'''
	with open(filename,'r') as csvfile:
		rows=csvfile.read().splitlines()

		for index, row in enumerate(rows):
			rows[index]=row.split(delimiter)

		#remove the header so we can iterate over it
		header=rows.pop(0)
		
		#create the nested dictionary that uses row numbers as keys to fake 'order'
		nestdict={}
		#loop over each row in the csv
		for index, row in enumerate(rows):
			#this dict comprehension loops over the pairs created when we zip the header and row lists together
			#and creates a dictionary for that line with the header as the key and row as the value 
			line={key:value for key,value in zip(header,row)}
			#then we add that line to our nested dictionary as a value, with the key being the index (row number)
			nestdict[index]=line

	return nestdict

bars=csv_to_dict("happy_hours.csv",",")

resources=[]

for key in bars:
	time.sleep(1)
	try:
		address, (latitude, longitude) = geolocator.geocode(bars[key]["Address"])
	#print bars[key]["Address"]
		#print address, latitude, longitude
	except:
		print "Unable to find location for ", bars[key]["Name"]

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
        		"marker-symbol": "bar",
        		"name": bars[key]["Name"],
        		"address": bars[key]["Address"],
        		"day": bars[key]["Day"],
        		"hours": bars[key]["Time"],
        		"specials": bars[key]["Details"]
      		}
    	}
    	resources.append(item)

geo={
	"type":"FeatureCollection",
	"features": resources
}


import json

with open("happy_hours.json","w") as jsonfile:
	jsonfile.write(json.dumps(geo, indent=4,sort_keys=True))
	