# 6강 경상수지
# Created by Ki Hyeongjun on 01/19/2021.
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


def get_yyyymm_add_months(n_yyyymm, n_months):
    n_yyyy, n_mm = divmod(n_yyyymm, 100)
    n_months_y, n_months_m = divmod(n_mm + n_months - 1, 12)
    output_yyyy = n_yyyy + n_months_y
    output_mm = n_months_m + 1
    output_yyyymm = output_yyyy * 100 + output_mm
    return output_yyyymm

########################################################################################################################
# 그림 4.1 GDP 대비 경상수지와 GDP 갭 (%)
# 10.1.1 국민계정(2015년 기준년) - 주요지표 - 연간지표 [111Y002][YY] (1953 부터)
BOK_111Y002 = pd.read_pickle('./Market_Watch_Data/BOK_111Y002.pkl')

# GDP 갭 계산
BOK_111Y002_00 = BOK_111Y002[BOK_111Y002["ITEM_CODE1"] == "10101"].copy()  # 국내총생산(GDP)(명목, 십억원)
BOK_111Y002_00["YYYYMMDD"] = BOK_111Y002_00["TIME"] * 10000 + 101
BOK_111Y002_00["DATETIME"] = pd.to_datetime(BOK_111Y002_00['YYYYMMDD'].astype(str), errors='coerce', format='%Y%m%d')
BOK_111Y002_00["GDP"] = BOK_111Y002_00["DATA_VALUE"].copy() * 1000000000  # 국내총생산(GDP)(명목, 원)
BOK_111Y002_00["Actual_GDP"] = BOK_111Y002_00["DATA_VALUE"].copy()  # 국내총생산(GDP)(명목, 십억원)

BOK_111Y002_03 = BOK_111Y002[BOK_111Y002["ITEM_CODE1"] == "90103"].copy()  # GDP 디플레이터 (2015=100)
BOK_111Y002_03["YYYYMMDD"] = BOK_111Y002_03["TIME"] * 10000 + 101
BOK_111Y002_03["DATETIME"] = pd.to_datetime(BOK_111Y002_03['YYYYMMDD'].astype(str), errors='coerce', format='%Y%m%d')
BOK_111Y002_03["GDP_Deflator"] = BOK_111Y002_03["DATA_VALUE"].copy()  # GDP 디플레이터 (2015=100)

BOK_111Y002_00 = pd.merge(BOK_111Y002_00, BOK_111Y002_03[["DATETIME", "GDP_Deflator"]], left_on='DATETIME', right_on='DATETIME', how='left')
BOK_111Y002_00["Real_GDP"] = BOK_111Y002_00["Actual_GDP"] / BOK_111Y002_00["GDP_Deflator"]
cycle, trend = sm.tsa.filters.hpfilter(BOK_111Y002_00["Real_GDP"], 100)  # 람다=100 으로 놓는게 중요 (경험치...)
BOK_111Y002_00["Potential_GDP"] = trend
BOK_111Y002_00["GDP_Gap"] = ((BOK_111Y002_00["Real_GDP"] - BOK_111Y002_00["Potential_GDP"]) / BOK_111Y002_00["Potential_GDP"]) * 100  # GDP 갭 (%)

BOK_111Y002_01 = BOK_111Y002[BOK_111Y002["ITEM_CODE1"] == "1010101"].copy()  # 국내총생산(GDP)(명목, 억달러)
BOK_111Y002_01["YYYYMMDD"] = BOK_111Y002_01["TIME"] * 10000 + 101
BOK_111Y002_01["DATETIME"] = pd.to_datetime(BOK_111Y002_01['YYYYMMDD'].astype(str), errors='coerce', format='%Y%m%d')
BOK_111Y002_01["GDP"] = BOK_111Y002_01["DATA_VALUE"].copy() * 100000000  # 국내총생산(GDP)(명목, 달러)
BOK_111Y002_01["Actual_GDP"] = BOK_111Y002_01["DATA_VALUE"].copy()  # 국내총생산(GDP)(명목, 억달러)

# GDP 대비 경상수지 계산
# 8.1.1 국제수지 [022Y013][MM,QQ,YY] (1980.01, 1980Q1 부터)
BOK_022Y013 = pd.read_pickle('./Market_Watch_Data/BOK_022Y013.pkl')

