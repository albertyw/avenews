"""
This script loads states into the database
"""
import csv

import pycountry
import mysql

db = mysql.Mysql()

# Empty all the relevant tables so we can start from scratch
db.query("TRUNCATE TABLE State;")
db.query("TRUNCATE TABLE StateAlias;")

# Load states
countries = list(pycountry.countries)
for country in countries:
    country_name = db.escape_string(country.name, True)
    print country_name
    db.query("SELECT id FROM Country WHERE countryName='"+country_name+"';")
    country_id = str(db.fetch()['id'])
    try:
        states = pycountry.subdivisions.get(country_code=country.alpha2)
    except:
        states = []
    for state in states:
        state_name = db.escape_string(state.name, True)
        db.query("INSERT INTO State (stateName, countryId) VALUES('"+state_name+"','"+country_id+"');")



