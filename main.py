"""
    victoria_restaurants.py

    Grab a list of Victoria, BC restuarants from the City of Victoria Open Data Portal

    Reads data from disk if available, otherwise goes to the City of Victoria
    Open Data Portal and grabs a fresh copy.
"""

import csv
import os
import json

import requests

FILENAME = 'businesses.csv'
CITY_OF_VICTORIA_DATA = 'http://vicmap.victoria.ca/_BusData/AllBusinessLicences_LatLong.csv'

if os.path.exists('businesses.csv'):
    data = open(FILENAME, 'r').read()
else:
    response = requests.get(CITY_OF_VICTORIA_DATA)
    if response.status_code == 200:
        data = response.text
        open(FILENAME, 'w').write(data)

records = list(csv.reader(data.splitlines()))
columns = [n.strip().lower() for n in records[0]]
businesses = records[1:]

name_pos = columns.index('trade_name')
address_pos = columns.index('civic_address')
category_pos = columns.index('category')

restaurants = []
for business in businesses:
    category = business[category_pos].lower()
    in_town = (business[address_pos] != 'BUSINESS - OUT OF TOWN')
    if in_town and 'restaurant' in category:
        name = business[name_pos].title()
        address = business[address_pos]

        # a hack to fix data formatting
        address = address.replace('VICTORIA BC', ', VICTORIA BC')

        restaurants.append({
            'name': name,
            'address': address,
        })
restaurants = {n: r for n,r in enumerate(restaurants)}

if os.path.exists('restaurants.json'):
    newData = open(FILENAME, 'r').read()
else:
    open('restaurants.json', 'w').write(json.dumps(restaurants, indent=2))