BOK_022Y013_00 = BOK_022Y013[BOK_022Y013["ITEM_CODE1"] == "000000"].copy()  # 경상수지 (백만달러)
BOK_022Y013_00["Current_Account"] = BOK_022Y013_00["DATA_VALUE"].copy() * 1000000  # 경상수지(current account) (달러)
BOK_022Y013_00["Current_Account"] = BOK_022Y013_00["Current_Account"].rolling(window=12).sum()  # 경상수지 12개월 누적

df_CA_to_GDP = pd.merge(BOK_022Y013_00, BOK_111Y002_01[["DATETIME", "GDP"]], left_on='DATETIME', right_on='DATETIME', how='left')
df_CA_to_GDP["GDP"] = df_CA_to_GDP["GDP"].fillna(method='ffill')
df_CA_to_GDP["CA_to_GDP"] = df_CA_to_GDP["Current_Account"] / df_CA_to_GDP["GDP"] * 100  # GDP 대비 경상수지 (%)

# 그림 4.1 GDP 대비 경상수지와 GDP 갭 (%)
# 시각화: 월별 시계열 자료 1개를 표시
fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300

plt.plot(df_CA_to_GDP["DATETIME"], df_CA_to_GDP["CA_to_GDP"], color='r', label="Current Account to GDP")
plt.plot(BOK_111Y002_00["DATETIME"], BOK_111Y002_00["GDP_Gap"], color='g', label="GDP Gap")

xlim_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')
plt.xlim(xlim_start, )
plt.ylim(-10, 15)
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Percentage (%)', fontsize=10)
plt.legend(loc='upper left')
plt.show()

plt.savefig("./Lecture_Figures_output/fig4.1_current_account_to_gdp_and_gdp_gap.png")


########################################################################################################################
# 그림 4.2 GDP 대비 경상수지와 저축률 (%)

# GDP 대비 경상수지 계산

# 10.1.1 국민계정(2015년 기준년) - 주요지표 - 연간지표 [111Y002][YY] (1953 부터)
BOK_111Y002 = pd.read_pickle('./Market_Watch_Data/BOK_111Y002.pkl')
BOK_111Y002_01 = BOK_111Y002[BOK_111Y002["ITEM_CODE1"] == "1010101"].copy()  # 국내총생산(GDP)(명목, 억달러)
BOK_111Y002_01["YYYYMMDD"] = BOK_111Y002_01["TIME"] * 10000 + 101
BOK_111Y002_01["DATETIME"] = pd.to_datetime(BOK_111Y002_01['YYYYMMDD'].astype(str), errors='coerce', format='%Y%m%d')
BOK_111Y002_01["GDP"] = BOK_111Y002_01["DATA_VALUE"].copy() * 100000000  # 국내총생산(GDP)(명목, 달러)
BOK_111Y002_01["Actual_GDP"] = BOK_111Y002_01["DATA_VALUE"].copy()  # 국내총생산(GDP)(명목, 억달러)

# 8.1.1 국제수지 [022Y013][MM,QQ,YY] (1980.01, 1980Q1 부터)
BOK_022Y013 = pd.read_pickle('./Market_Watch_Data/BOK_022Y013.pkl')
BOK_022Y013_00 = BOK_022Y013[BOK_022Y013["ITEM_CODE1"] == "000000"].copy()  # 경상수지 (백만달러)
BOK_022Y013_00["Current_Account"] = BOK_022Y013_00["DATA_VALUE"].copy() * 1000000  # 경상수지(current account) (달러)
BOK_022Y013_00["Current_Account"] = BOK_022Y013_00["Current_Account"].rolling(window=12).sum()  # 경상수지 12개월 누적

df_CA_to_GDP = pd.merge(BOK_022Y013_00, BOK_111Y002_01[["DATETIME", "GDP"]], left_on='DATETIME', right_on='DATETIME', how='left')
df_CA_to_GDP["GDP"] = df_CA_to_GDP["GDP"].fillna(method='ffill')
df_CA_to_GDP["CA_to_GDP"] = df_CA_to_GDP["Current_Account"] / df_CA_to_GDP["GDP"] * 100  # GDP 대비 경상수지 (%)


BOK_111Y002_02 = BOK_111Y002[BOK_111Y002["ITEM_CODE1"] == "8010400"].copy()  # 가계순저축률 (%)
BOK_111Y002_02["YYYYMMDD"] = BOK_111Y002_02["TIME"] * 10000 + 1231
BOK_111Y002_02["DATETIME"] = pd.to_datetime(BOK_111Y002_02['YYYYMMDD'].astype(str), errors='coerce', format='%Y%m%d')

