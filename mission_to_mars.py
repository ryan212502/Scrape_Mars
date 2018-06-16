
import pymongo
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_db
collection = db.marsnews
news_url = 'https://mars.nasa.gov/news/'
response = requests.get(news_url)
soup = BeautifulSoup(response.text, 'lxml')

browser = Browser('chrome', headless=False)
news_url = 'https://mars.nasa.gov/news/'
browser.visit(news_url)
html =  browser.html
news_soup = BeautifulSoup(html, 'html.parser')

result = news_soup.find('div', class_='content_title')
news_title= result.next_element.get_text()
result1=news_soup.find('div', class_='article_teaser_body')
news_p = result1.get_text()
#result2 = news_soup.find('div', class_='release_date')
#news_date = result2.get_text()

#print(news_date)
print(news_title)
print(news_p)

browser = Browser('chrome', headless=False)
image_url  = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(image_url )
html = browser.html
image_soup = BeautifulSoup(html, 'html.parser')

image = image_soup.find('div', class_='carousel_items')
image_url = image.article['style']
url = image_url.split('/s')[-1].split('.')[0]
featured_image_url= 'https://www.jpl.nasa.gov' +'/s'+ url + '.jpg'
print(featured_image_url )

browser = Browser('chrome', headless=False)
weather_url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(weather_url)

html = browser.html
weather_soup = BeautifulSoup(html, 'html.parser')

weather = weather_soup.find('div', class_='js-tweet-text-container')

mars_weather= weather.p.text.lstrip()
print(mars_weather)

facts_url = 'http://space-facts.com/mars/'

fact_table = pd.read_html(facts_url)
fact_table

df = fact_table[0]
df.columns = ['Mars', 'Value']
df

html_table = df.to_html()
df.to_html('table.html')

mars_facts=df.to_dict('records')
mars_facts

tem=list(mars_facts[0].values())
tem

Table = []
for i in range(0, len(mars_facts)):
    temp=list(mars_facts[i].values())
    Table.append(temp)

print(Table)

for i in Table:
     print (i)

hemisphere_image = []

browser = Browser('chrome', headless=False)
hemisphere_urls = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
       'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
       'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced',
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced']
for url in hemisphere_urls:
    browser.visit(url)
    html = browser.html
    hemisphere_soup = BeautifulSoup(html, 'html.parser')

    dictionary = {}
    hemipshere_title = hemisphere_soup.find('div', class_='content')
    dictionary["title"] = hemipshere_title.h2.text.lstrip()
    
    hemipshere_download=hemisphere_soup.find('div', class_='downloads')
    image=hemipshere_download.find('li')
    dictionary["image_url"] = image.find('a')['href']
    print(dictionary)
    hemisphere_image.append(dictionary)

