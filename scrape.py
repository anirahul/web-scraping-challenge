from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import pandas as pd
#executable_path = {"executable_path": "chromedriver.exe"}
#browser = Browser("chrome", "/Users/anirbanmukherjee/Desktop/Anaconda/UNC-CHA-DATA-PT-09-2019-U-C/UNC-CHA-DATA-PT-09-2019-U-C-master/12-Web-Scraping-and-Document-Databases/Homework", headless=False)
#executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
#browser = Browser('chrome', **executable_path, headless=False)

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=True)

def scrape ():
  
    browser = init_browser()
    mars_data = {}


    filepath = os.path.join("News – NASA’s Mars Exploration Program.html")
    with open(filepath, encoding='utf-8') as file:
        html = file.read()
    soup = BeautifulSoup(html,'html.parser')
    soup.title
    soup.title.text
    results = soup.find_all('p')
    for result in results:
        print(result.text)

    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    print(featured_image_url)


    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)
    mars_weather_html = browser.html
    mars_weather_soup = BeautifulSoup(mars_weather_html, 'html.parser')
    tweets = mars_weather_soup.find('ol', class_='stream-items')
    mars_weather = tweets.find('p', class_="tweet-text").text
    print(mars_weather)


    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)
    mars_facts_html = browser.html
    mars_facts_soup = BeautifulSoup(mars_facts_html, 'html.parser')

    print(mars_facts_soup)

    column1 = mars_facts_soup.find_all('td', class_='column-1')
    column2 = mars_facts_soup.find_all('td', class_='column-2')

    facets = []
    values = []

    for row in column1:
        facet = row.text.strip()
        facets.append(facet)
    
    for row in column2:
        value = row.text.strip()
        values.append(value)
    
    mars_facts = pd.DataFrame({
        "Facet":facets,
        "Value":values
        })

    mars_facts_html = mars_facts.to_html(header=False, index=False)
    mars_facts

    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_dicts = []

    for i in range(1,9,2):
        hemi_dict = {}
    
        browser.visit(mars_hemisphere_url)
        hemispheres_html = browser.html
        hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')
        hemi_name_links = hemispheres_soup.find_all('a', class_='product-item')
        hemi_name = hemi_name_links[i].text.strip('Enhanced')
    
        detail_links = browser.find_by_css('a.product-item')
        detail_links[i].click()

        browser.find_link_by_text('Sample').first.click()
        browser.windows.current = browser.windows[-1]
        hemi_img_html = browser.html
        browser.windows.current = browser.windows[0]
        browser.windows[-1].close()
    
        hemi_img_soup = BeautifulSoup(hemi_img_html, 'html.parser')
        hemi_img_path = hemi_img_soup.find('img')['src']

        print(hemi_name)
        hemi_dict['title'] = hemi_name.strip()
    
        print(hemi_img_path)
        hemi_dict['img_url'] = hemi_img_path

        hemi_dicts.append(hemi_dict)

    mars_data["hemisphere_imgs"] = hemi_dicts

    browser.quit()

    return mars_data



