# Created by Kim Hyeongjun on 05/01/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.
# investpy 패키지의 종목명은 investing.com 에서 검색 가능
import pandas as pd
import numpy as np
import investpy
import mplfinance as mpf
import datetime as dt
import matplotlib.pyplot as plt

# Import Dataset
krx_etf_market_price = pd.read_pickle('./KRX_raw/krx_etf_market_price_20211230.pkl')
krx_etf_basic_information = pd.read_pickle('./KRX_raw/krx_etf_basic_information.pkl')

# Import XLSX File
df_list_ETF = pd.read_excel(
    './KRX_raw/list_ETF.xlsx', sheet_name="Sheet1", header=0, skiprows=0, skipfooter=0)

krx_etf_market_price_month = pd.read_excel(
    './KRX_raw/krx_etf_market_price_20211201_20211230.xlsx', sheet_name="Sheet1", header=0, skiprows=0, skipfooter=0)


# 숫자로된 종목코드를 문자로 바꾸고 6자리 0으로 채운 뒤 앞에 A를 붙인다
df_list_ETF["종목번호"] = df_list_ETF["종목번호"].apply(str)
df_list_ETF["종목번호"] = df_list_ETF["종목번호"].str.zfill(6)

# 숫자로된 종목코드를 문자로 바꾸고 6자리 0으로 채운 뒤 앞에 A를 붙인다
krx_etf_basic_information["단축코드"] = krx_etf_basic_information["단축코드"].apply(str)
krx_etf_basic_information["단축코드"] = krx_etf_basic_information["단축코드"].str.zfill(6)

# 숫자로된 종목코드를 문자로 바꾸고 6자리 0으로 채운 뒤 앞에 A를 붙인다
krx_etf_market_price["종목코드"] = krx_etf_market_price["종목코드"].apply(str)
krx_etf_market_price["종목코드"] = krx_etf_market_price["종목코드"].str.zfill(6)

# 숫자로된 종목코드를 문자로 바꾸고 6자리 0으로 채운 뒤 앞에 A를 붙인다
krx_etf_market_price_month["종목코드"] = krx_etf_market_price_month["종목코드"].apply(str)
krx_etf_market_price_month["종목코드"] = krx_etf_market_price_month["종목코드"].str.zfill(6)


# 종목코드, 기본정보, 시세정보 연결
df_etf = pd.merge(df_list_ETF[["구분", "종목번호"]], krx_etf_basic_information[["단축코드", "한글종목약명", "상장일", "기초지수명", "총보수", "과세유형"]], left_on='종목번호', right_on='단축코드', how='left')
df_etf = pd.merge(df_etf, krx_etf_market_price[["종목코드", "시가총액", "종가", "순자산가치(NAV)"]], left_on='종목번호', right_on='종목코드', how='left')
df_etf = pd.merge(df_etf, krx_etf_market_price_month[["종목코드", "거래량", "거래대금"]], left_on='종목번호', right_on='종목코드', how='left')

df_etf.pop("단축코드")
df_etf.pop("종목코드_x")
df_etf.pop("종목코드_y")
df_etf["시총대비거래대금(월간)"] = (df_etf["거래대금"]/df_etf["시가총액"]).round(4)
df_etf["시가총액"] = (df_etf["시가총액"] / 100000000).round(2)
df_etf["거래대금"] = (df_etf["거래대금"] / 100000000).round(2)

df_etf2 = df_etf[["구분", "종목번호", "한글종목약명", "기초지수명", "과세유형", "총보수", "시가총액", "시총대비거래대금(월간)", "종가"]]

# 엑셀 저장
df_etf2.to_excel('./KRX_raw/list_ETF2.xlsx', index=False, index_label=None)
