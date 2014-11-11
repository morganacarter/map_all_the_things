import time
from geopy.geocoders import GoogleV3
geolocator=GoogleV3()

def csv_to_dict(Ohio_Courthouses,delimiter=","):
	'''
	A function that opens a csv file and turns it into a nested dictionary 
	with items in each row as a dictionary.
	'''
	with open(mapping_sample_OH_courthouses,'r') as csvfile:
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

courts=csv_to_dict("mapping_sample_OH_courthouses.csv",",")

resources=[]

for key in courts:
	time.sleep(1)
	try:
		address, (latitude, longitude) = geolocator.geocode(courts[key]["FullAddress"])
	#print bars[key]["Address"]
		#print address, latitude, longitude
	except:
		print "Unable to find location for ", courts[key]["Name"]

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
        		"name": courts[key]["Name"],
        		"address": courts[key]["Address"],
        		"day": courts[key]["Day"],
        		"hours": courts[key]["Time"],
        		"specials": courts[key]["Details"]
      		}
    	}
    	resources.append(item)

geo={
	"type":"FeatureCollection",
	"features": resources
}


import json

with open("ohio_court_addresses.json","w") as jsonfile:
	jsonfile.write(json.dumps(geo, indent=4,sort_keys=True))
	
