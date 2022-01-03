from urllib import robotparser

import bs4
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

'''Function defining the web-crawler/core
spider, which will fetch information from
a given website, and push the contents to
the second function clean_wordlist()'''

word_count = {}

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
	for each_text in soup.findAll('a'):
		content = each_text.text

		# use split() to break the sentence into
		# words and convert them into lowercase
		words = content.lower().split()

		for each_word in words:
			wordlist.append(each_word)
		clean_wordlist(wordlist)
	#print(wordlist)

# Function removes any unwanted symbols


def clean_wordlist(wordlist):

	clean_list = []
	for word in wordlist:
		symbols = "!@#$%^&*()_-+={[}]|\;:\"<>?/., "

		for i in range(len(symbols)):
			word = word.replace(symbols[i], '')

		if len(word) > 0:
			clean_list.append(word)
	create_dictionary(clean_list)
	#print(clean_list)


# Creates a dictionary containing each word's
# count and top_20 occurring words


def create_dictionary(clean_list):

	for word in clean_list:
		if word in word_count:
			word_count[word] += 1
		else:
			word_count[word] = 1

	''' To get the count of each word in
		the crawled page -->

	# operator.itemgetter() takes one
	# parameter either 1(denotes keys)
	# or 0 (denotes corresponding values)

	for key, value in sorted(word_count.items(),
					key = operator.itemgetter(1)):
		print ("% s : % s " % (key, value))

	<-- '''

	# c = Counter(word_count)

	# returns the most occurring elements
	# top = c.most_common(1)
# 	handling_frequenat_tokens(word_count)
#
# def handling_frequenat_tokens(word_count):
# 	x = {key : value for key, value in word_count.items() if value<100}
# 	print(x)


# Driver code
if __name__ == '__main__':

	df = pd.read_csv('links.csv')
	df.drop(df.columns[0],axis=1, inplace=True)
	#print(df)
	for domain, links in df.iteritems():
		for u in links:
			start(u)

	word_count = {key: value for key, value in word_count.items() if value < 100}
	print(word_count)

