"""
This script interacts with feedzilla and downloads news for blocks of states or cities
"""
import sys
import json
import urllib
import urllib2

import mysql

db = mysql.Mysql()
depth_to_zoom = {'City':4, 'State':3, 'Country':2,  'International':1}

# Get the arguments
depth = sys.argv[1]
start_id = str(sys.argv[2])
limit = str(sys.argv[3])
min_zoom = str(depth_to_zoom[depth])

# Read news
locations = {}
db.query("SELECT id, "+depth.lower()+"Name FROM "+depth+" WHERE id>="+start_id+" LIMIT "+limit)
while True:
    location = db.fetch()
    if location == {}:
        break
    locations[location[depth.lower()+'Name']] = str(int(location['id']))
    
for location_name, location_id in locations.iteritems():
    location_name = urllib.quote(location_name)
    url = 'http://api.feedzilla.com/v1/articles/search.json?q='+location_name
    print min_zoom+'   '+start_id+'   '+url
    try:
        json_response = urllib2.urlopen(url).read()
        articles = json.loads(json_response)
    except:
        continue
    articles = articles['articles']
    for article in articles:
        title = db.escape_string(article['title'])
        publish_date = db.escape_string(article['publish_date'])
        url = db.escape_string(article['url'])
        query = "INSERT INTO Article (title, minZoom, locId, publishDate, url) \
            VALUES('"+title+"', '"+min_zoom+"', '"+location_id+"', '"+publish_date+"', '"+url+"')"
        db.query(query)
