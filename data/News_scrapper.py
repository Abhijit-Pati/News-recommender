# -*- coding: utf-8 -*-
"""
Created on Tue May 26 17:00:57 2020

@author: Dhruv Chuttad
"""
import requests

from bs4 import BeautifulSoup as bs
import nltk
import gensim.models as g
import nltk
# nltk.download()
import codecs
import csv
import re
import string
import pandas as pd 
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

TITLE_FILE= "Titles.txt"
OUTPUT_FILE = "Corpus.csv"
OUTPUT_URL = "Hindu_urls.txt"

def text_clean(text):
    n="".join([c for c in text if c not in string.punctuation])
    tokens = word_tokenize(n)
    tokens = [w.lower() for w in tokens]
    words = [word for word in tokens if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    porter = PorterStemmer()
    stemmed = [porter.stem(word) for word in words]
    text=' '.join(stemmed)
    return text

def get_article_details(url,date):
    try:
        data=requests.get(url)
        soup2= bs(data.content,'html5lib')
        m = re.search('article(.+?).ece', url)
        if m:
            id_no = m.group(1)
        ID='content-body-14269002-'+str(id_no)# the article content-body in the article source page has this attribute 
        article_content= soup2.find('div', id=ID).get_text()
        article_content=article_content.replace("\n","")   
        article_title=soup2.find('meta',attrs={"property":"og:title"}).get('content')
        with open(OUTPUT_FILE,'a') as f:
            ruleswriter = csv.writer(f)
            ruleswriter.writerow([article_content,url])
        with open(TITLE_FILE, 'a') as f:
            f.write(article_title+'\n')
            
    except:
        pass
    
    
########
#extracts the article urls from the archive page of one date
def get_urls(main_url,date):
    unwanted_categories=['/andhra-pradesh/','/karnataka/','/kerala','/tamil-nadu/','/telangana/','/cities/','/cartoon/'] #to remove regional articles and other non-text articles 
    try:
        raw_data = requests.get(main_url)
        soup1 = bs(raw_data.content, 'html5lib')
        category_list = soup1.find_all('ul', class_='archive-list')

        with open(OUTPUT_URL, 'a') as u:
            for cat in category_list:
                article_list = cat.find_all('a')
                for art in article_list:
                    article_link=art['href']
                    count=0
                    for word in unwanted_categories:
                        if word in article_link:
                            count= count+1
                    if count==0:
                        u.write(article_link + "\n")
                        get_article_details(article_link,date)

            
            
    except:
        pass


def main():
    
    year=2019
    
    
    for month in range(10,12):# for october,november and december
        if month%2==0:
            d=32
        else:
            d=15
        for day in range(1,d):
            date = str(day) + '/' + str(month) + '/' + str(year)
            main_url = 'https://www.thehindu.com/archive/web/' + str(year) + '/' + str(month) + '/' + str(day) + '/'
            get_urls(main_url,date)


if __name__ == '__main__':
    main()