# 그림 4.2 GDP 대비 경상수지와 가계순저축률 (%)
# 시각화: 월별 시계열 자료 1개를 표시
fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300

plt.plot(df_CA_to_GDP["DATETIME"], df_CA_to_GDP["CA_to_GDP"], color='r', label="Current Account to GDP (%)")
plt.plot(BOK_111Y002_02["DATETIME"], BOK_111Y002_02["DATA_VALUE"], color='g', label="Households Net Saving Ratio (%)")

xlim_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')
plt.xlim(xlim_start, )
plt.ylim(-10, 30)
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Percentage (%)', fontsize=10)
plt.legend(loc='upper left')
plt.show()

plt.savefig("./Lecture_Figures_output/fig4.2_current_account_to_gdp_and_households_net_saving_ratio.png")


########################################################################################################################
# 그림 4.4 실질실효환율과 경상수지 추이

# BIS 실질실효환율(real effective exchange rate) 데이터 불러오기
df_bis_data = pd.read_excel(
    './Market_Watch_Data/BIS_Effective_Exchange_Rates.xlsx', sheet_name="Real", header=None, skiprows=5, skipfooter=0)
df_bis_header = pd.read_excel(
    './Market_Watch_Data/BIS_Effective_Exchange_Rates.xlsx', sheet_name="Real", header=None, skiprows=3, nrows=1)
df_bis_header[0] = "DATETIME"
df_bis_header = df_bis_header.transpose()
df_bis_header = df_bis_header[0].tolist()
df_bis_data.columns = df_bis_header
df_bis_data["Korea_100"] = df_bis_data["Korea"] - 100

# 8.1.1 국제수지 [022Y013][MM,QQ,YY] (1980.01, 1980Q1 부터)
BOK_022Y013 = pd.read_pickle('./Market_Watch_Data/BOK_022Y013.pkl')
BOK_022Y013_00 = BOK_022Y013[BOK_022Y013["ITEM_CODE1"] == "000000"].copy()  # 경상수지 (백만달러)
BOK_022Y013_00["Current_Account"] = BOK_022Y013_00["DATA_VALUE"].copy() / 1000  # 경상수지(current account) (십억 달러)
BOK_022Y013_00["Current_Account"] = BOK_022Y013_00["Current_Account"].rolling(window=12).sum()  # 경상수지 12개월 누적


# 그림 4.4 실질실효환율과 경상수지 추이
# 시각화: 월별 시계열 자료 2개를 서로 다른 y 축으로 표시하고 0 위치 통일
fig, ax1 = plt.subplots()
xlim_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')

# 첫번째 시계열
color1 = "tab:red"
ax1.set_xlabel("Dates")
ax1.set_ylabel("Real Effective Exchange Rates (%)", color=color1)  # 데이터 레이블
ax1.plot(df_bis_data["DATETIME"], df_bis_data["Korea_100"], color=color1)
ax1.tick_params(axis="y")

# 두번째 시계열
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color2 = "tab:blue"
ax2.set_ylabel("Current Account (billion dollars)", color=color2)  # 데이터 레이블
ax2.plot(BOK_022Y013_00["DATETIME"], BOK_022Y013_00["Current_Account"], color=color2, linestyle='-')
ax2.tick_params(axis='y')

# 그래프 기타 설정
fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
ax1.set_ylim([-30, 35])
ax2.set_ylim([-90, 120])
align_yaxis(ax1, 0, ax2, 0)  # 두 축이 동일한 0 값을 가지도록 조정
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlim(xlim_start, )
plt.show()
plt.savefig("./Lecture_Figures_output/fig4.4_real_effective_exchange_rates_and_current_account.png")  # 그림 저장



########################################################################################################################
# 그림 4.5 OECD 경기선행지수 (Composite Leading Indicators)
# 데이터 불러오기
OECD_MONTHLY = pd.read_pickle('./Market_Watch_Data/oecd_monthly.pkl')

# YYYYMM 을 기준으로 그 달의 가장 마지막 날짜 입력
OECD_MONTHLY["DATETIME"] = pd.to_datetime(
    get_yyyymm_add_months(OECD_MONTHLY["yyyymm"], 1) * 100 + 1, errors='coerce', format='%Y%m%d') + pd.Timedelta(days=-1)

