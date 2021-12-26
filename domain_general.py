from bs4 import BeautifulSoup
from urllib import request
from urllib import robotparser

from bs4 import BeautifulSoup
import json
import numpy as np
import requests
from urllib.parse import urlparse
import pandas as pd
from requests.models import MissingSchema
import spacy
import trafilatura
import urllib
import queue
from collections import Counter
import threading


with open('crawled_urls.txt','r') as fd:
    urls = fd.read().splitlines()

    '''def get_link(url):
        for u in url:
            # Takes the website you typed and stores it in > site < variable

            # urllib.request.urlopen(url).read()
            make_request_to_site = urllib.request.urlopen(u).read()
            # Makes a request to the site that we stored in a var
            soup = BeautifulSoup(make_request_to_site, "html.parser")
            # We pass it through BeautifulSoup parser in this case html.parser
            # Next we make a loop to find all links in the site that we stored
            links = []
            link_df = pd.DataFrame()
            for link in soup.findAll('a'):
                links.append(link.get('href'))
                links = pd.Series(links, name=u)
            #link_df[urlparse(u).netloc] = links
        return links'''
    def get_link(url):
        make_request_to_site = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(make_request_to_site, "html.parser")
        links = []
        for link in soup.findAll('a'):
            links.append(link.get('href'))
        links = pd.Series(links, name=url)
        return urlparse(url).netloc, links

    df_link = pd.DataFrame()
    for u in urls:
        domain, links = get_link(u)
        df_link[domain] = links
    print(df_link)


#print(get_link(urls))