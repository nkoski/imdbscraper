from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import re
import json
import pandas as pd
from google.cloud import bigquery
import os
import numpy as np

# change this to your chromedriver location
CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'

# webdriver config to speed up script
option = webdriver.ChromeOptions()

# uncomment these if you want to run the webdriver in headless mode
# option.add_argument("--headless")
# option.add_argument("--disable-extensions")
# option.add_argument("--disable-gpu")
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=option)



# xpath information for the data that we want to scrape from each page
revenue_xpath = "//*[ text() = 'Gross worldwide' ]/following-sibling::div"
opening_weekend_xpath = "//*[contains(text(),'Opening weekend')]/following-sibling::div"
budget_xpath = "//*[ text() = 'Budget' ]/following-sibling::div"
country_xpath1 = "//*[ text() = 'Countries of origin' ]/following-sibling::div/ul"
country_xpath2 = "//*[ text() = 'Country of origin' ]/following-sibling::div/ul"
awards_nominations_xpath = '//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[1]/div/ul/li'

# scrapes the data from url with movie id given as argument
def scrape(movieid):
    
    url = 'https://www.imdb.com/title/' + movieid

    driver.get(url)

    # parse data from xpath elements. Errors result in N/A values (a huge part of the movies do not contain this information which will throw an error)
    try:
        revenue = [my_elem.text for my_elem in WebDriverWait(driver, 5).until(expected_conditions.visibility_of_all_elements_located((By.XPATH, revenue_xpath)))][0]
    except:
        revenue = 'N/A'
    try:
        opening_weekend = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(expected_conditions.visibility_of_all_elements_located((By.XPATH, opening_weekend_xpath)))][0]
        match = re.findall(r'<span class="ipc-metadata-list-item__list-content-item">.+</span>', opening_weekend)[0]
        opening_weekend = match[match.index('>') + 1: match.index('</s')]
    except:
        opening_weekend = 'N/A'
    try:
        budget = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(expected_conditions.visibility_of_all_elements_located((By.XPATH, budget_xpath)))][0]
        match = re.findall(r'<span class="ipc-metadata-list-item__list-content-item">.+?</span>', budget)[0]
        budget = match[match.index('>') + 1: match.index('</s')]
    except:
        budget = 'N/A'
    try:
        countrylist = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(expected_conditions.visibility_of_all_elements_located((By.XPATH, country_xpath1)))][0]
        match = re.findall(r'<a class=.+?</a>', countrylist)
        countrylist = [x[x.index('>') + 1: x.index('</a')] for x in match]
        country = ", ".join(countrylist)
    except:
        try:
            countrylist = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(expected_conditions.visibility_of_all_elements_located((By.XPATH, country_xpath2)))][0]
            match = re.findall(r'<a class=.+?</a>', countrylist)
            countrylist = [x[x.index('>') + 1: x.index('</a')] for x in match]
            country = ", ".join(countrylist)
        except:
            country = 'N/A'
    try:
        awards = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(expected_conditions.visibility_of_all_elements_located((By.XPATH, awards_nominations_xpath)))][0]
        match = re.findall(r'<span class=.+?nominati.+?</span>', awards)[0]
        awards = match[match.index(">") + 1:match.index(" wins")]
    except:
        awards = 'N/A'
    return {"imdb_id": movieid, "revenue": revenue, "opening_weekend": opening_weekend, "budget": budget, "country": country, "awards": awards}



# some movie-ids for testing:
movieids = ['tt0111161', 'tt10896634', 'tt0311519', 'tt1371111']

# you can use a list like above or a Pandas dataframe



# loop through the movies list/dataframe and call the scraper function

filepath = '/home/user1/moviedata.json' # you need to create an empty json file somewhere and change this path
counter = 1
total = len(movieids) # size of the list/dataframe
for movieid in movieids: # here you can also use a Pandas dataframe, e.g. "for movieid in df["imdb_id"]"
    dict = scrape(movieid) # returns a dictionary with the scraped values for this movie
    with open(filepath, 'a') as outfile:
        json.dump(dict, outfile)
        outfile.write('\n')
    print("{} out of {} processed".format(counter, total))
    counter += 1
outfile.close()

# Prints a message when finished
print('All done! JSON file at {}'.format(filepath))

