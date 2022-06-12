# Libraries Used

import requests
from bs4 import BeautifulSoup
import pandas as pd
from cryptocmd import CmcScraper
import matplotlib.pyplot as plt
import seaborn as sns
import math

def get_topic_page(topic,yyyymmdd):
    
    topic_url = topic+'/historical/'+str(yyyymmdd) ##URL used
    response = requests.get(topic_url)
    
    with open('cryptooo.html','w') as f:
        f.write(response.text)
    
    if not response.ok:
        print('status:', response.status_code)
        raise Exception('Failed to fetch webpage')
     
    return BeautifulSoup(response.text,features="lxml")


def split_it(td_tags,symbol):
    if len(symbol) == 3:
        return td_tags[1].text[3:]
    else:
        return td_tags[1].text[4:]


def get_crypto_data(tr_tag):
    
    td_tags = tr_tag.find_all('td')  
    symbol =td_tags[2].text
    name = split_it(td_tags,symbol)       
    rank = td_tags[0].text
    price = td_tags[4].text
    market_cap = td_tags[6].text
    return {'Name:': name,
            'Symbol:':symbol,
            'Rank:': rank,
            'Price:': price,
            'Marketcap:': market_cap}


## get dataframe of all 20 crypto 

def flow_it():
    tr_tags = doc.tbody.find_all('tr')
    
    # Retrives top 20 crypto from any historical data given the date
    top_20_crypto = [get_crypto_data(tr_tags[i]) for i in range(20)]
    new_20 = pd.DataFrame(top_20_crypto)
    return new_20


# instance for cmcscraper to get the data 
#start = dd-mm-yyyy
#end = dd-mm-yyyy
def createit(new_20,start,end):
    
    new_list = []
    for i in range(18):
       
        new_list.append(CmcScraper((new_20.loc[i,'Symbol:']),start,end).get_dataframe().drop(['Market Cap','Volume','Low','High'],axis = 1))
        
    return new_list  


if __name__ == "__main__":

	topic='https://coinmarketcap.com'   ## URL to request to scrape
	doc = get_topic_page(topic,20200101)  ## takes in two argument, URL and the historical date to scrap
	data = flow_it()
	Symbol = list(data['Symbol:'])  #get a list of the top 20 coins symbols
	all_20_dataframe =createit(data,'01-01-2020','03-01-2022')
	Crypto_final_list = pd.concat(all_20_dataframe,keys = Symbol,axis = 1)
	Crypto_final_list.columns.names = ['Crypto','Crypto_info']
	Crypto_final_list

