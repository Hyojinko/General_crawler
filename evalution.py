import re

from nltk.translate.bleu_score import sentence_bleu
import pandas as pd
from nltk.tokenize import word_tokenize
from rouge import Rouge
from konlpy.tag import Okt

import matplotlib.pyplot as plt
df = pd.read_csv('/Users/kohyojin/Desktop/IDALab/2021-2 research/wordrank/result.csv')
ref_df = pd.read_csv('/Users/kohyojin/Desktop/IDALab/2021-2 research/wordrank/reference.csv')
res_df = pd.concat([df, ref_df['sentences']], axis=1)
bleu_score = []
okt = Okt()

stopwords = ['지원', '기술', '사업', '안내', '연구', '소개', '센터', '연구실', '신청',  '조회', '장비', '정보공개', '기업',

                          '구비', '현황', '정보', '비스', '운영', '기계', '경기도', '인증',  '사용', '창업', '본부', '바기', '신고', '등록',
                          '고객',
                          '제도', '개발',  '경기', '경영', '보고', '자료', '융합', '정책', '중소기업', '공고', '절차', '구단', '추진', '시스템',
                          '교육',
                          '환경', '홍보', '관련', '산업', '관리', '데터', '부소', '공지', '화학', '온라인', '바오', '헌장', '사항', '조직',
                          '검색', '제품', '메뉴', '제출', '견학', '계획', '연구원', '입찰', '한국', '시험', '안전',  '협약',  '정산',
                          '스타트업', '위탁', '확인', '인권', '회원', '공동', '플랫폼', '활용', '교통', '생산', '글벌', '섬유', '사트', '해외',
                          '분석',
                          '운드', '전략', '수출', '조사', '상담', '마케팅', '전자', '기관', '실적', '활동', '변경', '그인', '접수', '전체', '규정',
                          '대상',
                          '나노', '공시', '시설', '환원', '기술이전', '전시회', '육성', '채용', '프린팅', '분야', '목록', '행사', '공정', '국토', '참여',

                          '개방', '본문', '소재', '방법', '일반',  '보기','업무', '사전', '신뢰', '특허', '종합', '정밀', '너지', '청구',
                          '혁신',
                          '청렴', '소식', '구축', '통합',  '협력', '직원', '인사말', '윤리', '비즈니스', '실명',  '우수', '연구소',
                          '카드',
                          '처리', '공개', '협', '논문', '전문', '수요', '개요', '마당', '계좌', '채용정보', '구부','응용',
                          '상',
                          '시장', '연혁',  '영상', '포럼', '체계',  '지역', '사회', '제재', '유망', '집행', '대관',
                          '발간',
                          '제안', '프그램', '산업화', '스마트', '실증', '목표', '방침', '인건비', '납부', '비임', '현물', '수행', '연구개발', '지정',
                          '진흥',' ','\r','\n',
                          '민간', '인공', '지능',  '기획', '윤리경영', '갤러리', '연락처', '길', '사', '개척', '부패', '동영상', '산학',
                          '인프라', '지식',
                          '경력',  '구제', '학기술', '인재', '수렴', '부산', '발전', '만족', '매뉴얼', '연구시설', '동향', '김포시', '원단',
                          '맞춤',
                          '작성', '응답', '구매', '캠퍼스', '뉴스레터', '발굴', '부담', '비공개', '물', '반려동물', '투자', '부', '연구노트', '법규',
                          '강화',
                          '제공',  '보육', '심사', '감사', '그린', '도관', '보유', '매칭', '역량', '페스북', '요청', '코나', '미션',
                          '증명',
                           '수계약', '디자인말', '체험', '알림', '보도자료', '도란', '미래', '표준', '파트너', '바러스', '실험',
                          '예약',
                          '불복', '홈페지', '내용', '장애', '확산', '발표', '위원', '인력', '연간', '녹색',  '징계', '제조', '입금',
                          '첨단',
                          '탄소',  '검사', '예고', '메카트닉스', '법령', '인쇄', '국', '비연', '용자', '역학', '자연', '최종', '설립',
                          '연료', '정보처리', '변환기', '플랜트', '북부', '소리', '측정', '방향', '양주시', '청정', '진단', '교류', '동력',
                          '플라즈마',
                          '공헌', '천문', '광명시', '포천시', '나믹스', '평택시', '플라자', '협회', '본원', '국민', '대형', '공표', '네트워크', '레저',

                          '제시', '지도', '점검', '상세', '동', '자동차', '부품', '컨설팅', '검증', '뉴스', '대전', '외부', '품목', '클럽', '최우수',
                          '비즈',
                          '담당자', '판매', '천연물', '유효', '공모', '유래', '사례', '기타', '원클릭', '경영인', '개인', '홈', '교육정', '열기', '답변',
                          '민원',
                          '공유', '클린', '총괄', '원장', '물류', '야기',  '지침', '행위자', '동반성', '단계', '행동강령', '기능', '특정',
                          '공책',
                          '임관', '전용', '처', '고용', '수집', '기반',  '횟수', '차', '사버', '물질', '재연', '세미나', '건설', '밸리', '공정연',
                          '목적', '비젼', '업사클', '거부', '조합', '무단', '펀드', '정부', '성장', '맵', '공통', '완화', '초고', '블라인드', '진출',
                          '체결',
                          '강소기업', '성공', '임대', '스타', '정규직', '한도', '자원', '용품', '보안', '정직', '디바스', '주관', '산림', '제작', '엔젤',
                          '년도',
                          '네버', '패밀리', '캐릭터', '유투브', '패터닝', '투어', '인스타그램', '식각', '상시컨설팅', '기준', '국제', '박막', '진도',
                          '소프트웨어',  '개인정보', '회계감사', '성실', '입증', '오시', '사업자', '소자', '연수', '대학', '건물', '결제',
                          '도우미', '레이아웃',
                          '성숙', '거래', '설명', '보고서', '서식', '바로가기', '메인', '재산', '경매', '거래소', '로그인', '가입', '다운로드',
                          '나눔', '문의', '법인', '상용', '이용',
                          '주소', '출연', '프로그램', '이메일', '부서', '사이트', '약관', '바로가기', '마이', '페이지', '연구기관', '상표', '서비스',
                          '아이디어', '국유', '재산', '패스워드',
                          '설정', '기술자', '나눔', '멘토', '애로', '실험동물', '협업', '회의실', '임무', '구성원', '한의학', '문관', '공공', '서울',
                          '대구', '광주', '생활', '문화', '로드',
                          '길찾기', '크게', '유관', '소액', '무상', '단체','본문내용','바로가기', '기술이전절차','기술성숙도','기술성숙도(TRL)','관련기관안내',
                          '기술이전검색','기술이전온라인신청','고객의','소리','오시는길','주씨엔에이','주스트릭','주우리아이들플러스']

