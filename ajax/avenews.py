import json
import os
import sys
path = os.path.dirname(os.path.realpath(__file__))+'/../backend/'
sys.path.append(path)

import News
import mysql
from flask import Flask, abort
app = Flask(__name__)

zoom_to_depth = {'4':'City', '3':'State', '2':'Country', '1':'International'}
zooms = ['1','2','3','4']
max_state_lat_lon_difference = News.get_db_latlon(20)
max_city_lat_lon_difference = News.get_db_latlon(5)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/article/<article_id>")
def get_article(article_id):
    article = News.get_article(article_id)
    return json.dumps(article, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/articlelist/<country_name>")
def get_article_list(country_name):
    article_list = News.get_country_article_list(country_name)
    return json.dumps(article_list, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/latlon/country/<lat1>/<lon1>/<lat2>/<lon2>")
def latlon(lat1, lon1, lat2, lon2):
    lat1 = int(News.get_db_latlon(float(lat1)))
    lon1 = int(News.get_db_latlon(float(lon1)))
    lat2 = int(News.get_db_latlon(float(lat2)))
    lon2 = int(News.get_db_latlon(float(lon2)))
    news = News.get_country_news(lat1, lon1, lat2, lon2)
    return json.dumps(news, sort_keys=True, indent=4, separators=(',', ': '))

@app.route("/<zoom>/<query>")
def query(zoom, query):
    db = mysql.Mysql()
    if zoom not in zooms:
        abort(404)
    zoom = db.escape_string(zoom)
    query = db.escape_string(query)
    depth = zoom_to_depth[zoom]
    
    # Get the location_ids
    db.query("SELECT id FROM "+depth+" WHERE "+depth.lower()+"Name = '"+query+"'")
    location_id = db.fetch()
    location_id = str(location_id['id'])
    
    # Get the articles
    db.query("SELECT id, title, minZoom, publishDate, url FROM Article WHERE \
        minZoom='"+zoom+"' AND locId='"+location_id+"'")
    articles = []
    while True:
        article = db.fetch()
        if article == {}:
            break
        articles.append(article)
    return json.dumps(articles)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
