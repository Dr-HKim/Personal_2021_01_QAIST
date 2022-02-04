# Created by Kim Hyeongjun on 2021.10.01.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.
# 목표: 한국거래소 KRX 정보데이터시스템(http://data.krx.co.kr/)에서 자료를 크롤링한다.

# 참고: https://blog.naver.com/ellijahbyeon/222213048898

import requests
import pandas as pd
from io import BytesIO
import time

########################################################################################################################
# 통계 > 기본통계 > 증권상품 > ETF > 전종목 기본정보
# http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201030104
# 크롬 개발자도구(F12) 사용, Network 탭
# 페이지에서 엑셀 다운로드 아이콘을 클릭하면 Network 탭에서 generate.cmd 와 download.cmd 를 확인할 수 있다.
# generate.cmd > Headers > General > Request URL:
# http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd
# generate.cmd > Headers > Form Data : (아래 내용 확인 가능)
# locale: ko_KR
# share: 1
# csvxls_isNo: false
# name: fileDown
# url: dbms/MDC/STAT/standard/MDCSTAT04601
# generate.cmd > Headers > Request Headers : (아래 내용 확인 가능)
# Referer: http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201030104
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36
# download.cmd > Headers > General > Request URL:
# http://data.krx.co.kr/comm/fileDn/download_excel/download.cmd

tdate = 20220203  # 날짜 (필요없음)

gen_req_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
query_str_parms = {
    'locale': 'ko_KR',
    'share': '1',
    'csvxls_isNo': 'false',
    'name': 'fileDown',
    'url': 'dbms/MDC/STAT/standard/MDCSTAT04601'
}
headers = {
    'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36'  # generate.cmd 에서 찾아서 입력
}
r = requests.get(gen_req_url, query_str_parms, headers=headers)

gen_req_url = 'http://data.krx.co.kr/comm/fileDn/download_excel/download.cmd'
form_data = {
    'code': r.content
}
r = requests.post(gen_req_url, form_data, headers=headers)

df = pd.read_excel(BytesIO(r.content))
df['갱신일자'] = tdate

df.to_pickle('./KRX_raw/krx_etf_basic_information.pkl')


########################################################################################################################
# 통계 > 기본통계 > 증권상품 > ETF > 전종목 시세
# http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201030104
# 크롬 개발자도구(F12) 사용, Network 탭
# 페이지에서 엑셀 다운로드 아이콘을 클릭하면 Network 탭에서 generate.cmd 와 download.cmd 를 확인할 수 있다.
# generate.cmd > Headers > General > Request URL:
# http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd
# generate.cmd > Headers > Form Data : (아래 내용 확인 가능)
# locale: ko_KR
# share: 1
# csvxls_isNo: false
# name: fileDown
# url: dbms/MDC/STAT/standard/MDCSTAT04601
# generate.cmd > Headers > Request Headers : (아래 내용 확인 가능)
# Referer: http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201030104
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36
# download.cmd > Headers > General > Request URL:
# http://data.krx.co.kr/comm/fileDn/download_excel/download.cmd

tdate = 20211230  # 날짜

gen_req_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
query_str_parms = {
    'locale': 'ko_KR',
    'trdDd': str(tdate),
    'share': '1',
    'money': '1',
    'csvxls_isNo': 'false',
    'name': 'fileDown',
    'url': 'dbms/MDC/STAT/standard/MDCSTAT04301'
}
headers = {
    'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36'  # generate.cmd 에서 찾아서 입력
}
r = requests.get(gen_req_url, query_str_parms, headers=headers)

gen_req_url = 'http://data.krx.co.kr/comm/fileDn/download_excel/download.cmd'
form_data = {
    'code': r.content
}
r = requests.post(gen_req_url, form_data, headers=headers)

df = pd.read_excel(BytesIO(r.content))
df['갱신일자'] = tdate

file_name = 'krx_etf_market_price_' + str(tdate) + '.pkl'

df.to_pickle('./KRX_raw/' + file_name)



########################################################################################################################
# 통계 > 기본통계 > 증권상품 > ETF > 13102 전종목 등락률

strDd = 20211201  # 시작날짜
endDd = 20211229  # 종료날짜

gen_req_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
query_str_parms = {
    'locale': 'ko_KR',
    'strDd': str(strDd),
    'endDd': str(endDd),
    'share': '1',
    'money': '1',
    'csvxls_isNo': 'false',
    'name': 'fileDown',
    'url': 'dbms/MDC/STAT/standard/MDCSTAT04401'
}
headers = {
    'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36'  # generate.cmd 에서 찾아서 입력
}
r = requests.get(gen_req_url, query_str_parms, headers=headers)

gen_req_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
form_data = {
    'code': r.content
}
r = requests.post(gen_req_url, form_data, headers=headers)

df = pd.read_csv(BytesIO(r.content), encoding='cp949')


df = pd.read_excel(BytesIO(r.content))

df = pd.read_csv(BytesIO(r.content), encoding='euc-kr')


file_name = 'krx_etf_market_price_' + str(strDd) + "_" + str(endDd) + '.pkl'

df.to_pickle('./KRX_raw/' + file_name)
