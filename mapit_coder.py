#!/usr/bin/env python

import sys, argparse
from time import sleep
import csv
import pprint
import pygeocoder
import mapit_ew
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
            for field in fields[0:8]:
                fields_row.append(field)
            fields_row.append('Constituency')
            fields_row.append('Ward')
            fields_row.append('Output area')
            writer.writerow(fields_row)
            
        # Skip rows if option set
        if args.s > 0:
            for row in range(0, int(args.s)):
                reader.next()
                
        for row in reader:
            postcode = row[4]
            print "Postcode:\n" + postcode
            try:
                data = mapit_ew.getData(postcode)
                print data
                print ''
            except:
                print 'mapit error'
            new_row = []
            for field in row[0:8]:
                new_row.append(field)
            new_row.append(data['constituency']) if 'constituency' in data else new_row.append('')
            new_row.append(data['ward']) if 'ward' in data else new_row.append('')
            new_row.append(data['olf']) if 'olf' in data else new_row.append('')
                
            writer.writerow(new_row)
            #sleep(1.5)