#!/usr/bin/python2.6
# Load points from a csv file into a mongo database

import os
import sys

# If we're called as a CGI, exit now (security)
if os.getenv("HTTP_HOST"):
    sys.exit(1)

if len(sys.argv) < 3:
    print "loadmongo.py csvfile mapname"
    sys.exit(1)

import csv
import pymongo

mapname = sys.argv[2]

mconn = pymongo.Connection()
db = mconn.heatmaps.points

db.remove({"mapname": mapname})

for point in csv.reader(open(sys.argv[1], 'r')):

    # Parse and validate values.
    # ==========================

    uid, lat, lng = point
    try:
        lat = float(lat)
        lng = float(lng)
    except ValueError:
        print "bad line:", point
        continue

    point = { "lat": lat, "lng": lng, "mapname": mapname }
    db.insert(point)

db.create_index([("mapname", pymongo.ASCENDING), ("lat", pymongo.ASCENDING), ("lng", pymongo.ASCENDING)])
