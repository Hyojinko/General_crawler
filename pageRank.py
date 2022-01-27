import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
from konlpy.tag import Kkma, Okt
from konlpy.tag import Twitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np



class SentenceTokenizer(object):

    def get_contents(self,url):
        source_code = requests.get(url).text
        wordlist=[]
        # BeautifulSoup object which will
        # ping the requested url for data
        soup = BeautifulSoup(source_code, 'html.parser')

        # Text in given web-page is stored under
        # the <div> tags with class <entry-content>
        # print(soup.findAll('a'))
        for each_text in soup.findAll('a'):
            content = each_text.text
            content = content.lower()
            words=Okt().nouns(content)
            for each_word in words:
                wordlist.append(each_word)
        return wordlist
    def get_nouns(self,wordlist ):
        clean_list=[]
        for word in wordlist:
            word = re.sub('[a-zA-z]', '', word)
            symbols = "은는이가을를이다다의에에서로와과!@#$%^&*()_-+={[}]|\;:\"<>?/., "
            for i in range(len(symbols)):
                word = word.replace(symbols[i], '')
            if len(word) > 0:
                clean_list.append(word)
        nouns = []
        for word in clean_list:

            if word != '':
                '''nouns.append(' '.join([nouns for noun in Okt.nouns(sentence)
                             if len(noun) > 1]))'''
                nouns.append(' '.join([noun for noun in word if len(noun)>1]))
        return nouns

class GraphMatrix(object):
    def __init__(self):
        self.tfid = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b",
       stop_words=None)
        self.cnt = CountVectorizer(stop_words=None)
        self.graph_sentence = []

    def build_sent_graph(self, sentence):
        tfid_mat = self.tfid.fit_transform(sentence).toarray()
        self.graph_sentence = np.dot(tfid_mat, tfid_mat.T)
        return self.graph_sentence


    def build_words_graph(self, sentence):
        cnt_mat = normalize(self.cnt.fit_transform(sentence).toarray().astype(float),axis=0)
        vocab = self.cnt.vocabulary_
        return np.dot(cnt_mat.T, cnt_mat), {vocab[word]:word for word in vocab}

class Rank(object):
    def get_ranks(self, graph, d=0.85):
        A = graph
        matrix_size=A.shape[0]
        for id in range(matrix_size):
            A[id,id] = 0
            link_sum = np.sum(A[:,id])
            if link_sum != 0:
                A[:, id] /= link_sum
            A[:,id] *= -d
            A[id, id] = 1
        B = (1-d) * np.ones((matrix_size,1))
        ranks = np.linalg.solve(A,B)
        return {idx: r[0] for idx, r in enumerate(ranks)}

class TextRank(object):
    def __init__(self, text):
        self.sent_tokenize = SentenceTokenizer()
        self.sentences = self.sent_tokenize.get_contents(text)
        self.nouns = self.sent_tokenize.get_nouns(self.sentences)
        self.graph_matrix = GraphMatrix()
        self.sent_graph = self.graph_matrix.build_sent_graph(self.nouns)
        self.words_graph, self.idx2word = self.graph_matrix.build_words_graph(self.nouns)
        self.rank = Rank()
        self.sent_rank_idx = self.rank.get_ranks(self.sent_graph)
        self.sorted_sent_rank_idx = sorted(self.sent_rank_idx, key=lambda k: self.sent_rank_idx[k], reverse=True)
        self.word_rank_idx = self.rank.get_ranks(self.words_graph)
        self.sorted_word_rank_idx = sorted(self.word_rank_idx, key=lambda k: self.word_rank_idx[k], reverse=True)

    def summarize(self, sent_num=3):
        summary = []
        index = []
        for idx in self.sorted_sent_rank_idx[:sent_num]:
            index.append(idx)
        index.sort()
        for inx in index:
            summary.append(self.sentences[idx])
        return summary

    def keywords(self, word_num=10):
        rank = Rank()
        rank_idx = rank.get_ranks(self.words_graph)
        sorted_rank_idx = sorted(rank_idx, key=lambda k: rank_idx[k], reverse=True)
        keywords = []
        index = []
        for idx in sorted_rank_idx[:word_num]:
            index.append(idx)
        for idx in index:
            keywords.append(self.idx2word[idx])
        return keywords

df = pd.read_csv('links.csv')
df.drop(df.columns[0], axis=1, inplace=True)
# print(df)
for domain, links in df.iteritems():
    for u in links:
        textrank = TextRank(u)
for row in textrank.summarize(3):
    print(row)
    print()
print('keywords: ', textrank.keywords())
