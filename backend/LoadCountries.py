"""
This script loads countries into the database
"""
import csv

import pycountry
import mysql

db = mysql.Mysql()

# Empty all the relevant tables so we can start from scratch
db.query("TRUNCATE TABLE Country;")
db.query("TRUNCATE TABLE CountryAlias;")

# Load lat lon csv
reader = csv.reader(open('data/countryLatLon.txt','rb'))
latlon = {}
for row in reader:
    latlon[row[0]] = row[1:3]

# Load countries
countries = list(pycountry.countries)
for country in countries:
    country_name = db.escape_string(country.name, True)
    try:
        lat = str(float(latlon[str(country.alpha2)][0])*10**5)
        lon = str(float(latlon[str(country.alpha2)][1])*10**5)
    except:
        lat = '-1'
        lon = '-1'
    print country_name, lat, lon
    db.query("INSERT INTO Country (countryName, lat, lon) VALUES('"+country_name+"', '"+lat+"', '"+lon+"');")
    country_id = str(db.get_last_insert_id())
    db.query("INSERT INTO CountryAlias (countryId, aliasValue) VALUES('"+country_id+"','"+db.escape_string(country.alpha2)+"');")
    db.query("INSERT INTO CountryAlias (countryId, aliasValue) VALUES('"+country_id+"','"+db.escape_string(country.alpha3)+"');")
    if hasattr(country, 'official_name'):
        db.query("INSERT INTO CountryAlias (countryId, aliasValue) VALUES('"+country_id+"','"+db.escape_string(country.official_name, True)+"');")
