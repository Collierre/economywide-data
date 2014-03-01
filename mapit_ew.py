#!/usr/bin/env python

# Adapted from https://github.com/mikejamesthompson/mapit-requests

from datetime import datetime, time
import sys

import requests
import urllib
import json
import pprint

def getPostcode(postcode):

    # Form URL
    domain = "http://mapit.mysociety.org"
    path = "/postcode/"

    # Set request headers
    headers = {'User-Agent': 'Mike'}

    # Setup list to contain results
    areas = []

    url = domain + path + urllib.quote(postcode)

    # Fetch JSON
    response = requests.get(url, headers = headers)
    
    if(response.status_code != requests.codes.ok):
        sys.exit('Request failed')

    areas = [postcode, json.loads(response.text)]

    return areas

def getData(postcode):

    try:
        postcode = getPostcode(postcode)
        p = postcode[0]
        response = postcode[1]
        data = {}
    
        constituency_id = response['shortcuts']['WMC']
        data['constituency_id'] = constituency_id
        data['constituency_name'] = response['areas'][str(constituency_id)]['name'].encode('utf-8')
    
        ward_id = response['shortcuts']['ward']
        if type(ward_id) is not int:
            ward_id = ward_id['district']
        data['ward_id'] = ward_id
        data['ward_name'] = response['areas'][str(ward_id)]['name'].encode('utf-8')

        for area in response['areas']:
            areaType = response['areas'][area]['type']
            if(areaType=="OLF"):
                data['olf'] = response['areas'][area]['codes']['ons'].encode('utf-8')
            else:
                continue
    except:
        print postcode
        print('mapit error')
            
    return data
    
if __name__ == "main":
    print getData(sys.argv[1])
