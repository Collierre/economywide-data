#!/usr/bin/env python

import sys, argparse
from time import sleep
import csv
import pprint
import pygeocoder
import mapit_ew
import requests
import urllib
import json

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputfile')
parser.add_argument('-t', action='store_true')
args = parser.parse_args()

# If reading header row, write new file. If not, append
if args.t:
    write_mode = 'wb'
else:
    write_mode = 'ab'

with open(args.outputfile, write_mode) as csvoutput:
    writer = csv.writer(csvoutput, delimiter = ",", quotechar = '"')
    
    # If inputfile starts with header row, handle this and write updated header row to outputfile
    if args.t:
        fields_row = []
        fields_row.append('Constituency ID')
        fields_row.append('Constituency Name')
        writer.writerow(fields_row)
        
    # Form URL
    domain = "http://mapit.mysociety.org"
    path = "/areas/WMC"

    # Set request headers
    headers = {'User-Agent': 'Mike'}

    # Setup list to contain results
    wmcs = []

    url = domain + path

    # Fetch JSON
    response = requests.get(url, headers = headers)
    
    if(response.status_code != requests.codes.ok):
        sys.exit('Request failed')

    wmcs = json.loads(response.text)
    
    for wmc in wmcs:
        wmc_id = wmc
        wmc_name = wmcs[wmc]['name'].encode('utf-8')
        new_row = [wmc_id, wmc_name]
        writer.writerow(new_row)
