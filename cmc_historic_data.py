# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 13:59:56 2018

@author: CGall
"""

import requests
from bs4 import BeautifulSoup
import csv
import re

# Returns N number of urls from coinmarket cap by current ranking
def get_coin_urls(num):
    all_coins_url = 'https://coinmarketcap.com/all/views/all/'
    page = requests.get(all_coins_url)
    soup = BeautifulSoup(page.content, "html.parser" )
    
    url_list = []
    
    coins = soup.find_all(class_= 'currency-symbol')
    
    for url in coins:
        temp_str = str(url.find('a', href=re.compile(r"^/currencies/")))
        re.findall(r'"([^"]*)"', temp_str)
        if len(url_list) <= num:
            url_list.append(re.findall(r'"([^"]*)"', temp_str)[0])
        else:
            return url_list
    return url_list

# Gets all available historic data for a coin
def get_historic_data(coin_url):
    page = requests.get(coin_url)
    soup = BeautifulSoup(page.content, "html.parser" )
    table = soup.find('div', class_= 'table-responsive')
    
    title = soup.title.string.replace(' Historical Data | CoinMarketCap', '')
    

    print("Fetching historical data for " +  title)
    file_name = title + '.csv'
    myFile = open(file_name, 'w', newline='')
    with myFile:
        myFields = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Market Cap']
        writer = csv.DictWriter(myFile, fieldnames=myFields)
        #writer.writeheader()
    
        # Loop through table and extract elements
        for row in table.find_all('tr')[1:]: # 1 ignores headers
            date, openPrice, highPrice, lowPrice, closePrice, volume, marketCap = [td for td in row.stripped_strings]
            # Write output to new CSV file
            writer.writerow({    'Date' : date,
                                 'Open' : openPrice,
                                 'High' : highPrice,
                                 'Low' : lowPrice,
                                 'Close' : closePrice,
                                 'Volume' : volume,
                                 'Market Cap' : marketCap })




#### Main ####

# Get N number of coin urls from CMC   
coins = get_coin_urls(250)    

# Get historical data for coins and write to CSV file
for url in coins:
    coin_url = 'https://coinmarketcap.com' + url + 'historical-data/?start=20130428&end=20180415'
    get_historic_data(coin_url)
