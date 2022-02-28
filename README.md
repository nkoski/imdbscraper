# imdbscraper
Python tool for scraping data from IMDB pages based on the movie id.

# Instructions:
The scraper.py script needs a list or a Pandas dataframe with IMDB IDs, which form a part of the IMDB url used by the scraper function. You can find datasets with IMDB IDs included in here, for instance: https://www.imdb.com/interfaces/.

You also need to download the Selenium webdriver on your machine. More information here: https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/

# Note
The IMDB pages are loaded dynamically with JavaScript. Therefore, scraping is quite slow (approx. 10–15 seconds per page), which can result in more than a week of scraping if you want to scrape the entire IMDB catalog. This script can probably be optimized in a lot of ways (I built it fairly quickly as part of a course project), but the fact remains that scraping dynamically-loaded web pages takes time. One simple solution for speeding this up is dividing the dataframe into batches and running them in parallel across different webdrivers or virtual machines.