# LOLITOTR_GYSA: 12-month rate of change of the trend restored CLI
# LOLITONO: Normalised (CLI)
# LOLITOAA: Amplitude adjusted (CLI)
# 장기 추세를 제거하고 최근 수치에 가중치를 두는 방식으로 진폭조정된(Amplitude adjusted) CLI
# 100이 넘으면 경기 상승, 100을 밑돌면 경기 하강
df_oecd_cli = OECD_MONTHLY[(OECD_MONTHLY["location_id"] == "OECD") & (OECD_MONTHLY["subject_id"] == "LOLITOAA")].copy()
df_korea_cli = OECD_MONTHLY[(OECD_MONTHLY["location_id"] == "KOR") & (OECD_MONTHLY["subject_id"] == "LOLITOAA")].copy()

# 그림 4.5 OECD 경기선행지수 (Composite Leading Indicators)
# 시각화: 월별 시계열 자료 1개를 표시
fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300

plt.plot(df_oecd_cli["DATETIME"], df_oecd_cli["datavalue"], color='r', label="OECD Composite Leading Indicators")
plt.plot(df_korea_cli["DATETIME"], df_korea_cli["datavalue"], color='g', label="Korea Composite Leading Indicators")

xlim_start = pd.to_datetime("2000-01-01", errors='coerce', format='%Y-%m-%d')
plt.xlim(xlim_start, )
# plt.ylim(-1, 7)
plt.axhline(y=100, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Composite Leading Indicators', fontsize=10)
plt.legend(loc='upper right')
plt.show()

plt.savefig("./Lecture_Figures_output/fig4.5_composite_leading_indicators_oecd_kor.png")  # 그림 저장

########################################################################################################################
# 그림 4.7 한국은행 기준금리와 소비자물가지수 상승률 (%)
# 2.6 한국은행 기준금리 및 여수신금리 [098Y001][DD, MM, QQ, YY] (1994.01.03 부터)
BOK_098Y001_DD = pd.read_pickle('./Market_Watch_Data/BOK_098Y001_DD.pkl')
BOK_098Y001_DD_01 = BOK_098Y001_DD[BOK_098Y001_DD["ITEM_CODE1"] == "0101000"].copy()  # 한국은행 기준금리

# 7.4.2 소비자물가지수(2020=100)(전국, 특수분류)  [021Y126][MM,QQ,YY] (1975.01 부터)
BOK_021Y126 = pd.read_pickle('./Market_Watch_Data/BOK_021Y126.pkl')
BOK_021Y126_00 = BOK_021Y126[BOK_021Y126["ITEM_CODE1"] == "00"].copy()  # 총지수
BOK_021Y126_00["pct_change_DATA_VALUE"] = (BOK_021Y126_00["DATA_VALUE"].pct_change(12)) * 100  # 퍼센트 변화량 (전년비)

# 그림 4.7 한국은행 기준금리와 소비자물가지수 상승률 (%)
# 시각화: 월별 시계열 자료 1개를 표시
fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300

plt.plot(BOK_098Y001_DD_01["DATETIME"], BOK_098Y001_DD_01["DATA_VALUE"], color='r', label="BOK_ Base Rate (%)")
plt.plot(BOK_021Y126_00["DATETIME"], BOK_021Y126_00["pct_change_DATA_VALUE"], color='g', label="CPI Percent Changes (%)")

xlim_start = pd.to_datetime("2000-01-01", errors='coerce', format='%Y-%m-%d')
plt.xlim(xlim_start, )
plt.ylim(-1, 7)
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Percentage (%)', fontsize=10)
plt.legend(loc='upper left')
plt.show()

plt.savefig("./Lecture_Figures_output/fig4.7_bok_base_rate_and_cpi_percent_changes.png")  # 그림 저장


########################################################################################################################
# 그림 4.8 경상수지와 코스피 지수

# 8.1.1 국제수지 [022Y013][MM,QQ,YY] (1980.01, 1980Q1 부터)
BOK_022Y013 = pd.read_pickle('./Market_Watch_Data/BOK_022Y013.pkl')
BOK_022Y013_00 = BOK_022Y013[BOK_022Y013["ITEM_CODE1"] == "000000"].copy()  # 경상수지 (백만달러)
BOK_022Y013_00["Current_Account_3M"] = BOK_022Y013_00["DATA_VALUE"].rolling(window=3).sum() / 1000  # 경상수지 3개월 누적 (십억달러)
BOK_022Y013_00["Current_Account_12M"] = BOK_022Y013_00["DATA_VALUE"].rolling(window=12).sum() / 1000  # 경상수지 12개월 누적 (십억달러)
BOK_022Y013_00["Current_Account_cum"] = BOK_022Y013_00["DATA_VALUE"].cumsum() / 1000  # 경상수지 누적 (십억달러)

# 코스피지수
investpy_kospi = pd.read_pickle('./Market_Watch_Data/investpy_kospi.pkl')
investpy_kospi_monthly = investpy_kospi.resample('M').last()

# 그림 4.8 경상수지와 코스피 지수
# 시각화: 월별 시계열 자료 2개를 서로 다른 y 축으로 표시하고 0 위치 통일
fig, ax1 = plt.subplots()
xlim_start = pd.to_datetime("2000-01-01", errors='coerce', format='%Y-%m-%d')

# 첫번째 시계열
color1 = "tab:red"
ax1.set_xlabel("Dates")
ax1.set_ylabel("Current Account (12 months cumulative)", color=color1)  # 데이터 레이블
ax1.plot(BOK_022Y013_00["DATETIME"], BOK_022Y013_00["Current_Account_12M"], color=color1)
ax1.tick_params(axis="y")

# 두번째 시계열
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color2 = "tab:blue"
ax2.set_ylabel("KOSPI", color=color2)  # 데이터 레이블
ax2.plot(investpy_kospi_monthly.index, investpy_kospi_monthly["Close"], color=color2, linestyle='-')
ax2.tick_params(axis='y')

# 그래프 기타 설정
fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
ax1.set_ylim([-10, 120])
ax2.set_ylim([0, 3500])
# align_yaxis(ax1, 0, ax2, 0)  # 두 축이 동일한 0 값을 가지도록 조정
# plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlim(xlim_start, )
plt.show()

plt.savefig("./Lecture_Figures_output/fig4.8_current_account_and_kospi.png")  # 그림 저장


########################################################################################################################
# 그림 4.9 실질실효환율과 달러/원 환율 추이

# BIS 실질실효환율(real effective exchange rate) 데이터 불러오기
df_bis_data = pd.read_excel(
    './Market_Watch_Data/BIS_Effective_Exchange_Rates.xlsx', sheet_name="Real", header=None, skiprows=5, skipfooter=0)
df_bis_header = pd.read_excel(
    './Market_Watch_Data/BIS_Effective_Exchange_Rates.xlsx', sheet_name="Real", header=None, skiprows=3, nrows=1)
df_bis_header[0] = "DATETIME"
df_bis_header = df_bis_header.transpose()
df_bis_header = df_bis_header[0].tolist()
df_bis_data.columns = df_bis_header
df_bis_data["Korea_100"] = df_bis_data["Korea"] - 100

# 8.8.2.1 평균환율, 기말환율 > 주요국통화의 대원화 환율 통계자료 [036Y004][HY,MM,QQ,YY] (1964.05 부터)
BOK_036Y004 = pd.read_pickle('./Market_Watch_Data/BOK_036Y004.pkl')
BOK_036Y004_00 = BOK_036Y004[(BOK_036Y004["ITEM_CODE1"] == "0000001") & (BOK_036Y004["ITEM_CODE2"] == "0000200")].copy()  # 원달러환율 말일자료

# 그림 4.4 실질실효환율과 경상수지 추이
# 시각화: 월별 시계열 자료 2개를 서로 다른 y 축으로 표시하고 0 위치 통일
fig, ax1 = plt.subplots()
xlim_start = pd.to_datetime("2000-01-01", errors='coerce', format='%Y-%m-%d')

# 첫번째 시계열
color1 = "tab:red"
ax1.set_ylabel("USD/KRW", color=color1)  # 데이터 레이블
ax1.plot(BOK_036Y004_00["DATETIME"], BOK_036Y004_00["DATA_VALUE"], color=color1, linestyle='-')
ax1.tick_params(axis='y')

# 두번째 시계열
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color2 = "tab:blue"
ax2.set_ylabel("Real Effective Exchange Rates (%)", color=color2)  # 데이터 레이블
ax2.set_xlabel("Dates")
ax2.plot(df_bis_data["DATETIME"], df_bis_data["Korea_100"], color=color2)
ax2.tick_params(axis="y")

# 그래프 기타 설정
fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
ax1.set_ylim([800, 1600])
ax2.set_ylim([-40, 40])
# align_yaxis(ax1, 0, ax2, 0)  # 두 축이 동일한 0 값을 가지도록 조정
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlim(xlim_start, )
plt.show()
plt.savefig("./Lecture_Figures_output/fig4.9_real_effective_exchange_rates_and_usdkrw.png")  # 그림 저장


