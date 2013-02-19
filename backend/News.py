"""
This contains a lot of helper functions for avenews
"""
import mysql

"""
Convert the lat/lon into the units used for the database
"""

def zoom_conversion():
    return {'City':4, 'State':3, 'Country':2,  'International':1}
    
def get_db_latlon(lat_or_lon):
    return lat_or_lon * 10**5

def get_real_latlon(lat_or_lon):
    return lat_or_lon * 10**-5
    
def get_article(article_id):
    db = mysql.Mysql()
    article_id = db.escape_string(article_id)
    db.query("SELECT * FROM Article WHERE id='"+article_id+"';")
    article = db.fetch()
    return article

def get_country_article_list(country_name):
    db = mysql.Mysql()
    country_name = db.escape_string(country_name)
    db.query("SELECT id FROM Country WHERE countryName='"+country_name+"'")
    country = db.fetch()
    country_id = country['id']
    db.query("SELECT * FROM Article WHERE minZoom='2' AND locId='"+str(country_id)+"'")
    article_list = []
    while True:
        article = db.fetch()
        if article == {}:
            break
        article_list.append(article)
    return article_list
            
    
def get_country_news(lat1, lon1, lat2, lon2):
    # Make sure lat1, lon1 is less than lat2, lon2
    if lat1 > lat2:
        temp = lat1
        lat1 = lat2
        lat2 = temp
    if lon1 > lon2:
        temp = lon1
        lon1 = lon2
        lon2 = temp
    
    # Find all countries within the boundaries
    db = mysql.Mysql()
    db.query("SELECT * FROM Country WHERE lat != '-1' AND lon != '-1'")
    locations = []
    while True:
        country = db.fetch()
        if country == {}:
            break
        if not (country['lat'] > lat1 and country['lat'] < lat2 and
           country['lon'] > lon1 and country['lon'] < lon2):
            continue
        country_name = country['countryName']
        country_lat = get_real_latlon(country['lat'])
        country_lon = get_real_latlon(country['lon'])
        locations.append([country_name, country_lat, country_lon])
    return locations
    
def get_state_news(lat1, lon1, lat2, lon2):
    #TODO
    return []
    
def get_city_news(lat1, lon1, lat2, lon2):
    # TODO
    return []
