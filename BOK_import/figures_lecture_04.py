# Created by Kim Hyeongjun on 01/19/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.
# https://ecos.bok.or.kr/jsp/openapi/OpenApiController.jsp
# ecos.bok.or.kr 접속 (E-mail: yuii7890@naver.com)
# 개발 가이드 > 통계코드검색

import datetime
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from data_raw.def_authentication import *
import statsmodels.api as sm  # HP Filtering


def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny+dy, maxy+dy)


########################################################################################################################
# 그림 4.1 GDP 대비 경상수지와 GDP 갭 (%)
# 10.1.1 국민계정(2015년 기준년) - 주요지표 - 연간지표 [111Y002][YY] (1953 부터)
BOK111Y002 = pd.read_pickle('./BOK_raw/BOK111Y002.pkl')

# GDP 갭 계산
BOK111Y002_00 = BOK111Y002[BOK111Y002["ITEM_CODE1"] == "10101"].copy()  # 국내총생산(GDP)(명목, 십억원)
BOK111Y002_00["YYYYMMDD"] = BOK111Y002_00["TIME"] * 10000 + 101
BOK111Y002_00["DATETIME"] = pd.to_datetime(BOK111Y002_00['YYYYMMDD'].astype(str), errors='coerce', format='%Y%m%d')
BOK111Y002_00["GDP"] = BOK111Y002_00["DATA_VALUE"].copy() * 1000000000  # 국내총생산(GDP)(명목, 원)
BOK111Y002_00["Actual_GDP"] = BOK111Y002_00["DATA_VALUE"].copy()  # 국내총생산(GDP)(명목, 십억원)

BOK111Y002_03 = BOK111Y002[BOK111Y002["ITEM_CODE1"] == "90103"].copy()  # GDP 디플레이터 (2015=100)
BOK111Y002_03["YYYYMMDD"] = BOK111Y002_03["TIME"] * 10000 + 101
BOK111Y002_03["DATETIME"] = pd.to_datetime(BOK111Y002_03['YYYYMMDD'].astype(str), errors='coerce', format='%Y%m%d')
BOK111Y002_03["GDP_Deflator"] = BOK111Y002_03["DATA_VALUE"].copy()  # GDP 디플레이터 (2015=100)

BOK111Y002_00 = pd.merge(BOK111Y002_00, BOK111Y002_03[["DATETIME", "GDP_Deflator"]], left_on='DATETIME', right_on='DATETIME', how='left')
BOK111Y002_00["Real_GDP"] = BOK111Y002_00["Actual_GDP"] / BOK111Y002_00["GDP_Deflator"]
cycle, trend = sm.tsa.filters.hpfilter(BOK111Y002_00["Real_GDP"], 100)  # 람다=100 으로 놓는게 중요 (경험치...)
BOK111Y002_00["Potential_GDP"] = trend
BOK111Y002_00["GDP_Gap"] = ((BOK111Y002_00["Real_GDP"] - BOK111Y002_00["Potential_GDP"]) / BOK111Y002_00["Potential_GDP"]) * 100  # GDP 갭 (%)

BOK111Y002_01 = BOK111Y002[BOK111Y002["ITEM_CODE1"] == "1010101"].copy()  # 국내총생산(GDP)(명목, 억달러)
BOK111Y002_01["YYYYMMDD"] = BOK111Y002_01["TIME"] * 10000 + 101
BOK111Y002_01["DATETIME"] = pd.to_datetime(BOK111Y002_01['YYYYMMDD'].astype(str), errors='coerce', format='%Y%m%d')
BOK111Y002_01["GDP"] = BOK111Y002_01["DATA_VALUE"].copy() * 100000000  # 국내총생산(GDP)(명목, 달러)
BOK111Y002_01["Actual_GDP"] = BOK111Y002_01["DATA_VALUE"].copy()  # 국내총생산(GDP)(명목, 억달러)

# GDP 대비 경상수지 계산
# 8.1.1 국제수지 [022Y013][MM,QQ,YY] (1980.01, 1980Q1 부터)
BOK022Y013 = pd.read_pickle('./BOK_raw/BOK022Y013.pkl')

BOK022Y013_00 = BOK022Y013[BOK022Y013["ITEM_CODE1"] == "000000"].copy()  # 경상수지 (백만달러)
BOK022Y013_00["Current_Account"] = BOK022Y013_00["DATA_VALUE"].copy() * 1000000  # 경상수지(current account) (달러)
BOK022Y013_00["Current_Account"] = BOK022Y013_00["Current_Account"].rolling(window=12).sum()  # 경상수지 12개월 누적

df_CA_to_GDP = pd.merge(BOK022Y013_00, BOK111Y002_01[["DATETIME", "GDP"]], left_on='DATETIME', right_on='DATETIME', how='left')
df_CA_to_GDP["GDP"] = df_CA_to_GDP["GDP"].fillna(method='ffill')
df_CA_to_GDP["CA_to_GDP"] = df_CA_to_GDP["Current_Account"] / df_CA_to_GDP["GDP"] * 100  # GDP 대비 경상수지 (%)

# 그림 4.1 GDP 대비 경상수지와 GDP 갭 (%)
# 시각화: 월별 시계열 자료 1개를 표시
fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300

plt.plot(df_CA_to_GDP["DATETIME"], df_CA_to_GDP["CA_to_GDP"], color='r', label="Current Account to GDP")
plt.plot(BOK111Y002_00["DATETIME"], BOK111Y002_00["GDP_Gap"], color='g', label="GDP Gap")

xlim_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')
plt.xlim(xlim_start, )
plt.ylim(-10, 15)
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Percentage (%)', fontsize=10)
plt.legend(loc='upper left')
plt.show()

plt.savefig("./BOK_processed/fig4.1_current_account_to_gdp_and_gdp_gap.png")
