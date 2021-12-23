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

################################################################################################
########################   Reference   #########################################################
# https://codereview.stackexchange.com/questions/64757/crawl-multiple-pages-at-once


with open('crawled_urls.txt','r') as fd:
    urls = fd.read().splitlines()
    urls = pd.DataFrame([urlparse(u) for u in urls])

    q = queue.Queue()


    def get_page_links(page, crawled, to_crawl, next_tier, robot_set):
        rp = robotparser.RobotFileParser()
        links = []
        #uparse = urlparse.urlparse
        for link in page[1].find_all('a'):
            url = link.get('href')
            base_url = (urlparse(page[0]).scheme + '://' + urlparse(page[0]).netloc)
            if base_url not in robot_set:
                robot_set.add(base_url)
                rp.set_url(urlparse.urljoin(base_url, 'robots.txt'))
                rp.read()
            abs_url = urlparse.urljoin(base_url, url)
            if rp.can_fetch('*', abs_url):
                links.append(abs_url)
        links = set(links)
        next_tier.extend(links)
        to_crawl.update(links)
        to_crawl.remove(page[0])
        crawled.add(page[0])


    def get_page(url):
        try:
            return [url, BeautifulSoup(urllib.request.urlopen(url).read())]
        except:
            return [url, BeautifulSoup("")]


    def get_page_words(page, word_index):
        url = page[0]
        words = page[1].get_text()
        to_remove = '{}[]«#$%^&*._,1234567890+=<>/\()":;!?'
        bad_words = set(['http', 'www', 'com', 'https', 'gov', 'org', 'edu', 'imgs'])
        for i in to_remove:
            words = words.replace(i, ' ').lower()
        words = words.split()
        for word in words:
            if word in word_index:
                word_index[word].add(url)
            elif len(word) < 15 and word not in bad_words:
                word_index[word] = set([url])


    def crawl_web(url, maxdepth):
        depth = 0
        robot_set = set()
        crawled = set()
        to_crawl = set([url])
        word_index = {}
        tier_list = [[url]]
        while depth < maxdepth:
            next_tier = []
            for url in tier_list[depth]:
                page = get_page(url)
                t1 = threading.Thread(target=get_page_links, args=(page, crawled, to_crawl, next_tier, robot_set))
                t2 = threading.Thread(target=get_page_words, args=(page, word_index))
                t1.start()
                t2.start()
                t1.join()
                t2.join()
            tier_list.append(next_tier)
            depth += 1
        return crawled, to_crawl, word_index, tier_list


    def search_engine(target_string, word_index):
        targets = list(set(target_string.split()))
        result = []
        for word in targets:
            if word in word_index:
                result += word_index[word]
        ans = Counter(result).most_common(3)
        return ans

    for index, u in urls.iterrows():
        root = u['scheme']+'://'+u['netloc']
        result = crawl_web(root, 2)
        word_index = result[2]
        print(result[0])
        print(search_engine('starting about', word_index))