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
    def __init__(self):
        self.stopwords = ['지원', '기술', '사업', '안내', '연구', '소개', '센터', '및', '연구실', '신청', '제', '조회', '장비', '정보공개', '기업',
                          '평',
                          '구비', '현황', '정보', '비스', '운영', '기계', '경기도', '인증', '성', '사용', '창업', '본부', '바기', '신고', '등록',
                          '고객',
                          '제도', '개발', '역', '경기', '경영', '보고', '자료', '융합', '정책', '중소기업', '공고', '절차', '구단', '추진', '시스템',
                          '교육',
                          '환경', '홍보', '관련', '산업', '관리', '데터', '부소', '공지', '화학', '온라인', '바오', '헌장', '사항', '조직', '비', '문',
                          '검색', '제품', '메뉴', '제출', '견학', '계획', '연구원', '입찰', '한국', '시험', '안전', '료', '협약', '용', '정산', '식',
                          '스타트업', '위탁', '확인', '인권', '회원', '공동', '플랫폼', '활용', '교통', '생산', '글벌', '섬유', '회', '사트', '해외',
                          '분석',
                          '운드', '전략', '수출', '조사', '상담', '마케팅', '전자', '기관', '실적', '활동', '변경', '그인', '접수', '전체', '규정',
                          '대상',
                          '나노', '공시', '시설', '환원', '기술이전', '전시회', '육성', '채용', '프린팅', '분야', '목록', '행사', '공정', '국토', '참여',
                          '관',
                          '개방', '본문', '소재', '방법', '일반', '결', '보기', '체', '업무', '사전', '신뢰', '특허', '종합', '정밀', '너지', '청구',
                          '혁신',
                          '청렴', '소식', '구축', '통합', '계', '협력', '직원', '인사말', '윤리', '비즈니스', '실명', '견', '특', '우수', '연구소',
                          '카드',
                          '처리', '단', '공개', '협', '논문', '전문', '수요', '개요', '마당', '계좌', '채용정보', '구부', '실', '질', '응용', '봇',
                          '상',
                          '시장', '연혁', '팹', '참', '입', '영상', '포럼', '체계', '학', '지역', '사회', '전', '제재', '유망', '집행', '대관',
                          '발간',
                          '제안', '프그램', '산업화', '스마트', '실증', '목표', '방침', '인건비', '납부', '비임', '현물', '수행', '연구개발', '지정',
                          '진흥',
                          '민간', '인공', '지능', '별', '행', '기획', '윤리경영', '갤러리', '연락처', '길', '사', '개척', '부패', '동영상', '산학',
                          '인프라', '지식',
                          '경력', '구', '집', '구제', '학기술', '인재', '수렴', '부산', '발전', '만족', '매뉴얼', '연구시설', '동향', '김포시', '원단',
                          '맞춤',
                          '작성', '응답', '구매', '캠퍼스', '뉴스레터', '발굴', '부담', '비공개', '물', '반려동물', '투자', '부', '연구노트', '법규',
                          '강화',
                          '제공', '창', '보육', '심사', '감사', '그린', '도관', '보유', '팀', '매칭', '판', '역량', '페스북', '요청', '코나', '미션',
                          '증명',
                          '애', '수계약', '디자인말', '체험', '금', '알림', '보도자료', '도란', '미래', '표준', '파트너', '자', '후', '바러스', '실험',
                          '예약',
                          '불복', '홈페지', '내용', '장애', '확산', '발표', '위원', '인력', '친', '연간', '녹색', '뢰', '면', '징계', '제조', '입금',
                          '첨단',
                          '탄소', '초', '검사', '광', '예고', '메카트닉스', '법령', '인쇄', '국', '비연', '내', '용자', '역학', '자연', '최종', '설립',
                          '연료', '정보처리', '변환기', '플랜트', '드', '북부', '소리', '측정', '방향', '양주시', '청정', '진단', '교류', '동력',
                          '플라즈마',
                          '공헌', '천문', '광명시', '포천시', '나믹스', '평택시', '플라자', '협회', '본원', '국민', '대형', '공표', '네트워크', '레저',
                          '앞',
                          '제시', '지도', '점검', '상세', '동', '자동차', '부품', '컨설팅', '검증', '뉴스', '대전', '외부', '품목', '클럽', '최우수',
                          '비즈',
                          '담당자', '판매', '천연물', '유효', '공모', '유래', '사례', '기타', '원클릭', '경영인', '개인', '홈', '교육정', '열기', '답변',
                          '민원',
                          '공유', '클린', '총괄', '원장', '물류', '야기', '공', '센', '지침', '행위자', '동반성', '단계', '행동강령', '기능', '특정',
                          '공책',
                          '임관', '전용', '처', '고용', '수집', '기반', '연', '횟수', '차', '사버', '물질', '재연', '세미나', '건설', '밸리', '공정연',
                          '목적', '비젼', '업사클', '거부', '조합', '무단', '펀드', '정부', '성장', '맵', '공통', '완화', '초고', '블라인드', '진출',
                          '체결',
                          '강소기업', '성공', '임대', '스타', '정규직', '한도', '자원', '용품', '보안', '정직', '디바스', '주관', '산림', '제작', '엔젤',
                          '년도',
                          '약', '네버', '패밀리', '캐릭터', '유투브', '패터닝', '투어', '인스타그램', '식각', '상시컨설팅', '기준', '국제', '박막', '진도',
                          '소프트웨어', '피', '개인정보', '랩', '회계감사', '성실', '입증', '오시', '사업자', '소자', '연수', '대학', '건물', '결제',
                          '도우미', '레이아웃',
                          '창', '성숙', '거래', '설명', '보고서', '서식', '바로가기', '메인', '재산', '경매', '거래소', '로그인', '가입', '다운로드',
                          '나눔', '문의', '법인', '상용', '이용',
                          '주소', '출연', '프로그램', '이메일', '부서', '사이트', '약관', '바로가기', '마이', '페이지', '연구기관', '상표', '서비스',
                          '아이디어', '국유', '재산', '패스워드',
                          '설정', '기술자', '나눔', '멘토', '애로', '실험동물', '협업', '회의실', '임무', '구성원', '한의학', '문관', '공공', '서울',
                          '대구', '광주', '생활', '문화', '로드',
                          '길찾기', '크게', '유관', '소액', '무상', '단체']

    def get_contents(self, url):
        source_code = requests.get(url).text
        wordlist = []
        # BeautifulSoup object which will
        # ping the requested url for data
        soup = BeautifulSoup(source_code, 'html.parser')

        # Text in given web-page is stored under
        # the <div> tags with class <entry-content>
        # print(soup.findAll('a'))
        sentences = []
        for each_text in soup.findAll('a'):
            content = each_text.text
            # content = content.lower()
            sentences.append(content)
        return sentences

    def get_nouns(self, sentences):
        clean_list = []
        wordlist = []
        for sent in sentences:
            words = Okt().nouns(sent)
            for w in words:
                wordlist.append(w)

        for word in wordlist:
            word = re.sub('[a-zA-z]', '', word)
            symbols = "!@#$%^&*()_-+={[}]|\;:\"<>?/., "
            for i in range(len(symbols)):
                word = word.replace(symbols[i], '')
            if len(word) > 0:
                clean_list.append(word)
        nouns = []
        '''for word in clean_list:

            if word != '':
                #nouns.append(' '.join([nouns for noun in Okt.nouns(sentence)
                             if len(noun) > 1]))
                nouns.append(' '.join([noun for noun in word if noun not in self.stopwords and len(noun)>1]))
                '''
        nouns.append(' '.join([noun for noun in clean_list if noun not in self.stopwords and len(noun) > 1]))

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
        cnt_mat = normalize(self.cnt.fit_transform(sentence).toarray().astype(float), axis=0)
        vocab = self.cnt.vocabulary_
        return np.dot(cnt_mat.T, cnt_mat), {vocab[word]: word for word in vocab}


class Rank(object):
    def get_ranks(self, graph, d=0.85):
        A = graph
        matrix_size = A.shape[0]
        for id in range(matrix_size):
            A[id, id] = 0
            link_sum = np.sum(A[:, id])
            if link_sum != 0:
                A[:, id] /= link_sum
            A[:, id] *= -d
            A[id, id] = 1
        B = (1 - d) * np.ones((matrix_size, 1))
        ranks = np.linalg.solve(A, B)
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
keywords=[]
summaries = []
sumByDomain = pd.DataFrame(index = ['keywords','summary'] )
for domain, links in df.iteritems():
    for u in links:
        try:
            textrank = TextRank(u)
            keyword = textrank.keywords()
            keywords.extend(keyword)
            summary = textrank.summarize(3)
            summaries.extend(summary)
        except ValueError:
            continue
    '''print(keywords)
    sumByDomain=sumByDomain[domain]['keywords'].append(pd.Series(keywords))
    sumByDomain[domain]['summary'] = summaries'''
#print('keywords: ', textrank.keywords())


#Reference https://excelsior-cjh.tistory.com/93
