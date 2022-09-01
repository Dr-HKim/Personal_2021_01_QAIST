# 5강 인플레이션
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
# 그림 3.2 소비자물가지수와 근원소비자물가지수 상승률 추이 비교

# 4.2.1 소비자물가지수(2020=100)(전국, 특수분류) [901Y010][A,M,Q] (1975.01 부터)
BOK_901Y010 = pd.read_pickle('./Market_Watch_Data/BOK_901Y010.pkl')
BOK_901Y010_00 = BOK_901Y010[BOK_901Y010["ITEM_CODE1"] == "00"].copy()  # 총지수
BOK_901Y010_QB = BOK_901Y010[BOK_901Y010["ITEM_CODE1"] == "QB"].copy()  # 농산물및석유류제외지수 (근원 소비자물가지수)
BOK_901Y010_00["pct_change_DATA_VALUE"] = (BOK_901Y010_00["DATA_VALUE"].pct_change(12)) * 100  # 퍼센트 변화량 (전년비)
BOK_901Y010_QB["pct_change_DATA_VALUE"] = (BOK_901Y010_QB["DATA_VALUE"].pct_change(12)) * 100  # 퍼센트 변화량 (전년비)

# 시각화: 월별 시계열 자료 2개를 같은 y 축으로 표시
fig = plt.figure()
plt.plot(BOK_901Y010_00["DATETIME"], BOK_901Y010_00["pct_change_DATA_VALUE"], color='r', label="CPI")
plt.plot(BOK_901Y010_QB["DATETIME"], BOK_901Y010_QB["pct_change_DATA_VALUE"], color='g', label="Core CPI")

xlim_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')
plt.xlim(xlim_start, )
plt.ylim(-2, 12)
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Percentage Changes (%)', fontsize=10)
plt.legend(loc='upper left')
plt.show()

fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
plt.savefig("./Lecture_Figures_output/fig3.2_cpi_and_core_cpi_growth_rates.png")

########################################################################################################################
# 그림 3.3 소비자물가와 생산자물가 상승률 추이 (전년동기대비)

# 4.1.1.1. 생산자물가지수(2015=100)(기본분류) [404Y014][A,M,Q] (1965.01 부터) (1910~1964 자료는 따로 있음)
# 총지수의 경우 1993.08 이전 몇년간 자료 없음
BOK_404Y014 = pd.read_pickle('./Market_Watch_Data/BOK_404Y014.pkl')
BOK_404Y014_AA = BOK_404Y014[(BOK_404Y014["ITEM_CODE1"] == "*AA") & (BOK_404Y014["TIME"] > 199300)].copy()  # 총지수
BOK_404Y014_AA["pct_change_DATA_VALUE"] = (BOK_404Y014_AA["DATA_VALUE"].pct_change(12)) * 100  # 퍼센트 변화량 (전년비)

# 시각화: 월별 시계열 자료 2개를 같은 y 축으로 표시
fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
plt.plot(BOK_901Y010_00["DATETIME"], BOK_901Y010_00["pct_change_DATA_VALUE"], color='r', label="CPI")  # 소비자물가지수
plt.plot(BOK_404Y014_AA["DATETIME"], BOK_404Y014_AA["pct_change_DATA_VALUE"], color='g', label="PPI")  # 생산자물가지수

xlim_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')
plt.xlim(xlim_start, )
plt.ylim(-5, 20)
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Percentage Changes (%)', fontsize=10)
plt.legend(loc='upper left')
plt.show()

plt.savefig("./Lecture_Figures_output/fig3.3_cpi_and_ppi_growth_rates.png")

########################################################################################################################
# 그림 3.4 GDP 갭과 물가상승률 추이

# 2.1.1.1. 국민소득통계(2015년 기준년) > 주요지표 > 주요지표(연간지표) [200Y001][A] (1953 부터)
BOK_200Y001 = pd.read_pickle('./Market_Watch_Data/BOK_200Y001.pkl')

# GDP 갭 계산
BOK_200Y001_00 = BOK_200Y001[BOK_200Y001["ITEM_CODE1"] == "10101"].copy()  # 국내총생산(GDP)(명목, 십억원)
BOK_200Y001_00["YYYYMMDD"] = BOK_200Y001_00["TIME"] * 10000 + 101
BOK_200Y001_00["DATETIME"] = pd.to_datetime(BOK_200Y001_00['YYYYMMDD'].astype(str), errors='coerce', format='%Y%m%d')
BOK_200Y001_00["GDP"] = BOK_200Y001_00["DATA_VALUE"].copy() * 1000000000  # 국내총생산(GDP)(명목, 원)
BOK_200Y001_00["Actual_GDP"] = BOK_200Y001_00["DATA_VALUE"].copy()  # 국내총생산(GDP)(명목, 십억원)

