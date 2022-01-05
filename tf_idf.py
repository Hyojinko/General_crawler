from urllib import robotparser

import bs4
import json
import numpy as np
import requests
from urllib.parse import urlparse
import pandas as pd
from requests.models import MissingSchema
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
import trafilatura
import urllib
import queue
from collections import Counter
import threading
from pymongo import MongoClient
################################################################################################
########################   Reference   #########################################################
# https://codereview.stackexchange.com/questions/64757/crawl-multiple-pages-at-once

# Python3 program for a word frequency
# counter after crawling/scraping a web-page
import requests
from bs4 import BeautifulSoup
import operator
from collections import Counter


def start(url):

	# empty list to store the contents of
	# the website fetched from our web-crawler
	wordlist = []
	source_code = requests.get(url).text

	# BeautifulSoup object which will
	# ping the requested url for data
	soup = BeautifulSoup(source_code, 'html.parser')

	# Text in given web-page is stored under
	# the <div> tags with class <entry-content>
	# print(soup.findAll('a'))
	content_list=[]
	for each_text in soup.findAll('a'):
		content = each_text.text
		content = content.lower()
		content_list.append(content)

	clean_contents(content_list)

def clean_contents(content_list):
	clean_contents = []
	for cont in content_list:
		symbols = "!@#$%^&*()_-+={[}]|\;:\"<>?/., "

		for i in range(len(symbols)):
			cont = cont.replace(symbols[i], '')

			if len(cont) > 0:
				clean_contents.append(cont)

	get_tfidf(clean_contents)

def get_tfidf(clean_contents):
	tfidfv = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', ngram_range=(2,3)).fit(clean_contents)
	print(tfidfv.vocabulary_)



	''' words = content.lower().split()

		for each_word in words:
			wordlist.append(each_word)
		clean_wordlist(wordlist)

	clean_list = []
	for word in wordlist:
		symbols = "!@#$%^&*()_-+={[}]|\;:\"<>?/., "

		for i in range(len(symbols)):
			word = word.replace(symbols[i], '')

		if len(word) > 0:
			clean_list.append(word)
	create_dictionary(clean_list) '''
if __name__ == '__main__':

	df = pd.read_csv('links.csv')
	df.drop(df.columns[0],axis=1, inplace=True)
	#print(df)
	for domain, links in df.iteritems():
		for u in links:
			start(u)



