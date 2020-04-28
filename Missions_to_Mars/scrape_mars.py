#!/usr/bin/env python
# coding: utf-8


#!pip install twitterscraper
# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from twitterscraper import query_tweets
from twitterscraper import query_tweets_from_user as qtfu
import pandas as pd
from selenium import webdriver
import time

executable_path = {'executable_path': 'chromedriver.exe'}


# URL of page to be scraped
news_url = "https://mars.nasa.gov/news"


# Retrieve page with the requests module
response = requests.get(news_url)


# Create BeautifulSoup object; parse with 'html.parser'
soup = bs(response.text, 'html.parser')


# Examine the results, then determine element that contains sought info
#print(soup.prettify())


news_title = soup.find('div', class_="content_title").text
news_p = soup.find('div', class_='rollover_description_inner').text
#print (news_title)
#print (news_p)


# Scrape the space image
image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(image_url)
# Go to 'FULL IMAGE
browser.click_link_by_partial_text('FULL IMAGE')
browser.links.find_by_partial_text('FULL IMAGE')
time.sleep(5)
browser.click_link_by_partial_text('more info')
browser.links.find_by_partial_text('more info')
html = browser.html
image_soup = bs(html, 'html.parser')
feat_img_url = image_soup.find('figure', class_='lede').a['href']
featured_image_url = f'https://www.jpl.nasa.gov{feat_img_url}'
print(featured_image_url)


import requests
import shutil
response = requests.get(featured_image_url, stream=True)
with open('img.jpg', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
    
# Display the image with IPython.display
#from IPython.display import Image
#Image(url='img.jpg')


# Scraping the Twitter report on Mars
twitter_url = "https://twitter.com/MarsWxReport"
         

tweets = qtfu(user='MarsWxReport', limit=10)
tweets_df=pd.DataFrame(t.__dict__ for t in tweets)

#print (tweets_df)


mars_weather = tweets_df.loc[[0],"text"]
#print (mars_weather)

# Scaping the space facts website
mars_facts_url = "https://space-facts.com/mars"
tables = pd.read_html(mars_facts_url)
#print(tables)

#Find Mars Facts DataFrame in the lists of DataFrames
df = tables[0]
#Assign the columns
df.columns = ['Description', 'Value']
print(df)


#Save html to folder and show as html table string
mars_df = df.to_html(classes = 'table table-stripped')
#print(mars_df)


# Scraping Mars hemisphere name
astr_usgs_url = 'https://astrogeology.usgs.gov/'
hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(hemisphere_url)
hemisphere_html = browser.html
hemisphere_soup = bs(hemisphere_html, 'html.parser')
# Mars hemispheres data
all_mars_hemispheres = hemisphere_soup.find('div', class_='collapsible results')
mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')

hemisphere_image_urls = []
# Iterate through each hemisphere data
for i in mars_hemispheres:
    # Collect Title
    hemisphere = i.find('div', class_="description")
    title = hemisphere.h3.text
    #Collect image link by browsing to hemisphere page
    hemisphere_link = hemisphere.a["href"]
    #print (hemisphere_link)
    #browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(astr_usgs_url + hemisphere_link)
    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')
    image_link = image_soup.find('div', class_='downloads')
    image_url = image_link.find('li').a['href']
    # Create Dictionary to store title and url info
    image_dict = {}
    image_dict['title'] = title
    image_dict['img_url'] = image_url
    hemisphere_image_urls.append(image_dict)  
   

#print (hemisphere_image_urls) 





