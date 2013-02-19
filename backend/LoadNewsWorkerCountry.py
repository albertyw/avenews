"""
This script interacts with feedzilla and downloads news about a country
"""
import sys
import json
import urllib
import urllib2

import mysql

subcategories_url = 'http://api.feedzilla.com/v1/categories/19/subcategories.json'
news_url_prefix = 'http://api.feedzilla.com/v1/categories/19/subcategories/'
news_url_suffix = '/articles.json'
uncategorized_news_url = 'http://api.feedzilla.com/v1/articles/search.json?q='

"""
Get two dictionaries of countries with feedzilla subcategories and countries without
"""
def get_country_categories(url):
    db = mysql.Mysql()
    country_categories = {}
    country_categories = {}
    json_response = urllib2.urlopen(url).read()
    subcategories = json.loads(json_response)
    for subcategory in subcategories:
        subcategory_name = subcategory['english_subcategory_name']
        db.query("SELECT id, countryName FROM Country")
        for country in db.iterate_rows():
            if country['countryName'] in subcategory_name:
                country_categories[country['id']] = subcategory['subcategory_id']
                break
    db.query("SELECT id, countryName FROM Country")
    uncategorized_countries = {}
    for country in db.iterate_rows():
        if country['id'] not in country_categories:
            uncategorized_countries[country['id']] = country['countryName']
    return country_categories, uncategorized_countries

"""
Download the news for a subcategory
"""
def load_subcategories_news(country_id, subcategory_id):
    db = mysql.Mysql()
    news_url = news_url_prefix+str(subcategory_id)+news_url_suffix
    json_response = urllib2.urlopen(news_url)
    news = json.loads(json_response.read())
    news = news['articles']
    for article in news:
        title = db.escape_string(article['title'])
        publish_date = db.escape_string(article['publish_date'])
        url = db.escape_string(article['url'])
        query = "INSERT INTO Article (title, minZoom, locId, publishDate, url) \
            VALUES('"+title+"', '2', '"+str(country_id)+"', '"+publish_date+"', '"+url+"')"
        db.query(query)

"""
Download news of a country without a subcategory
"""
def load_uncategorized_countries_news(country_id, country_name):
    db = mysql.Mysql()
    country_name = country_name.replace('.','')
    url = uncategorized_news_url+urllib.quote_plus(country_name)
    try:
        json_response = urllib2.urlopen(url).read()
    except Exception as e:
        print e
        print 'Counry Name: '+country_name
        print 'URL: '+url
    articles = json.loads(json_response)
    articles = articles['articles']
    for article in articles:
        title = db.escape_string(article['title'])
        publish_date = db.escape_string(article['publish_date'])
        url = db.escape_string(article['url'])
        query = "INSERT INTO Article (title, minZoom, locId, publishDate, url) \
            VALUES('"+title+"', '2', '"+str(country_id)+"', '"+publish_date+"', '"+url+"')"
        db.query(query)

if __name__ == '__main__':
    # Get the arguments
    part = int(sys.argv[1])
    parallelization = int(sys.argv[2])
    
    country_categories, uncategorized_countries = get_country_categories(subcategories_url)
    total = len(country_categories) + len(uncategorized_countries)
    start_id = part * (total / parallelization)+1
    end_id = (part + 1) * (total / parallelization)
    if part == parallelization - 1:
        end_id = total
    
    counter = 1
    for country_id, subcategory_id in country_categories.items():
        if start_id <= counter and counter <= end_id:
            print country_id
            load_subcategories_news(country_id, subcategory_id)
        counter += 1
    for country_id, country_name in uncategorized_countries.items():
        if start_id <= counter and counter <= end_id:
            print country_name
            load_uncategorized_countries_news(country_id, country_name)
        counter += 1
        
