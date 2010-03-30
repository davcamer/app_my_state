#!/opt/local/bin/python2.6
# encoding: utf-8
"""
test.py

Created by David Cameron on 2010-03-08.
Copyright (c) 2010 David Cameron. All rights reserved.
"""

from pyproj import Proj,transform

utm = Proj(proj="utm",ellps="WGS84",zone="55",south=True)

def ENtoLL84(easting,northing):
  # Returns (lat,long) tuple
  vlon_utm, vlat_utm = utm(easting,northing,inverse=True)
  return (vlat_utm,vlon_utm)

import csv
import string

ASSET_NUMBER_COLUMN = 0
DESCRIPTION_COLUMN = 1
CATEGORY_COLUMN = 2
MODEL_NUMBER_COLUMN = 3
MODEL_DESCRIPTION_COLUMN = 4
COLOUR_SCHEME_COLUMN = 5
EASTING_COLUMN = 6
NORTHING_COLUMN = 7

ASSET_NUMBER = "asset number"
DESCRIPTION = "description"
CATEGORY = "category"
MODEL_NUMBER = "model number"
MODEL_DESCRIPTION = "model description"
COLOUR_SCHEME = "colour scheme"
LATITUDE = "latitude"
LONGITUDE = "longitude"

def openCsvReader(filename):
  return csv.reader(open(filename))

def openCsvWriter(filename):
  return csv.writer(open(filename, 'w'))

def readData():
  reader = openCsvReader('furniture.csv')
  writer = openCsvWriter('furniture_with_gps.csv')
  
  headers = reader.next()
  writer.writerow(headers + ["latitude","longitude"])
  
  discarded = 0
  
  data = []
  
  for row in reader:
    easting, northing = row[EASTING_COLUMN], row[NORTHING_COLUMN]
    if easting == '' or northing == '':
      print "discarding: ", row
      discarded = discarded + 1
      continue
    lat, lon = ENtoLL84(easting, northing)
    writer.writerow(row + [lat, lon])
    
    data.append({CATEGORY: row[CATEGORY_COLUMN], LATITUDE: lat, LONGITUDE: lon})
  
  print "had to discard", discarded, "rows"
  return data

def writeRubyOutput(data):
  ruby = open('ruby_code.txt', 'w')
  lineTemplate = string.Template("              {:description=>'$category',:latitude=>'$latitude',:longitude=>'$longitude'},\n")

  for point in data:
    ruby.write(lineTemplate.substitute(point))
  ruby.close()

def groupByCategory(items):
  groups = {}
  for item in items:
    category = item[CATEGORY]
    if not category in groups:
      groups[category] = []
    groups[category].append(item)
  
  for key, value in groups.iteritems():
    print len(value), key
  
  return groups

def writeJavaScriptOutput(data):
  groups = groupByCategory(data)
  
  groupStartTemplate = string.Template("var $key = [\n")
  lineTemplate = string.Template("  {category: '$category', latitude: '$latitude', longitude: '$longitude'},\n")
  groupEnd = "];\n"
  
  js = open('data.js', 'w')
  for key, items in groups.iteritems():
    js.write(groupStartTemplate.substitute({"key": key.replace(' ', '_')}))
    for item in items:
      js.write(lineTemplate.substitute(item))
    js.write(groupEnd)
  js.close()

def main():
  data = readData()
  writeRubyOutput(data)
  writeJavaScriptOutput(data)

if __name__ == '__main__':
	main()

