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

# 7.4.2 소비자물가지수(2015=100)(전국, 특수분류)  [021Y126][MM,QQ,YY] (1975.01 부터)
BOK021Y126 = pd.read_pickle('./BOK_raw/BOK021Y126.pkl')

BOK021Y126_00 = BOK021Y126[BOK021Y126["ITEM_CODE1"] == "00"].copy()  # 총지수
BOK021Y126_QB = BOK021Y126[BOK021Y126["ITEM_CODE1"] == "QB"].copy()  # 농산물및석유류제외지수 (근원 소비자물가지수)
BOK021Y126_00["pct_change_DATA_VALUE"] = (BOK021Y126_00["DATA_VALUE"].pct_change(12)) * 100  # 퍼센트 변화량 (전년비)
BOK021Y126_QB["pct_change_DATA_VALUE"] = (BOK021Y126_QB["DATA_VALUE"].pct_change(12)) * 100  # 퍼센트 변화량 (전년비)

# 시각화: 월별 시계열 자료 2개를 같은 y 축으로 표시
fig = plt.figure()
plt.plot(BOK021Y126_00["DATETIME"], BOK021Y126_00["pct_change_DATA_VALUE"], color='r', label="CPI")
plt.plot(BOK021Y126_QB["DATETIME"], BOK021Y126_QB["pct_change_DATA_VALUE"], color='g', label="Core CPI")

xlim_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')
plt.xlim(xlim_start, )
plt.ylim(-2, 12)
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Percentage Changes (%)', fontsize=10)
plt.legend(loc='upper left')
plt.show()

fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
plt.savefig("./BOK_processed/fig3.2_cpi_and_core_cpi_growth_rates.png")

########################################################################################################################
# 그림 3.3 소비자물가와 생산자물가 상승률 추이 (전년동기대비)

# 7.1.1 생산자물가지수(2015=100)(기본분류)  [013Y202][MM,QQ,YY] (1965.01 부터)
BOK013Y202 = pd.read_pickle('./BOK_raw/BOK013Y202.pkl')

BOK013Y202_AA = BOK013Y202[BOK013Y202["ITEM_CODE1"] == "*AA"].copy()  # 총지수
BOK013Y202_AA["pct_change_DATA_VALUE"] = (BOK013Y202_AA["DATA_VALUE"].pct_change(12)) * 100  # 퍼센트 변화량 (전년비)

# 시각화: 월별 시계열 자료 2개를 같은 y 축으로 표시
fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
plt.plot(BOK021Y126_00["DATETIME"], BOK021Y126_00["pct_change_DATA_VALUE"], color='r', label="CPI")
plt.plot(BOK013Y202_AA["DATETIME"], BOK013Y202_AA["pct_change_DATA_VALUE"], color='g', label="PPI")

xlim_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')
plt.xlim(xlim_start, )
plt.ylim(-5, 20)
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Percentage Changes (%)', fontsize=10)
plt.legend(loc='upper left')
plt.show()

plt.savefig("./BOK_processed/fig3.3_cpi_and_ppi_growth_rates.png")

########################################################################################################################
# 그림 3.4 GDP 갭과 물가상승률 추이

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

BOK111Y002_04 = BOK111Y002[BOK111Y002["ITEM_CODE1"] == "9010301"].copy()  # GDP 디플레이터 등락률 (%)
BOK111Y002_04["YYYYMMDD"] = BOK111Y002_04["TIME"] * 10000 + 101
BOK111Y002_04["DATETIME"] = pd.to_datetime(BOK111Y002_04['YYYYMMDD'].astype(str), errors='coerce', format='%Y%m%d')
BOK111Y002_04["GDP_Deflator_Changes"] = BOK111Y002_04["DATA_VALUE"].copy()  # GDP 디플레이터 등락률 (%)


# 시각화: 연도별 시계열 자료 2개를 같은 y 축으로 표시
fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300

plt.plot(BOK111Y002_00["DATETIME"], BOK111Y002_00["GDP_Gap"], color='r', label="GDP Gap")
plt.plot(BOK111Y002_04["DATETIME"], BOK111Y002_04["GDP_Deflator_Changes"], color='g', label="Changes in GDP Deflator")

xlim_start = pd.to_datetime("1970-01-01", errors='coerce', format='%Y-%m-%d')
plt.xlim(xlim_start, )
plt.ylim(-10, 35)
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Percentage Changes (%, %p)', fontsize=10)
plt.legend(loc='upper right')
plt.show()

