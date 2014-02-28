#!/usr/bin/env python

import sys, argparse
import csv
import pprint
import pygeocoder
#from pygeocoder import Geocoder
from pygeolib import GeocoderError, GeocoderResult

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputfile')
parser.add_argument('-o', '--outputfile')
parser.add_argument('-s', default=0)
parser.add_argument('-t', action='store_true')
args = parser.parse_args()

# If reading header row, write new file. If not, append
if args.t:
    write_mode = 'wb'
else:
    write_mode = 'ab'

with open(args.inputfile, 'rb') as csvfile:
    with open(args.outputfile, write_mode) as csvoutput:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        writer = csv.writer(csvoutput, delimiter = ",", quotechar = '"')
        
        # If inputfile starts with header row, handle this and write updated header row to outputfile
        if args.t:
            fields = reader.next()
            fields_row = []
            for field in fields[0:11]:
                fields_row.append(field)
            fields_row.append('Premise_Latitude')
            fields_row.append('Premise_Longitude')
            for field in fields[11:]:
                fields_row.append(field)
            writer.writerow(fields_row)
            
        # Skip rows if option set
        if args.s > 0:
            for row in range(0, int(args.s)):
                reader.next()
            
        for row in reader:
            premise_address = row[8] + "\n" + row[9] + "\n" + row[10]
            print "Premise address:\n" + premise_address
            try:
                premise_coords = pygeocoder.Geocoder.geocode(premise_address)[0].coordinates
                print premise_coords
                print ''
            except GeocoderError, e:
                if e[0] == "ZERO_RESULTS":
                    print "Geocoding failed for this address\n"
                    premise_coords = ('', '')
                elif e[0] == "OVER_QUERY_LIMIT":
                    print e[0]
                    sys.exit(1)
                                
            new_row = []
            for field in row[0:11]:
                new_row.append(field)
            new_row.append(premise_coords[0])
            new_row.append(premise_coords[1])
            for field in row[11:]:
                new_row.append(field)
                
            writer.writerow(new_row)