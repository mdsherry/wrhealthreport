import csv
import datetime
from collections import defaultdict
facilities_reader = csv.DictReader( open('Facilities_OpenData.csv', 'rb') )
facilities = {}
today = datetime.date.today()
for entry in facilities_reader:
	facilities[entry['FACILITYID']] = (entry["BUSINESS_NAME"], entry["ADDR"], entry["CITY"])
	opendate = datetime.datetime.strptime( entry["OPEN_DATE"], "%Y/%m/%d")



inspection_reader = csv.DictReader( open('Inspections_OpenData.csv', 'rb' ) )

inspections = defaultdict( list )
inspectionDetails = {}
for entry in inspection_reader:
	inspections[entry["FACILITYID"]].append( entry['INSPECTION_ID'] )
	inspectionDetails[entry['INSPECTION_ID']] = entry["INSPECTION_DATE"]


infraction_reader = csv.DictReader( open('Infractions_OpenData.csv', 'rb' ) )

infractions = defaultdict(list)

for entry in infraction_reader:
	inspectionId = entry['INSPECTION_ID']
	infractions[inspectionId].append( "{importance}: {description}".format( importance=entry["INFRACTION_TYPE"], description=entry["Description1"]))

def totalInfractions( facility ):
	return sum( len(infractions[inspect]) for inspect in inspections[facility]  )

faclist = facilities.keys()
faclist.sort( reverse=True, key=totalInfractions )

for facility in faclist:
	if facility not in facilities:
		print "Unknown facility ", facility
		continue
	print "{name} ({addr}, {city})".format( name=facilities[facility][0], addr=facilities[facility][1], city=facilities[facility][2])
	for inspection in sorted( inspections[facility], reverse=True, key=lambda x:inspectionDetails[x] ):
		print "\t", inspectionDetails[inspection]
		for infraction in infractions[inspection]:
			print "\t\t",infraction