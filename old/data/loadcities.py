"""
This script loads a csv files of cities from http://www.maxmind.com/app/worldcities
Includes the following fields:

    * Country Code
    * ASCII City Name
    * City Name
    * State/Region
    * Population
    * Latitude
    * Longitude 
    
Country Code 	char(2) 	ISO 3166 Country Code,
ASCII City Name 	varchar(100) 	Name of city or town in ASCII encoding
City Name 	varchar(255) 	Name of city or town in ISO-8859-1 encoding. A list of cities contained in GeoIP City is available.
State/Region 	char(2) 	For US, ISO-3166-2 code for the state/province name. Outside of the US, FIPS 10-4 code
Population 	unsigned int 	Population of city (available for over 33,000 major cities only)
Latitude 	numeric (float) 	Latitude of city where IP is located
Longitude 	numeric (float) 	Longitude of city where IP is located

e.g.:
ad,sornas,Sornas,05,,42.5666667,1.5333333

@author: Albert Wang
@date: 10/24/2010
"""

import csv
import mysql

mysql_connection = mysql.Mysql()

csv_file_location = "./worldcitiespop.txt"
csv_file_handle = open(csv_file_location,'r')
csv_file_reader = csv.reader(csv_file_handle,delimiter=',')

# Read the city data line by line
for line in csv_file_reader:
    country_code = mysql_connection.escape_string(line[0])
    ascii_name = mysql_connection.escape_string(line[1])
    # name = mysql_connection.escape_string(line[2])
    state = mysql_connection.escape_string(line[3])
    population = mysql_connection.escape_string(line[4])
    latitude = mysql_connection.escape_string(line[5])
    longitude = mysql_connection.escape_string(line[6])
    
    # Insert data into database
    query = "INSERT INTO cities (country_code, ascii_name, state, population, latitude, longitude)\
    VALUES('"+country_code+"', '"+ascii_name+"', '"+state+"', '"+population+"', '"+latitude+"', '"+longitude+"')"
    mysql_connection.query(query)
