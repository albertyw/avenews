"""
This script loads cities into the database
"""
import csv

import pycountry
import mysql

db = mysql.Mysql()

# Empty all the relevant tables so we can start from scratch
db.query("TRUNCATE TABLE City")
db.query("TRUNCATE TABLE CityAlias")

# Load cities
# Country,City,AccentCity,Region,Population,Latitude,Longitude
csv = csv.reader(open('worldcitiespop.txt','rb'))
for row in csv:
    print row[1]," in ",row[0]
    if row[4] <= 1000000 or row[4] == '':
        continue
    try:
        states = pycountry.subdivisions.get(country_code=row[0].upper())
    except:
        continue
    for state in states:
        if state.code[3:] == row[3]:
            break
    db.query("SELECT id FROM State WHERE stateName='"+db.escape_string(state.name)+"'")
    state_id = str(db.fetch()['id'])
    db.query("INSERT INTO City (cityName, stateId) VALUES('"+db.escape_string(row[1])+"','"+state_id+"')")
    
    
