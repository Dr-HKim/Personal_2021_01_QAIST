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


def get_yyyymm_add_months(n_yyyymm, n_months):
    n_yyyy, n_mm = divmod(n_yyyymm, 100)
    n_months_y, n_months_m = divmod(n_mm + n_months - 1, 12)
    output_yyyy = n_yyyy + n_months_y
    output_mm = n_months_m + 1
    output_yyyymm = output_yyyy * 100 + output_mm
    return output_yyyymm


def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny+dy, maxy+dy)


########################################################################################################################
# 그림 2.2 실질경제성장률과 기업의 매출액순이익률

# 10.1.1 국민계정(2015년 기준년) - 주요지표 - 연간지표 [111Y002] (1953 부터)
BOK_111Y002 = pd.read_pickle('./Market_Watch_Data/BOK_111Y002.pkl')
BOK_111Y002_01 = BOK_111Y002[BOK_111Y002["ITEM_CODE1"] == "20101"].copy()  # 국내총생산(실질성장률)[%]

# 12.1.1 기업경영분석 - 기업경영분석지표 - 기업경영분석지표(~2007)[027Y131][YY] (1960 부터)
BOK_027Y131 = pd.read_pickle('./Market_Watch_Data/BOK_027Y131.pkl')
BOK_027Y131_01 = BOK_027Y131[(BOK_027Y131["ITEM_NAME1"] == "전산업") & (BOK_027Y131["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
BOK_027Y131_02 = BOK_027Y131[(BOK_027Y131["ITEM_NAME1"] == "제조업") & (BOK_027Y131["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
BOK_027Y131_03 = BOK_027Y131[(BOK_027Y131["ITEM_NAME1"] == "제조업") & (BOK_027Y131["ITEM_NAME2"] == "매출액경상이익률(~2006)")].copy()  # 국내총생산(실질성장률)[%]

# 12.1.1 기업경영분석 - 기업경영분석지표 - 기업경영분석지표(2007~2010)[027Y331][YY]
BOK_027Y331 = pd.read_pickle('./Market_Watch_Data/BOK_027Y331.pkl')
BOK_027Y331_01 = BOK_027Y331[(BOK_027Y331["ITEM_NAME1"] == "전산업") & (BOK_027Y331["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
BOK_027Y331_02 = BOK_027Y331[(BOK_027Y331["ITEM_NAME1"] == "제조업") & (BOK_027Y331["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
BOK_027Y331_03 = BOK_027Y331[(BOK_027Y331["ITEM_NAME1"] == "제조업") & (BOK_027Y331["ITEM_NAME2"] == "매출액세전순이익률")].copy()  # 국내총생산(실질성장률)[%]

# 12.1.1 기업경영분석 - 기업경영분석지표 - 기업경영분석지표(2009~, 전수조사) [027Y431][YY]
BOK_027Y431 = pd.read_pickle('./Market_Watch_Data/BOK_027Y431.pkl')
BOK_027Y431_01 = BOK_027Y431[(BOK_027Y431["ITEM_NAME1"] == "전산업") & (BOK_027Y431["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
BOK_027Y431_02 = BOK_027Y431[(BOK_027Y431["ITEM_NAME1"] == "제조업") & (BOK_027Y431["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
BOK_027Y431_03 = BOK_027Y431[(BOK_027Y431["ITEM_NAME1"] == "제조업") & (BOK_027Y431["ITEM_NAME2"] == "매출액세전순이익률")].copy()  # 국내총생산(실질성장률)[%]

# 그림: 경제성장률과 기업이익의 추이
real_gdp_growth = BOK_111Y002_01.copy()
net_income_to_sales = pd.concat([BOK_027Y131_03, BOK_027Y331_03, BOK_027Y431_03])

fig, ax1 = plt.subplots()

color1 = "tab:red"
ax1.set_xlabel("year")
ax1.set_ylabel("Real GDP Growth (annual, %)", color=color1)
ax1.plot(real_gdp_growth["TIME"], real_gdp_growth["DATA_VALUE"], color=color1)
ax1.tick_params(axis="y")

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color2 = "tab:blue"
ax2.set_ylabel("Net Income to Sales (annual, %)", color=color2)  # we already handled the x-label with ax1
ax2.plot(net_income_to_sales["TIME"], net_income_to_sales["DATA_VALUE"], color=color2, linestyle='-')
ax2.tick_params(axis='y')

fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
align_yaxis(ax1, 0, ax2, 0)  # 두 축이 동일한 0 값을 가지도록 조정
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlim([1981, 2022])
plt.show()

# 그림 저장
plt.savefig("./Lecture_Figures_output/fig2.2_net_income_to_sales_and_real_gdp_growth.png")


########################################################################################################################
# 그림 2.3 실질경제성장률과 연간 코스피 성장률
# 실질GDP (전년동기대비변동률, %)
# 6.1.2 증권/재정 - 주식거래 및 주가지수 [028Y015][MM, YY] (200002, 1976 부터)
BOK_028Y015 = pd.read_pickle('./Market_Watch_Data/BOK_028Y015.pkl')
BOK_028Y015_01 = BOK_028Y015[BOK_028Y015["ITEM_NAME1"] == "KOSPI_종가"].copy()  # 국내총생산(GDP)(실질, 원계열, 전년동기)

# 그림: 경제성장률과 코스피지수의 추이
kospi_index = BOK_028Y015_01.copy()
kospi_index["L1_DATA_VALUE"] = kospi_index["DATA_VALUE"].shift(1)
kospi_index["GROWTH_RATE"] = (kospi_index["DATA_VALUE"]/kospi_index["L1_DATA_VALUE"]-1)*100

fig, ax1 = plt.subplots()

color1 = "tab:red"
ax1.set_xlabel("year")
ax1.set_ylabel("Real GDP Growth (annual, %)", color=color1)
ax1.plot(real_gdp_growth["TIME"], real_gdp_growth["DATA_VALUE"], color=color1)
ax1.tick_params(axis="y")

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color2 = "tab:blue"
ax2.set_ylabel("KOSPI Growth (annual, %)", color=color2)  # we already handled the x-label with ax1
ax2.plot(kospi_index["TIME"], kospi_index["GROWTH_RATE"], color=color2, linestyle='-')
ax2.tick_params(axis='y')

fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
align_yaxis(ax1, 0, ax2, 0)  # 두 축이 동일한 0 값을 가지도록 조정
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlim([1981, 2022])
plt.show()

# 그림 저장
plt.savefig("./Lecture_Figures_output/fig2.3_kospi_growth_and_real_gdp_growth.png")


########################################################################################################################
# 그림 2.7 코스피지수와 MSCI 신흥시장지수
# 데이터 불러오기
investpy_msci = pd.read_pickle('./Market_Watch_Data/investpy_msci.pkl')
investpy_kospi = pd.read_pickle('./Market_Watch_Data/investpy_kospi.pkl')

investpy_kospi.reset_index(level=0, inplace=True)  # 날짜 인덱스를 칼럼으로
investpy_kospi.rename(
    columns={"Open": "KOSPI_Open", "High": "KOSPI_High", "Low": "KOSPI_Low", "Close": "KOSPI_Close"}, inplace=True)
investpy_kospi = investpy_kospi[["Date", "KOSPI_Open", "KOSPI_High", "KOSPI_Low", "KOSPI_Close"]]

# MSCI, KOSPI 데이터 합치고 정렬
df_index_daily0 = pd.merge(investpy_msci, investpy_kospi, left_on="Date", right_on="Date", how="outer")
df_index_daily0.sort_values(by=["Date"], inplace=True)

# Daily to Monthly
# 날짜를 YYYYMM 형태로 변환
df_index_daily0["YYYYMM"] = df_index_daily0["Date"].dt.year * 100 + df_index_daily0["Date"].dt.month

# YYYYMM 그룹별 OHLC 구하기
df_index_monthly0 = df_index_daily0.groupby(by='YYYYMM', as_index=False).agg({
    "MXEF_Close": "last", "MXEF_Open": "first", "MXEF_High": "max", "MXEF_Low": "min",
    "MXWO_Close": "last", "MXWO_Open": "first", "MXWO_High": "max", "MXWO_Low": "min",
    "KOSPI_Close": "last", "KOSPI_Open": "first", "KOSPI_High": "max", "KOSPI_Low": "min"})

# YYYYMM 을 기준으로 그 달의 가장 마지막 날짜 입력
df_index_monthly0["Date"] = pd.to_datetime(
    get_yyyymm_add_months(df_index_monthly0["YYYYMM"], 1) * 100 + 1, errors='coerce', format='%Y%m%d') + pd.Timedelta(days=-1)

# 그림: MSCI Emerging Markets and KOSPI
fig, ax1 = plt.subplots()

color1 = "tab:red"
ax1.set_xlim([pd.to_datetime("1990-01-01 00:00:00"), pd.to_datetime("2022-12-31 00:00:00")])
ax1.set_xlabel("Date")
ax1.set_ylabel("KOSPI(1980.1.4=100)", color=color1)
ax1.plot(df_index_monthly0["Date"], df_index_monthly0["KOSPI_Close"], color=color1)
ax1.tick_params(axis="y")

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color2 = "tab:blue"
ax2.set_ylabel("MSCI Emerging Markets (1987.12.31=100)", color=color2)  # we already handled the x-label with ax1
ax2.plot(df_index_monthly0["Date"], df_index_monthly0["MXEF_Close"], color=color2, linestyle='-')
ax2.tick_params(axis='y')

fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
align_yaxis(ax1, 0, ax2, 0)  # 두 축이 동일한 0 값을 가지도록 조정
plt.show()

# 그림 저장
plt.savefig("./Lecture_Figures_output/fig2.7_kospi_and_msci_emerging_markets.png")

########################################################################################################################
# 그림 2.8 OECD 경기선행지수와 MSCI 신흥시장지수
# 데이터 불러오기
investpy_msci = pd.read_pickle('./Market_Watch_Data/investpy_msci.pkl')
oecd_monthly = pd.read_pickle('./Market_Watch_Data/oecd_monthly.pkl')

# LOLITOTR_GYSA: 12-month rate of change of the trend restored CLI
df_oecd_cli = oecd_monthly[(oecd_monthly["location_id"] == "OECD") & (oecd_monthly["subject_id"] == "LOLITOTR_GYSA")].copy()

# YYYYMM 을 기준으로 그 달의 가장 마지막 날짜 입력
df_oecd_cli["Date"] = pd.to_datetime(
    get_yyyymm_add_months(df_oecd_cli["yyyymm"], 1) * 100 + 1, errors='coerce', format='%Y%m%d') + pd.Timedelta(days=-1)

# MSCI 데이터 불러오기
df_msci_daily = investpy_msci.copy()

# Daily to Monthly
# 날짜를 YYYYMM 형태로 변환
df_msci_daily["YYYYMM"] = df_msci_daily["Date"].dt.year * 100 + df_msci_daily["Date"].dt.month

# YYYYMM 그룹별 OHLC 구하기
df_msci_monthly = df_msci_daily.groupby(by='YYYYMM', as_index=False).agg({
    "MXEF_Close": "last", "MXEF_Open": "first", "MXEF_High": "max", "MXEF_Low": "min",
    "MXWO_Close": "last", "MXWO_Open": "first", "MXWO_High": "max", "MXWO_Low": "min"})

df_msci_monthly["L12_MXEF_Close"] = df_msci_monthly["MXEF_Close"].shift(12)  # lag
df_msci_monthly["MXEF_YoY"] = (df_msci_monthly["MXEF_Close"]/df_msci_monthly["L12_MXEF_Close"] - 1)*100
# df_msci_monthly["L12_KOSPI_Close"] = df_msci_monthly["KOSPI_Close"].shift(12)  # lag
# df_msci_monthly["KOSPI_YoY"] = (df_msci_monthly["KOSPI_Close"]/df_msci_monthly["L12_KOSPI_Close"] - 1)*100

# YYYYMM 을 기준으로 그 달의 가장 마지막 날짜 입력
df_msci_monthly["Date"] = pd.to_datetime(
    get_yyyymm_add_months(df_msci_monthly["YYYYMM"], 1) * 100 + 1, errors='coerce', format='%Y%m%d') + pd.Timedelta(days=-1)


# 시각화
fig, ax1 = plt.subplots()

color1 = "tab:red"
ax1.set_xlim([pd.to_datetime("1990-01-01 00:00:00"), pd.to_datetime("2022-12-31 00:00:00")])
ax1.set_xlabel("Date")
ax1.set_ylabel("OECD Composite Leading Indicator", color=color1)
ax1.plot(df_oecd_cli["Date"], df_oecd_cli["datavalue"], color=color1)
ax1.tick_params(axis="y")

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color2 = "tab:blue"
ax2.set_ylabel("MSCI Emerging Markets Monthly YoY", color=color2)  # we already handled the x-label with ax1
ax2.plot(df_msci_monthly["Date"], df_msci_monthly["MXEF_YoY"], color=color2, linestyle='-')
ax2.tick_params(axis='y')

fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
align_yaxis(ax1, 0, ax2, 0)  # 두 축이 동일한 0 값을 가지도록 조정
plt.axhline(y=0, color='green', linestyle='dotted')
plt.show()

# 그림 저장
plt.savefig("./Lecture_Figures_output/fig2.8_oecd_cli_and_msci_emerging_markets.png")
