# -*- coding: utf-8 -*-
from urllib import robotparser

import bs4
import json
import numpy as np
import unicodedata
import requests
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
import re
from sklearn.metrics.pairwise import cosine_similarity
from urllib.parse import urlparse
import pandas as pd
from requests.models import MissingSchema
import spacy
import trafilatura
import urllib
import queue
from sklearn.feature_extraction.text import TfidfVectorizer
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
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
word_count = {}
docs=[]
stopwords=['지원', '기술', '사업', '안내', '연구', '소개', '센터', '및', '연구실', '신청', '제', '조회', '장비', '정보공개', '기업', '평', '구비', '현황', '정보', '비스', '운영', '기계', '경기도', '인증', '성', '사용', '창업', '본부', '바기', '신고', '등록', '고객', '제도', '개발', '역', '경기', '경영', '보고', '자료', '융합', '정책', '중소기업', '공고', '절차', '구단', '추진', '시스템', '교육', '환경', '홍보', '관련', '산업', '관리', '데터', '부소', '공지', '화학', '온라인', '바오', '헌장', '사항', '조직', '비', '문', '검색', '제품', '메뉴', '제출', '견학', '계획', '연구원', '입찰', '한국', '시험', '안전', '료', '협약', '용', '정산', '식', '스타트업', '위탁', '확인', '인권', '회원', '공동', '플랫폼', '활용', '교통', '생산', '글벌', '섬유', '회', '사트', '해외', '분석', '운드', '전략', '수출', '조사', '상담', '마케팅', '전자', '기관', '실적', '활동', '변경', '그인', '접수', '전체', '규정', '대상', '나노', '공시', '시설', '환원', '기술전', '전시회', '육성', '채용', '프린팅', '분야', '목록', '행사', '공정', '국토', '참여', '관', '개방', '본문', '소재', '방법', '일반', '결', '보기', '체', '업무', '사전', '신뢰', '특허', '종합', '정밀', '너지', '청구', '혁신', '청렴', '소식', '구축', '통합', '계', '협력', '직원', '인사말', '윤리', '비즈니스', '실명', '견', '특', '우수', '연구소', '카드', '처리', '단', '공개', '협', '논문', '전문', '수요', '개요', '마당', '계좌', '채용정보', '구부', '실', '질', '응용', '봇', '상', '시장', '연혁', '팹', '참', '입', '영상', '포럼', '체계', '학', '지역', '사회', '전', '제재', '유망', '집행', '대관', '발간', '제안', '프그램', '산업화', '스마트', '실증', '목표', '방침', '인건비', '납부', '비임', '현물', '수행', '연구개발', '지정', '진흥', '민간', '인공', '지능', '별', '행', '기획', '윤리경영', '갤러리', '길', '사', '개척', '부패', '동영상', '산학', '인프라', '지식', '경력', '구', '집', '구제', '학기술', '인재', '수렴', '부산', '발전', '만족', '매뉴얼', '연구시설', '동향', '김포시', '원단', '맞춤', '작성', '응답', '구매', '캠퍼스', '뉴스레터', '발굴', '부담', '비공개', '물', '반려동물', '투자', '부', '연구노트', '법규', '강화', '제공', '창', '보육', '심사', '감사', '그린', '도관', '보유', '팀', '매칭', '판', '역량', '페스북', '요청', '코나', '미션', '증명', '애', '수계약', '디자인', '체험', '금', '알림', '보도자료', '도란', '미래', '표준', '파트너', '자', '후', '바러스', '실험', '예약', '불복', '홈페지', '내용', '장애', '확산', '발표', '위원', '인력', '친', '연간', '녹색', '뢰', '면', '징계', '제조', '입금', '첨단', '탄소', '초', '검사', '광', '예고', '메카트닉스', '법령', '인쇄', '국', '비연', '내', '용자', '역학', '자연', '최종', '설립', '연료', '정보처리', '변환기', '플랜트', '드', '북부', '소리', '측정', '방향', '양주시', '청정', '진단', '교류', '동력', '플라즈마', '공헌', '천문', '광명시', '포천시', '나믹스', '평택시', '플라자', '협회', '본원', '국민', '대형', '공표', '네트워크', '레저', '앞', '제시', '지도', '점검', '상세', '동', '자동차', '부품', '컨설팅', '검증', '뉴스', '대전', '외부', '품목', '클럽', '최우수', '비즈', '담당자', '판매', '천연물', '유효', '공모', '유래', '사례', '기타', '원클릭', '경영인', '개인', '홈', '교육정', '열기', '답변', '민원', '공유', '클린', '총괄', '원장', '물류', '야기', '공', '센', '지침', '행위자', '동반성', '단계', '행동강령', '기능', '특정', '공책', '임관', '전용', '처', '고용', '수집', '기반', '연', '횟수', '차', '사버', '물질', '재연', '세미나', '건설', '밸리', '공정연', '목적', '비젼', '업사클', '거부', '조합', '무단', '펀드', '정부', '성장', '맵', '공통', '완화', '초고', '블라인드', '진출', '체결', '강소기업', '성공', '임대', '스타', '정규직', '한도', '자원', '용품', '보안', '정직', '디바스', '주관', '산림', '제작', '엔젤', '년도', '약', '네버', '패밀리', '캐릭터', '유투브', '패터닝', '투어', '인스타그램', '식각', '상시컨설팅', '기준', '국제', '박막', '진도', '소프트웨어', '피', '개인정보', '랩', '회계감사', '성실', '입증', '오시', '사업자', '소자', '연수', '대학', '건물', '결제']

