"""
This script loads a csv files of cities from http://www.mobilgistix.com/Resources/GIS/Locations/average-latitude-longitude-countries.aspx
Includes the following fields:

    * ISO 3166 Country Code
    * Country Name
    * Latitude
    * Longitude 
    
e.g.:
"AF","Afghanistan",33,65

@author: Albert Wang
@date: 10/24/2010
"""

import csv
import mysql

mysql_connection = mysql.Mysql()

csv_file_location = "./average-latitude-longitude-countries.csv"
csv_file_handle = open(csv_file_location,'r')
csv_file_reader = csv.reader(csv_file_handle,delimiter=',')

# Read the city data line by line
for line in csv_file_reader:
    country_code = mysql_connection.escape_string(line[0])
    name = mysql_connection.escape_string(line[1])
    latitude = mysql_connection.escape_string(line[2])
    longitude = mysql_connection.escape_string(line[3])
    
    # Insert data into database
    query = "INSERT INTO countries (code, name, latitude, longitude)\
    VALUES('"+country_code+"', '"+name+"', '"+latitude+"', '"+longitude+"')"
    mysql_connection.query(query)
