# 1강 강의개요
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
# 그림 1.1 소비자물가지수 (월간)
# 4.2.1 소비자물가지수(2020=100)(전국, 특수분류) [901Y010][A,M,Q] (1975.01 부터)
BOK_901Y010 = pd.read_pickle('./Market_Watch_Data/BOK_901Y010.pkl')
BOK_901Y010_00 = BOK_901Y010[BOK_901Y010["ITEM_CODE1"] == "00"].copy()  # 총지수
BOK_901Y010_00["pct_change_DATA_VALUE"] = (BOK_901Y010_00["DATA_VALUE"].pct_change(12)) * 100  # 퍼센트 변화량 (전년비)

# 시각화
fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
fig.set_size_inches(1800/300, 1200/300)  # 그래프 크기 지정, DPI=300

plt.plot(BOK_901Y010_00["DATETIME"], BOK_901Y010_00["DATA_VALUE"], color='r', label="CPI")
xlim_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')
plt.xlim(xlim_start, )
plt.ylim(30, 120)
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Consumer Price Index (2020=100)', fontsize=10)
plt.legend(loc='upper left')
plt.show()

plt.savefig("./Lecture_Figures_output/fig1.1_cpi.png")

########################################################################################################################
# 그림 1.2 소비자물가지수 상승률과 예적금 금리 비교

# 4.2.1.1 예금은행 가중평균금리 - 수신금리 - 신규취급액 기준 [005Y001] (1996.01 부터)
BOK_005Y001 = pd.read_pickle('./Market_Watch_Data/BOK_005Y001.pkl')
BOK_005Y001_01 = BOK_005Y001[BOK_005Y001["ITEM_CODE1"] == "BEABAA211"]  # 정기예금
BOK_005Y001_02 = BOK_005Y001[BOK_005Y001["ITEM_CODE1"] == "BEABAA212"]  # 정기적금

# 시각화: 월별 시계열 자료 3개를 같은 y 축으로 표시
fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
fig.set_size_inches(1800/300, 1200/300)  # 그래프 크기 지정, DPI=300

plt.plot(BOK_021Y126_00["DATETIME"], BOK_021Y126_00["pct_change_DATA_VALUE"], color='r', label="CPI Percent Changes (%)")
plt.plot(BOK_005Y001_01["DATETIME"], BOK_005Y001_01["DATA_VALUE"], color='b', label="Deposit Rate (%)")
plt.plot(BOK_005Y001_02["DATETIME"], BOK_005Y001_02["DATA_VALUE"], color='g', label="Savings Account Rate (%)")

xlim_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')
plt.xlim(xlim_start, )
plt.ylim(-1, 20)
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Rates (%)', fontsize=10)
plt.legend(loc='upper right')
plt.show()

plt.savefig("./Lecture_Figures_output/fig1.2_cpi_deposit_rates.png")


########################################################################################################################
# 그림 1.3 달러/원 환율
# 8.8.2.1 평균환율, 기말환율 > 주요국통화의 대원화 환율 통계자료 [036Y004][HY,MM,QQ,YY] (1964.05 부터)
BOK_036Y004 = pd.read_pickle('./Market_Watch_Data/BOK_036Y004.pkl')
BOK_036Y004_01 = BOK_036Y004[(BOK_036Y004["ITEM_CODE1"] == "0000001") & (BOK_036Y004["ITEM_CODE2"] == "0000200")]  # 원달러 환율 말일자료

# 시각화: 월별 시계열 자료 3개를 같은 y 축으로 표시
fig = plt.figure()
# fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
fig.set_size_inches(1800/300, 1200/300)  # 그래프 크기 지정, DPI=300

plt.plot(BOK_036Y004_01["DATETIME"], BOK_036Y004_01["DATA_VALUE"], color='b', label="USD/KRW")

xlim_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')
plt.xlim(xlim_start, )
plt.ylim(500, 1800)
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('USD/KRW', fontsize=10)
plt.legend(loc='upper right')
plt.show()

plt.savefig("./Lecture_Figures_output/fig1.3_exchange_rates.png")