plt.savefig("./BOK_processed/fig3.4_gdp_gap_and_changes_in_gdp_deflator.png")

########################################################################################################################
# 그림 3.5 GDP 갭과 제조업 생산능력 및 가동률 지수 추이

# KOSIS 제조업 생산능력 및 가동률지수 (2015=100, 계절조정) (1980.01 시작)
KOSIS_DT_1F31501 = pd.read_pickle('./BOK_raw/KOSIS_DT_1F31501.pkl')
KOSIS_DT_1F31501['DATA_VALUE_lag6'] = KOSIS_DT_1F31501['DATA_VALUE'].shift(6)  # lag

# KOSIS 제조업 평균가동률 (1980.01 시작)
KOSIS_DT_1F31502 = pd.read_pickle('./BOK_raw/KOSIS_DT_1F31502.pkl')
KOSIS_DT_1F31502['DATA_VALUE_lag6'] = KOSIS_DT_1F31502['DATA_VALUE'].shift(6)  # lag

# 그림: GDP 갭과 공장 가동률 지수 추이 비교
# 시각화: 월별 시계열 자료 2개를 서로 다른 y 축으로 표시하고 0 위치 통일
fig, ax1 = plt.subplots()
xlim_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')

# 첫번째 시계열
color1 = "tab:red"
ax1.set_xlabel("Dates")
ax1.set_ylabel("GDP Gap (%p)", color=color1)  # 데이터 레이블
ax1.plot(BOK111Y002_00["DATETIME"], BOK111Y002_00["GDP_Gap"], color=color1)
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
plt.savefig("./BOK_processed/fig3.5_gdp_gap_to_capicity_utilization_index.png")  # 그림 저장

########################################################################################################################
# 그림 3.6 소비자물가 상승률과 제조업 생산능력 및 가동률 지수 추이
# 시각화: 월별 시계열 자료 2개를 서로 다른 y 축으로 표시하고 0 위치 통일
fig, ax1 = plt.subplots()
xlim_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')

# 첫번째 시계열
color1 = "tab:red"
ax1.set_xlabel("Dates")
ax1.set_ylabel("CPI Growth (%)", color=color1)  # 데이터 레이블
ax1.plot(BOK021Y126_00["DATETIME"], BOK021Y126_00["pct_change_DATA_VALUE"], color=color1)
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
plt.savefig("./BOK_processed/fig3.6_cpi_growth_to_capicity_utilization_index.png")  # 그림 저장

########################################################################################################################
# 그림 3.7 소비자물가 상승률과 환율변동
# 8.8.2.1 평균환율, 기말환율 > 주요국통화의 대원화 환율 통계자료 [036Y004][HY,MM,QQ,YY] (1964.05 부터)
BOK036Y004 = pd.read_pickle('./BOK_raw/BOK036Y004.pkl')
BOK036Y004_01 = BOK036Y004[(BOK036Y004["ITEM_CODE1"] == "0000001") & (BOK036Y004["ITEM_CODE2"] == "0000200")].copy()  # 원/미국달러 말일자료
BOK036Y004_01["pct_change_DATA_VALUE"] = (BOK036Y004_01["DATA_VALUE"].pct_change(12)) * 100  # 퍼센트 변화량 (전년비)

# 시각화: 월별 시계열 자료 2개를 서로 다른 y 축으로 표시하고 0 위치 통일
fig, ax1 = plt.subplots()
xlim_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')

# 첫번째 시계열
color1 = "tab:red"
ax1.set_xlabel("Dates")
ax1.set_ylabel("CPI Growth (%)", color=color1)  # 데이터 레이블
ax1.plot(BOK021Y126_00["DATETIME"], BOK021Y126_00["pct_change_DATA_VALUE"], color=color1)
ax1.tick_params(axis="y")

# 두번째 시계열
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color2 = "tab:blue"
ax2.set_ylabel("Percentage Change in Exchange Rate (%)", color=color2)  # 데이터 레이블
ax2.plot(BOK036Y004_01["DATETIME"], BOK036Y004_01["pct_change_DATA_VALUE"], color=color2, linestyle='-')
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
plt.savefig("./BOK_processed/fig3.7_cpi_growth_to_exchange_rate_change.png")  # 그림 저장



