# import library
from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urlparse
from StoreToCSV import saveToCSV
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import csv
from langdetect import detect

from ReadCSV import *

HTTP= "http:"
COUNT = 0
# scraped_data_dict = {
#   "company": "",
#   "url": "",
#   "data": ""
# }
def increment():
    global COUNT
    COUNT = COUNT+1
    print(COUNT)

scraped_data_list=[]

def is_valid_url(url):
    val = URLValidator()
    try:
        val(url)
        #print(url)
        return True
    except:
        #print(url)
        return False

def is_http_or_https(url):
    return urlparse(url).scheme in {'http', 'https'}
    

#Scrape these linked urls
#output should have company's name, url, data
def web_scrap(link):
    if not (is_http_or_https(link)):
        link = HTTP + link

    #print(link)
    reqs=requests.get(link)
    contents=reqs.text
    soups = BeautifulSoup(contents, 'html.parser')
    #text = re.sub(r'[\ \n]{2,}', '', soups.get_text())
    #words = text.split()

    # Extract text from p tags
    p_tags = soups.find_all('p')
    p_texts = [p.text for p in p_tags]

    # Extract text from h1 tags
    h1_tags = soups.find_all('h1')
    h1_texts = [h1.text for h1 in h1_tags]

    # Extract text from span tags
    span_tags = soups.find_all('span')
    span_texts = [span.text for span in span_tags]

    # Combine the extracted texts
    text = p_texts + h1_texts + span_texts
    return text

    # Remove non-English words and gibberish
    # filtered_words = []
    # for word in words:
    #     try:
    #         language = detect(word)
    #         if language == 'en':
    #             filtered_words.append(word)
    #     except:
    #         pass

    # # Join the filtered words back into a text
    # filtered_text = ' '.join(filtered_words)
    # return  filtered_text

# Request to website and download HTML contents
def start_scrape(company_name, url):
    req=requests.get(url)
    content=req.text
    soup = BeautifulSoup(content, 'html.parser')
    links = {url}
    for link in soup.findAll('a'):
        currURL = link.get('href')
        #print("link is:", link.get('href'))
        #print('url is: ', url)
        if(is_valid_url(currURL)):
            links.add(currURL)

    soup = re.sub(r'[\ \n]{2,}', '', soup.get_text())
    thisdict = dict(Company_name = company_name, url = url, data = soup)
    scraped_data_list.append(thisdict)
    #print(links)
    try:
        for link in links:
            raw_data = web_scrap(link)
            thisdict = dict(Company_name = company_name, url = link, data = raw_data)
            scraped_data_list.append(thisdict)
            increment()
    except:
        print('invalid url found: ')

    return scraped_data_list    



def main():
    df = getCSVFile()
    #print(len(df))

    for index, row in df.iterrows():
        #print(row)
        data = start_scrape(company_name=row['Name'], url=row['URL'])
        saveToCSV(data=data)

    print("data scraoping completed...")

main()
#print(is_http_or_https("http://job-seeker.com"))
#print(re.sub(r'[\ \n]{2,}', '', soup.get_text()))