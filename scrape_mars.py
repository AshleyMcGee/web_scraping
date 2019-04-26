#import dependencies

from splinter import Browser
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time


def scrape():

    #Connect chromedriver with splinter's Browser object.
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    #create dictionary off of every single variable, make each variable a key
    #be careful not to accidentally change how things work by changing variable names
    mars = {}

    #Use chromedriver to open the NASA website
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #Latest article title.
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #Key for mars' article title
    article_title = soup.find_all("div", class_="content_title")[0].text.strip()
    mars['article_title'] = article_title

    #Latest article paragraph.
    paragraph = soup.find('div', class_='article_teaser_body').text.strip()
    mars['artile_text'] = paragraph

    #Reinitialize the url for every click-through
    #On main page, click thorugh full image button
    browser.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    html2 = browser.html
    soup2 = BeautifulSoup(html2, "html.parser")
    

    browser.click_link_by_partial_text("FULL IMAGE")

    #On carosel page, click through more info
    html3 = browser.html
    soup3 = BeautifulSoup(html3, "html.parser")
    time.sleep(3)
    browser.click_link_by_text("more info     ")

    #Full-sized image link
    html4 = browser.html
    soup4 = BeautifulSoup(html4, "html.parser")
    base_url_featured = "https://www.jpl.nasa.gov"

    for i in soup4.find_all('figure'):
        featured_image = base_url_featured + (i.a['href'])

    mars['featured_image'] = featured_image

    #Connect to Mars Weather's Twitter account
    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)

    #The tweet
    html5 = browser.html
    soup5 = BeautifulSoup(html5, "html.parser")

    mars_weather = soup5.find("ol", class_="stream-items js-navigable-stream")\
                .find_all("li", class_="js-stream-item stream-item stream-item ")[0]\
                .find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.strip()

    mars['todays_weather'] = mars_weather

    #Connect to the Mars Facts web pages
    url4 = "https://space-facts.com/mars/"

    #Use pandas to scrape the table of facts about Mars.
    table = pd.read_html(url4)

    #Mars is cool. This table says so.
    df = table[0]
    df.columns = ["Planet Profile", "Stats"]

    #Pandas turns the table into html for later use
    table_data_html = df.to_html()

    mars['mars_stats'] = table_data_html

    #Connect to the USGS website
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)

    #Cook the soup
    html6 = browser.html
    soup6 = BeautifulSoup(html6, "html.parser")

    link_titles = []

    for el in soup6.findAll("div", class_="description"):
        link_titles.append(el.find("h3").text.strip())

    links = browser.find_by_css('a.product-item h3')

    #Connect to the USGS website again
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)

    mars_hemispheres = []
    base_url = "https://astrogeology.usgs.gov"

    for i in range(len(links)):
        #empty dictionary
        hemispheres = {}

        #click to the hemisphere
        browser.find_by_css('a.product-item h3')[i].click()

        #reinitialize browser and cook the soup
        html7 = browser.html
        soup7 = BeautifulSoup(html7, "html.parser")

        #get the image url
        full_url = base_url + soup7.find('img', class_="wide-image")['src']

        #fill dictionary
        hemispheres['title'] = link_titles[i]
        hemispheres['image_url'] = full_url

        #push to mars_hemispheres list
        mars_hemispheres.append(hemispheres)

        #click back
        browser.back()

    mars['hemispheric_data'] = mars_hemispheres

    return mars
