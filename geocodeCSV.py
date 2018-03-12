import geocoder
import csv

from importlib import reload
import incident
reload(incident)
from incident import Incident
import json

incidents = []
cache = []
cachedLocations = []

def updateCSV():
    load()
    geocodeCSV()
    dump_csv_raw(incidents, "harvard_crime_incidents.csv")
    dump_csv_raw(cache, "incident_cache.csv")

def load():
    with open("incident_cache.csv", "r") as f:
        freader = csv.DictReader(f)
        for row in freader:
            cache.append(row)

    for row in cache:
        #cachedLocations = incident["location"]
        cachedLocations.append(row["street_address"])

    with open("harvard_crime_incidents.csv", "r") as f:
            freader = csv.DictReader(f)
            for row in freader:
                incidents.append(row)

def geocodeCSV():
    for row in incidents:
        #only need to geocode new ones
        if row["latitude"] == "":
            if row["street_address"] in cachedLocations:
                length = len(cachedLocations)
                for i in range(0, length):
                    try:
                        if cachedLocations[i] == row["street_address"]:
                            break
                        row["latitude"] = cache[i]["latitude"]
                        row["longitude"] = cache[i]["longitude"]
                    except ValueError:
                        x = 2
            else:
                geocode(row)

def geocode(row):
   # HUPD only covers stuff in Massachusetts so manually adding the state here
    fullAddress = row["location"] + ", " + row["street_address"] + ", " + row["city"] + ", " + "MA"
    geocoded = geocoder.google(fullAddress)
    if geocoded.latlng != None:
        # use cached copy if available
        print(fullAddress)
        print(geocoded.latlng)
    else:
        shortAddress = row["street_address"] + ", " + row["city"] + ", " + "MA"
        geocoded = geocoder.google(shortAddress)
        print(fullAddress)
        print(geocoded.latlng)
        if(geocoded.latlng == None):
            # PROBLEM: sometimes the request just doesn't work so we'll get None,
            # even if the address is actually geocode-able!
            # We should throttle this
            geocoded.latlng = [0,0]

    row["latitude"] = geocoded.latlng[0]
    row["longitude"] = geocoded.latlng[1]

    #add to cache
    cache.append(row)
    cachedLocations.append(row["street_address"])

def dump_csv_raw(incidents, fname):
    """
    Dumps a list of raw incident rows to CSV.
    """
    with open(fname, 'w') as csvfile:
        fieldnames = Incident.CSV_FIELDS
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for row in incidents:
            try:
                writer.writerow(row)
            except ValueError:
                x = 2