BOK_200Y001_03 = BOK_200Y001[BOK_200Y001["ITEM_CODE1"] == "90103"].copy()  # GDP 디플레이터 (2015=100)
BOK_200Y001_03["YYYYMMDD"] = BOK_200Y001_03["TIME"] * 10000 + 101
BOK_200Y001_03["DATETIME"] = pd.to_datetime(BOK_200Y001_03['YYYYMMDD'].astype(str), errors='coerce', format='%Y%m%d')
BOK_200Y001_03["GDP_Deflator"] = BOK_200Y001_03["DATA_VALUE"].copy()  # GDP 디플레이터 (2015=100)

BOK_200Y001_00 = pd.merge(BOK_200Y001_00, BOK_200Y001_03[["DATETIME", "GDP_Deflator"]], left_on='DATETIME', right_on='DATETIME', how='left')
BOK_200Y001_00["Real_GDP"] = BOK_200Y001_00["Actual_GDP"] / BOK_200Y001_00["GDP_Deflator"]
cycle, trend = sm.tsa.filters.hpfilter(BOK_200Y001_00["Real_GDP"], 100)  # 람다=100 으로 놓는게 중요 (경험치...)
BOK_200Y001_00["Potential_GDP"] = trend
BOK_200Y001_00["GDP_Gap"] = ((BOK_200Y001_00["Real_GDP"] - BOK_200Y001_00["Potential_GDP"]) / BOK_200Y001_00["Potential_GDP"]) * 100  # GDP 갭 (%)

BOK_200Y001_01 = BOK_200Y001[BOK_200Y001["ITEM_CODE1"] == "1010101"].copy()  # 국내총생산(GDP)(명목, 억달러)
BOK_200Y001_01["YYYYMMDD"] = BOK_200Y001_01["TIME"] * 10000 + 101
BOK_200Y001_01["DATETIME"] = pd.to_datetime(BOK_200Y001_01['YYYYMMDD'].astype(str), errors='coerce', format='%Y%m%d')
BOK_200Y001_01["GDP"] = BOK_200Y001_01["DATA_VALUE"].copy() * 100000000  # 국내총생산(GDP)(명목, 달러)
BOK_200Y001_01["Actual_GDP"] = BOK_200Y001_01["DATA_VALUE"].copy()  # 국내총생산(GDP)(명목, 억달러)

BOK_200Y001_04 = BOK_200Y001[BOK_200Y001["ITEM_CODE1"] == "9010301"].copy()  # GDP 디플레이터 등락률 (%)
BOK_200Y001_04["YYYYMMDD"] = BOK_200Y001_04["TIME"] * 10000 + 101
BOK_200Y001_04["DATETIME"] = pd.to_datetime(BOK_200Y001_04['YYYYMMDD'].astype(str), errors='coerce', format='%Y%m%d')
BOK_200Y001_04["GDP_Deflator_Changes"] = BOK_200Y001_04["DATA_VALUE"].copy()  # GDP 디플레이터 등락률 (%)


# 시각화: 연도별 시계열 자료 2개를 같은 y 축으로 표시
fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300

plt.plot(BOK_200Y001_00["DATETIME"], BOK_200Y001_00["GDP_Gap"], color='r', label="GDP Gap")
plt.plot(BOK_200Y001_04["DATETIME"], BOK_200Y001_04["GDP_Deflator_Changes"], color='g', label="Changes in GDP Deflator")

xlim_start = pd.to_datetime("1970-01-01", errors='coerce', format='%Y-%m-%d')
plt.xlim(xlim_start, )
plt.ylim(-10, 35)
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Percentage Changes (%, %p)', fontsize=10)
plt.legend(loc='upper right')
plt.show()

plt.savefig("./Lecture_Figures_output/fig3.4_gdp_gap_and_changes_in_gdp_deflator.png")

########################################################################################################################
# 그림 3.5 GDP 갭과 제조업 생산능력 및 가동률 지수 추이

# KOSIS 제조업 생산능력 및 가동률지수 (2015=100, 계절조정) (1980.01 시작)
KOSIS_DT_1F31501 = pd.read_pickle('./Market_Watch_Data/KOSIS_DT_1F31501.pkl')
KOSIS_DT_1F31501['DATA_VALUE_lag6'] = KOSIS_DT_1F31501['DATA_VALUE'].shift(6)  # lag

# KOSIS 제조업 평균가동률 (1980.01 시작)
KOSIS_DT_1F31502 = pd.read_pickle('./Market_Watch_Data/KOSIS_DT_1F31502.pkl')
KOSIS_DT_1F31502['DATA_VALUE_lag6'] = KOSIS_DT_1F31502['DATA_VALUE'].shift(6)  # lag

# 그림: GDP 갭과 공장 가동률 지수 추이 비교
# 시각화: 월별 시계열 자료 2개를 서로 다른 y 축으로 표시하고 0 위치 통일
fig, ax1 = plt.subplots()
xlim_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')