for index, row in res_df.iterrows():
    keyword = row[2]
    summary = row[3]
    reference = row[4]
    summary_tokenized = []
    reference_tokenized = []
    '''if summary != '':
        summary_tokenized.append(' '.join([noun for noun in okt.nouns(str(summary))
                               if  len(noun) > 1]))
    if reference != '':
        reference_tokenized.append(' '.join([noun for noun in okt.nouns(str(reference))
                               if noun not in stopwords and len(noun) > 1]))'''

    #reference_tokenized = word_tokenize(reference)
    rouge = Rouge()
    scores = rouge.get_scores(summary, reference,avg=True)
    for key in scores:
        print(key)
        if type(scores[key]) == str or type(scores[key]) == int:
            print(key,':',scores[key])
        if type(scores[key]) == list:
            for i in scores[key]:
                print(key,':',i)
        if type(scores[key]) == dict:
            for e in scores[key]:
                print(e,':', scores[key][e])
    '''results['rouge1-f'].append(rouge1_f_metric)
    results['rouge1-p'].append(rouge1_p_metric)
    results['rouge1-r'].append(rouge1_r_metric)

    results['rouge2-f'].append(rouge2_f_metric)
    results['rouge2-p'].append(rouge2_p_metric)
    results['rouge2-r'].append(rouge2_r_metric)

    results['rougel-f'].append(rougel_f_metric)
    results['rougel-p'].append(rougel_p_metric)
    results['rougel-r'].append(rougel_r_metric)
'''




'''bleu = sentence_bleu(summary_tokenized, reference_tokenized)
    print(bleu)
    bleu_score.append(bleu)
bleu_score = pd.Series(bleu_score)
bleu_score.plot()
plt.show()'''




