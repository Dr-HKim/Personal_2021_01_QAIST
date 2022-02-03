# Created by Kim Hyeongjun on 2021.10.01.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.
# 목표: 한국거래소 KRX 정보데이터시스템(http://data.krx.co.kr/)에서 자료를 크롤링한다.

# 참고: https://blog.naver.com/ellijahbyeon/222213048898

import requests
import pandas as pd
from io import BytesIO
import time

# 통계 > 기본통계 > 주식 > 종목시세 > 전종목시세
# http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201
# 크롬 개발자도구(F12) 사용, Network 탭
# 페이지에서 엑셀 다운로드 아이콘을 클릭하면 Network 탭에서 generate.cmd 와 download.cmd 를 확인할 수 있다.
# generate.cmd > Headers > General > Request URL:
# http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd
# generate.cmd > Headers > Form Data : (아래 내용 확인 가능)
# mktId: ALL
# trdDd: 20211115
# share: 1
# money: 1
# csvxls_isNo: false
# name: fileDown
# url: dbms/MDC/STAT/standard/MDCSTAT01501
# generate.cmd > Headers > Request Headers : (아래 내용 확인 가능)
# Referer: http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36
# download.cmd > Headers > General > Request URL:
# http://data.krx.co.kr/comm/fileDn/download_excel/download.cmd

tdate = 20211111  # 날짜

gen_req_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
query_str_parms = {
    'mktId': 'ALL',
    'trdDd': str(tdate),
    'share': '1',
    'money': '1',
    'csvxls_isNo': 'false',
    'name': 'fileDown',
    'url': 'dbms/MDC/STAT/standard/MDCSTAT01501'
}
headers = {
    'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'  # generate.cmd 에서 찾아서 입력
}
r = requests.get(gen_req_url, query_str_parms, headers=headers)

gen_req_url = 'http://data.krx.co.kr/comm/fileDn/download_excel/download.cmd'
form_data = {
    'code': r.content
}
r = requests.post(gen_req_url, form_data, headers=headers)

df = pd.read_excel(BytesIO(r.content))
df['일자'] = tdate

path = './data_raw/'
file_name = 'basic_' + str(tdate) + '.xlsx'
df.to_excel(path+file_name, index=False, index_label=None)
print('KRX crawling completed :', tdate)

########################################################################################################################
# 지수 > 주가지수 > 지수구성종목
# generate.cmd > Headers > General > Request URL:
# http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd
# generate.cmd > Headers > Form Data : (아래 내용 확인 가능)
# tboxindIdx_finder_equidx0_1: 코스피 200
# indIdx: 1
# indIdx2: 028
# codeNmindIdx_finder_equidx0_1: 코스피 200
# param1indIdx_finder_equidx0_1:
# trdDd: 20211115
# money: 3
# csvxls_isNo: false
# name: fileDown
# url: dbms/MDC/STAT/standard/MDCSTAT00601
# generate.cmd > Headers > Request Headers : (아래 내용 확인 가능)
# Referer: http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36
# download.cmd > Headers > General > Request URL:
# http://data.krx.co.kr/comm/fileDn/download_excel/download.cmd

tdate = 20211111  # 날짜


def get_kospi200_companies(tdate):
    gen_req_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
    query_str_parms = {
        "tboxindIdx_finder_equidx0_1": '코스피 200',
        "indIdx": "1",
        "indIdx2": "028",
        "codeNmindIdx_finder_equidx0_1": "코스피 200",
        "param1indIdx_finder_equidx0_1": "",
        "trdDd": str(tdate),
        "money": "3",
        "csvxls_isNo": "false",
        "name": "fileDown",
        "url": "dbms/MDC/STAT/standard/MDCSTAT00601"
    }
    headers = {
        'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'  # generate.cmd 에서 찾아서 입력
    }
    r = requests.get(gen_req_url, query_str_parms, headers=headers)

    gen_req_url = 'http://data.krx.co.kr/comm/fileDn/download_excel/download.cmd'
    form_data = {
        'code': r.content
    }
    r = requests.post(gen_req_url, form_data, headers=headers)

    df = pd.read_excel(BytesIO(r.content))
    df['일자'] = tdate
    print('KRX crawling completed :', tdate)
    return df


# 코스피200 지수는 매년 6, 12월에 정기 변경이 이루어진다.
# 5월부터 10월말까지 시가총액을 기준으로 통상 11월 말에 교체 종목이 발표된다.
list_date = [20040107, 20050104, 20060104, 20070104, 20080104, 20090105, 20100104, 20110104, 20120104, 20130104,
             20140106, 20150105, 20160104, 20170104, 20180104, 20190104, 20200106, 20210104,
             20040705, 20050704, 20060704, 20070704, 20080704, 20090706, 20100705, 20110704, 20120704, 20130704,
             20140704, 20150706, 20160704, 20170704, 20180704, 20190704, 20200706, 20210705]

# 비어있는 데이터프레임 만들기
df_kospi200_companies_crawling = pd.DataFrame(columns=["종목코드", "종목명", "종가", "대비", "등락률", "상장시가총액", "일자"])

for date in list_date:
    df_kospi200 = get_kospi200_companies(tdate=date)
    if len(df_kospi200) < 10:
        print(str(date) + " is empty")
    df_kospi200_companies_crawling = pd.concat([df_kospi200_companies_crawling, df_kospi200])
    time.sleep(1)

df_kospi200_companies = df_kospi200_companies_crawling.sort_values(by=['일자', '종목코드']).copy()

# 숫자로된 종목코드를 문자로 바꾸고 6자리 0으로 채운 뒤 앞에 A를 붙인다
df_kospi200_companies["종목코드_new"] = df_kospi200_companies["종목코드"].apply(str)
df_kospi200_companies["종목코드_new"] = "A" + df_kospi200_companies["종목코드_new"].str.zfill(6)

# 데이터 저장
df_kospi200_companies.to_excel('./data_raw/df_kospi200_companies.xlsx', index=False, index_label=None)
df_kospi200_companies.to_pickle('./data_raw/df_kospi200_companies.pkl')
