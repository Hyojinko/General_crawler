import pandas as pd
from krwordrank.word import KRWordRank
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from konlpy.tag import Kkma
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
from krwordrank.hangle import normalize
import numpy as np

################################################################################################
########################   Reference   #########################################################
# https://codereview.stackexchange.com/questions/64757/crawl-multiple-pages-at-once

# Python3 program for a word frequency
# counter after crawling/scraping a web-page


cleaned_contents = []


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
	for cont in content_list:
		symbols = "!@#$%^&*()_-+={[}]|\;:\"<>?/., "

		for i in range(len(symbols)):
			cont = cont.replace(symbols[i], '')

			if len(cont) > 0:
				cleaned_contents.append(cont)
	#wordRank(clean_contents)
	return cleaned_contents


'''def get_tfidf(clean_contents):
	tfidfv = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', ngram_range=(2,3)).fit(clean_contents)
	print(tfidfv.vocabulary_)'''

'''def wordRank(clean_contents):
	clean_contents = [normalize(text, english=False, number=False) for text in clean_contents]
	extractor = KRWordRank(min_count=2, max_length=10, verbose=True)
	beta = 0.85
	max_iter = 10
	keywords, rank, graph = extractor.extract(clean_contents, beta, max_iter)
	for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:10]:
		print('%8s:\t%.4f'%(word,r))'''



if __name__ == '__main__':

	df = pd.read_csv('links.csv')
	df.drop(df.columns[0],axis=1, inplace=True)
	#print(df)
	for domain, links in df.iteritems():
		for u in links:
			start(u)
	contents = cleaned_contents
	contents = [normalize(text, english=False, number=False) for text in contents]
	extractor = KRWordRank(min_count=2, max_length=10, verbose=True)
	beta = 0.85
	max_iter = 10
	keywords, rank, graph = extractor.extract(contents, beta, max_iter)
	for word, r in sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:10]:
		print('%8s:\t%.4f' % (word, r))