def start(url):

   # empty list to store the contents of
   # the website fetched from our web-crawler
   wordlist = []
   source_code = requests.get(url, verify=False).text

   # BeautifulSoup object which will
   # ping the requested url for data
   soup = BeautifulSoup(source_code, 'html.parser')

   # Text in given web-page is stored under
   # the <div> tags with class <entry-content>
   # print(soup.findAll('a'))
   symbols = "!@#$%^&*()-+={[}]|\;:\"<>·?/.,└ "
   subcontext=[]

   for each_text in soup.findAll('a'):
      content = each_text.text
      subcontext.append(content)

      # for i in range(len(symbols)):
      #    content = content.replace(symbols[i], ' ')


      # # subcontext.append(content)
      # #
      # # subcontext = ",".join(subcontext)
      #docs.append(content)

      #words = Okt().nouns(content)
   str = " ".join(subcontext)
   str = re.sub('[a-zA-z]', '', str)
   str = unicodedata.normalize("NFKD", str)
   str = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]',
                    '', str)
   docs.append(str)
   # for each_word in words:
   #    wordlist.append(each_word)
   #    clean_wordlist(wordlist)
   #print(wordlist)


# Function removes any unwanted symbols


def clean_wordlist(wordlist):
	clean_list = []

	for word in wordlist:
		word = re.sub('[a-zA-z]', '', word)


	symbols = "\!@#$%^&*()_-+={[}]|\;:\"<>?/., "
	for i in range(len(stopwords)):
		word = word.replace(stopwords[i], "")
	for i in range(len(symbols)):
		word = word.replace(symbols[i], ' ')

	if len(word) > 0:
		clean_list.append(word)

	create_dictionary(clean_list)





# print(clean_list)


# Creates a dictionary containing each word's
# count and top_20 occurring words


def create_dictionary(clean_list):

   for word in clean_list:
      if word in word_count:
         word_count[word] += 1
      else:
         word_count[word] = 1

def tfidf(docs):

   vect = TfidfVectorizer(max_features=3)
   tfvect = vect.fit(docs)
   tfidv_df = pd.DataFrame(tfvect.transform(docs).toarray(), columns=sorted(vect.vocabulary_))
   cos=cosine_similarity(tfidv_df, tfidv_df)
   return cos



# Driver code
if __name__ == '__main__':

   df = pd.read_csv('links.csv')
   df.drop(df.columns[0],axis=1, inplace=True)
   #print(df)
   for domain, links in df.iteritems():
      for u in links:
         start(u)

   # word_count = {key: value for key, value in word_count.items() if value < 100}
   # word_count= sorted(word_count.items(), key=operator.itemgetter(1), reverse=True)
   # print(word_count)
   print(docs)

   print(pd.DataFrame(tfidf(docs)).to_string())