# 첫번째 시계열
color1 = "tab:red"
ax1.set_xlabel("Dates")
ax1.set_ylabel("GDP Gap (%p)", color=color1)  # 데이터 레이블
ax1.plot(BOK_200Y001_00["DATETIME"], BOK_200Y001_00["GDP_Gap"], color=color1)
ax1.tick_params(axis="y")

# 두번째 시계열
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color2 = "tab:blue"
ax2.set_ylabel("Manufacturing Capacity Utilization Index (2015=100)", color=color2)  # 데이터 레이블
ax2.plot(KOSIS_DT_1F31501["DATETIME"], KOSIS_DT_1F31501["DATA_VALUE"], color=color2, linestyle='-')
ax2.tick_params(axis='y')

# 그래프 기타 설정
fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
# ax1.set_ylim([0, 12])
# ax2.set_ylim([60, 85])
# align_yaxis(ax1, 0, ax2, 0)  # 두 축이 동일한 0 값을 가지도록 조정
# plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlim(xlim_start, )
plt.show()
plt.savefig("./Lecture_Figures_output/fig3.5_gdp_gap_to_capicity_utilization_index.png")  # 그림 저장

########################################################################################################################
# 그림 3.6 소비자물가 상승률과 제조업 생산능력 및 가동률 지수 추이
# 시각화: 월별 시계열 자료 2개를 서로 다른 y 축으로 표시하고 0 위치 통일
fig, ax1 = plt.subplots()
xlim_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')

# 첫번째 시계열
color1 = "tab:red"
ax1.set_xlabel("Dates")
ax1.set_ylabel("CPI Growth (%)", color=color1)  # 데이터 레이블
ax1.plot(BOK_901Y010_00["DATETIME"], BOK_901Y010_00["pct_change_DATA_VALUE"], color=color1)  # 소비자물가지수
ax1.tick_params(axis="y")

# 두번째 시계열
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color2 = "tab:blue"
ax2.set_ylabel("Manufacturing Capacity Utilization Index (2015=100, 6 months lagged)", color=color2)  # 데이터 레이블
ax2.plot(KOSIS_DT_1F31501["DATETIME"], KOSIS_DT_1F31501["DATA_VALUE_lag6"], color=color2, linestyle='-')
ax2.tick_params(axis='y')

# 그래프 기타 설정
fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
# ax1.set_ylim([0, 12])
# ax2.set_ylim([60, 85])
# align_yaxis(ax1, 0, ax2, 0)  # 두 축이 동일한 0 값을 가지도록 조정
# plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlim(xlim_start, )
plt.show()
plt.savefig("./Lecture_Figures_output/fig3.6_cpi_growth_to_capicity_utilization_index.png")  # 그림 저장

########################################################################################################################
# 그림 3.7 소비자물가 상승률과 환율변동
# 3.1.2.1. 평균환율/기말환율 > 주요국통화의 대원화 환율 [731Y004][A,M,Q,S] (1964.05 부터)
BOK_731Y004 = pd.read_pickle('./Market_Watch_Data/BOK_731Y004.pkl')
BOK_731Y004_01 = BOK_731Y004[(BOK_731Y004["ITEM_CODE1"] == "0000001") & (BOK_731Y004["ITEM_CODE2"] == "0000200")].copy()  # 원/미국달러 말일자료
BOK_731Y004_01["pct_change_DATA_VALUE"] = (BOK_731Y004_01["DATA_VALUE"].pct_change(12)) * 100  # 퍼센트 변화량 (전년비)

# 시각화: 월별 시계열 자료 2개를 서로 다른 y 축으로 표시하고 0 위치 통일
fig, ax1 = plt.subplots()
xlim_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')

# 첫번째 시계열
color1 = "tab:red"
ax1.set_xlabel("Dates")
ax1.set_ylabel("CPI Growth (%)", color=color1)  # 데이터 레이블
ax1.plot(BOK_901Y010_00["DATETIME"], BOK_901Y010_00["pct_change_DATA_VALUE"], color=color1)  # 소비자물가지수
ax1.tick_params(axis="y")

# 두번째 시계열
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color2 = "tab:blue"
ax2.set_ylabel("Percentage Change in Exchange Rate (%)", color=color2)  # 데이터 레이블
ax2.plot(BOK_731Y004_01["DATETIME"], BOK_731Y004_01["pct_change_DATA_VALUE"], color=color2, linestyle='-')
ax2.tick_params(axis='y')

# 그래프 기타 설정
fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
# ax1.set_ylim([0, 12])
# ax2.set_ylim([60, 85])
# align_yaxis(ax1, 0, ax2, 0)  # 두 축이 동일한 0 값을 가지도록 조정
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlim(xlim_start, )
plt.show()
plt.savefig("./Lecture_Figures_output/fig3.7_cpi_growth_to_exchange_rate_change.png")  # 그림 저장
