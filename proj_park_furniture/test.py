#!/opt/local/bin/python2.6
# encoding: utf-8
"""
test.py

Created by David Cameron on 2010-03-08.
Copyright (c) 2010 David Cameron. All rights reserved.
"""

from pyproj import Proj,transform

utm = Proj(proj="utm",ellps="aust_SA",zone="55",south=True)

def ENtoLL84(easting,northing):
  # Returns (lat,long) tuple
  vlon_utm, vlat_utm = utm(easting,northing,inverse=True)
  return (vlat_utm,vlon_utm)

import csv
import string

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
  
  EASTING_COLUMN = 6
  NORTHING_COLUMN = 7
  DESCRIPTION_COLUMN = 1
  CATEGORY_COLUMN = 2
  
  DESCRIPTION = "description"
  LATITUDE = "latitude"
  LONGITUDE = "longitude"
  
  data = []
  
  for row in reader:
    easting, northing = row[EASTING_COLUMN], row[NORTHING_COLUMN]
    if easting == '' or northing == '':
      print "discarding: ", row
      discarded = discarded + 1
      continue
    lat, lon = ENtoLL84(easting, northing)
    writer.writerow(row + [lat, lon])
    
    data.append({DESCRIPTION: row[CATEGORY_COLUMN], LATITUDE: lat, LONGITUDE: lon})
  
  print "had to discard", discarded, "rows"
  return data

def writeRubyOutput(data):
  ruby = open('ruby_code.txt', 'w')
  lineTemplate = string.Template("              {:description=>'$description',:latitude=>'$latitude',:longitude=>'$longitude'},\n")

  for point in data:
    ruby.write(lineTemplate.substitute(point))

def main():
  data = readData()
  writeRubyOutput(data)

if __name__ == '__main__':
	main()

