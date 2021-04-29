# Created by Kim Hyeongjun on 01/19/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.
# 조지프 엘리스, "경제를 읽는 기술 (Ahead of the Curve)"


import datetime
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from data_raw.def_authentication import *


def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny+dy, maxy+dy)


def get_bok_data(STAT_CODE, CYCLE_TYPE, START_DATE, END_DATE, AUTH_KEY=get_bok_auth_key(), REQ_TYPE="xml", LANG="kr",
                 START_COUNT="1", END_COUNT="100000", ITEM_1="?", ITEM_2="?", ITEM_3="?"):
    # 호출하려는 OpenAPI URL 정의
    BOK_url = "".join(
        ["http://ecos.bok.or.kr/api/StatisticSearch/", AUTH_KEY, "/", REQ_TYPE, "/", LANG, "/", START_COUNT, "/",
         END_COUNT, "/", STAT_CODE, "/", CYCLE_TYPE, "/", START_DATE, "/", END_DATE, "/", ITEM_1, "/", ITEM_2, "/",
         ITEM_3])
    # 정의된 OpenAPI URL을 호출합니다.
    BOK_response = requests.get(BOK_url)

    # http 요청이 성공했을때 API의 리턴값 가져오기
    if BOK_response.status_code == 200:
        try:
            BOK_xml = BeautifulSoup(BOK_response.text, "xml")
            BOK_xml_row = BOK_xml.find_all("row")

            list_STAT_CODE = []
            list_STAT_NAME = []
            list_ITEM_CODE1 = []
            list_ITEM_NAME1 = []
            list_ITEM_CODE2 = []
            list_ITEM_NAME2 = []
            list_ITEM_CODE3 = []
            list_ITEM_NAME3 = []
            list_UNIT_NAME = []
            list_TIME = []
            list_DATA_VALUE = []

            for item in BOK_xml_row:
                item_STAT_CODE = item.find("STAT_CODE").text
                item_STAT_NAME = item.find("STAT_NAME").text
                item_ITEM_CODE1 = item.find("ITEM_CODE1").text
                item_ITEM_NAME1 = item.find("ITEM_NAME1").text
                item_ITEM_CODE2 = item.find("ITEM_CODE2").text
                item_ITEM_NAME2 = item.find("ITEM_NAME2").text
                item_ITEM_CODE3 = item.find("ITEM_CODE3").text
                item_ITEM_NAME3 = item.find("ITEM_NAME3").text
                item_UNIT_NAME = item.find("UNIT_NAME").text
                item_TIME = item.find("TIME").text
                item_DATA_VALUE = item.find("DATA_VALUE").text

                try:
                    item_DATA_VALUE = float(item_DATA_VALUE)
                except:
                    item_DATA_VALUE = np.nan

                list_STAT_CODE.append(item_STAT_CODE)
                list_STAT_NAME.append(item_STAT_NAME)
                list_ITEM_CODE1.append(item_ITEM_CODE1)
                list_ITEM_NAME1.append(item_ITEM_NAME1)
                list_ITEM_CODE2.append(item_ITEM_CODE2)
                list_ITEM_NAME2.append(item_ITEM_NAME2)
                list_ITEM_CODE3.append(item_ITEM_CODE3)
                list_ITEM_NAME3.append(item_ITEM_NAME3)
                list_UNIT_NAME.append(item_UNIT_NAME)
                list_TIME.append(item_TIME)
                list_DATA_VALUE.append(item_DATA_VALUE)

            df_BOK = pd.DataFrame(list_STAT_CODE, columns=["STAT_CODE"])
            df_BOK["STAT_NAME"] = list_STAT_NAME
            df_BOK["ITEM_CODE1"] = list_ITEM_CODE1
            df_BOK["ITEM_NAME1"] = list_ITEM_NAME1
            df_BOK["ITEM_CODE2"] = list_ITEM_CODE2
            df_BOK["ITEM_NAME2"] = list_ITEM_NAME2
            df_BOK["ITEM_CODE3"] = list_ITEM_CODE3
            df_BOK["ITEM_NAME3"] = list_ITEM_NAME3
            df_BOK["UNIT_NAME"] = list_UNIT_NAME
            df_BOK["TIME"] = list_TIME
            df_BOK["TIME"] = df_BOK["TIME"].apply(pd.to_numeric)
            df_BOK["DATA_VALUE"] = list_DATA_VALUE

            if CYCLE_TYPE == "MM":
                df_BOK["DATETIME"] = pd.to_datetime(df_BOK['TIME'].astype(str), errors='coerce', format='%Y%m')
            elif CYCLE_TYPE == "DD":
                df_BOK["DATETIME"] = pd.to_datetime(df_BOK['TIME'].astype(str), errors='coerce', format='%Y%m%d')

        except Exception as e:
            print(str(e))
            # 예외가 발생했을때 처리
    return df_BOK


MM_START_DATE = "200301"
QQ_START_DATE = "20031"

DD_END_DATE = "20210219"
MM_END_DATE = "202101"
QQ_END_DATE = "20204"

########################################################################################################################
# 10.1.1 국민계정(2015년 기준년) - 주요지표 - 연간지표 [111Y002] (1953 부터)
BOK111Y002 = get_bok_data(STAT_CODE="111Y002", CYCLE_TYPE="YY", START_DATE="1953", END_DATE="2020")
BOK111Y002.groupby(["ITEM_CODE1", "ITEM_NAME1"]).size()
BOK111Y002_01 = BOK111Y002[BOK111Y002["ITEM_CODE1"] == "20101"].copy()  # 국내총생산(실질성장률)[%]

# 12.1.1 기업경영분석 - 기업경영분석지표 - 기업경영분석지표(~2007)[027Y131][YY] (1960 부터)
BOK027Y131 = get_bok_data(STAT_CODE="027Y131", CYCLE_TYPE="YY", START_DATE="1960", END_DATE="2006")
BOK027Y131_01 = BOK027Y131[(BOK027Y131["ITEM_NAME1"] == "전산업") & (BOK027Y131["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
BOK027Y131_02 = BOK027Y131[(BOK027Y131["ITEM_NAME1"] == "제조업") & (BOK027Y131["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
BOK027Y131_03 = BOK027Y131[(BOK027Y131["ITEM_NAME1"] == "제조업") & (BOK027Y131["ITEM_NAME2"] == "매출액경상이익률(~2006)")].copy()  # 국내총생산(실질성장률)[%]

# 12.1.1 기업경영분석 - 기업경영분석지표 - 기업경영분석지표(2007~2010)[027Y331][YY]
BOK027Y331 = get_bok_data(STAT_CODE="027Y331", CYCLE_TYPE="YY", START_DATE="2007", END_DATE="2008")
BOK027Y331_01 = BOK027Y331[(BOK027Y331["ITEM_NAME1"] == "전산업") & (BOK027Y331["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
BOK027Y331_02 = BOK027Y331[(BOK027Y331["ITEM_NAME1"] == "제조업") & (BOK027Y331["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
BOK027Y331_03 = BOK027Y331[(BOK027Y331["ITEM_NAME1"] == "제조업") & (BOK027Y331["ITEM_NAME2"] == "매출액세전순이익률")].copy()  # 국내총생산(실질성장률)[%]

# 12.1.1 기업경영분석 - 기업경영분석지표 - 기업경영분석지표(2009~, 전수조사) [027Y431][YY]
BOK027Y431 = get_bok_data(STAT_CODE="027Y431", CYCLE_TYPE="YY", START_DATE="2009", END_DATE="2020")
BOK027Y431.groupby(["ITEM_CODE1", "ITEM_NAME1"]).size()
BOK027Y431_01 = BOK027Y431[(BOK027Y431["ITEM_NAME1"] == "전산업") & (BOK027Y431["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
BOK027Y431_02 = BOK027Y431[(BOK027Y431["ITEM_NAME1"] == "제조업") & (BOK027Y431["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
BOK027Y431_03 = BOK027Y431[(BOK027Y431["ITEM_NAME1"] == "제조업") & (BOK027Y431["ITEM_NAME2"] == "매출액세전순이익률")].copy()  # 국내총생산(실질성장률)[%]

########################################################################################################################
# 그림: 경제성장률과 기업이익의 추이
real_gdp_growth = BOK111Y002_01.copy()
net_income_to_sales = pd.concat([BOK027Y131_03, BOK027Y331_03, BOK027Y431_03])

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
fig.set_size_inches(2400/300, 1800/300)  # 그래프 크기 지정, DPI=300
align_yaxis(ax1, 0, ax2, 0)  # 두 축이 동일한 0 값을 가지도록 조정
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlim([1981, 2020])
plt.show()

# 그림 저장
plt.savefig("./data_processed/fig1_net_income_to_sales_and_real_gdp_growth.png")

########################################################################################################################
# 실질GDP (전년동기대비변동률, %)
# 6.1.2 증권/재정 - 주식거래 및 주가지수 [028Y015][MM, YY] (200002, 1976 부터)
BOK028Y015 = get_bok_data(STAT_CODE="028Y015", CYCLE_TYPE="YY", START_DATE="1976", END_DATE="2020")
BOK028Y015.groupby(["ITEM_CODE1", "ITEM_NAME1"]).size()
BOK028Y015_01 = BOK028Y015[BOK028Y015["ITEM_NAME1"] == "KOSPI_종가"].copy()  # 국내총생산(GDP)(실질, 원계열, 전년동기)

# 그림: 경제성장률과 코스피지수의 추이
kospi_index = BOK028Y015_01.copy()
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
fig.set_size_inches(2400/300, 1800/300)  # 그래프 크기 지정, DPI=300
align_yaxis(ax1, 0, ax2, 0)  # 두 축이 동일한 0 값을 가지도록 조정
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlim([1981, 2020])
plt.show()

# 그림 저장
plt.savefig("./data_processed/fig2_kospi_growth_and_real_gdp_growth.png")


########################################################################################################################
kosis_url = get_kosis_url()
kosis_response = requests.get(kosis_url)  # Open API URL 호출
data = kosis_response.json()
dfItem = pd.DataFrame.from_records(data)

import investpy

tmp = investpy.indices.get_indices_dict(country=None, columns=None, as_json=False)
dfItem = pd.DataFrame.from_records(tmp)

tmp2 = investpy.indices.search_indices(by="name", value="MSCI Emerging Markets")

df = investpy.get_index_historical_data(index="MSCI Emerging Markets", country="world",
                                        from_date='30/01/2012',
                                        to_date='27/04/2021')


########################################################################################################################
# 실질GDP (전년동기대비변동률, %)
# 10.1.2 국민계정(2015년 기준년) - 주요지표 - 분기지표 [111Y055] (1960Q1 부터)
BOK111Y055 = get_bok_data(STAT_CODE="111Y055", CYCLE_TYPE="QQ", START_DATE="19601", END_DATE=QQ_END_DATE)
BOK111Y055.groupby(["ITEM_CODE1", "ITEM_NAME1"]).size()
BOK111Y055_01 = BOK111Y055[BOK111Y055["ITEM_CODE1"] == "10211"].copy()  # 국내총생산(GDP)(실질, 원계열, 전년동기)
BOK111Y055_01["Year"], BOK111Y055_01["Quarter"] = BOK111Y055_01["TIME"].divmod(10)

tmp = BOK111Y055_01.loc[BOK111Y055_01["Year"] > 2017]

plt.bar(range(len(tmp.DATA_VALUE)), tmp.DATA_VALUE, align='center')
plt.xticks(range(len(tmp.DATA_VALUE)), tmp.TIME, size='small')
plt.show()

# 실질소비자지출(PCE) (전년동기대비변동률, %) (홍정의: 실질 가계 최종소비지출)
# 10.7.1.1.2. 가계의 목적별 최종소비지출(계절조정, 실질, 분기) [111Y027] (1970Q1 부터)
BOK111Y027 = get_bok_data(STAT_CODE="111Y027", CYCLE_TYPE="QQ", START_DATE="19701", END_DATE=QQ_END_DATE)
BOK111Y027.groupby(["ITEM_CODE1", "ITEM_NAME1"]).size()
BOK111Y027_01 = BOK111Y027[BOK111Y027["ITEM_CODE1"] == "10116"].copy()  # 가계 최종소비지출
BOK111Y027_01["L4_PCE"] = BOK111Y027_01["DATA_VALUE"].shift(4)
BOK111Y027_01["Growth_Rate"] = (BOK111Y027_01["DATA_VALUE"] / BOK111Y027_01["L4_PCE"] - 1) * 100

# 산업생산 (전년동기대비변동률, %)
# FRB, 통계청


# 실질자본지출 (전년동기대비변동률, %) (홍정의: 실질 총고정자본형성)
# 10.6.1.2. 자본재형태별 총자본형성(계절조정, 실질, 분기) [111Y023] (1970Q1 부터)
BOK111Y023 = get_bok_data(STAT_CODE="111Y023", CYCLE_TYPE="QQ", START_DATE="19701", END_DATE=QQ_END_DATE)
BOK111Y023.groupby(["ITEM_CODE1", "ITEM_NAME1"]).size()
BOK111Y023_01 = BOK111Y023[BOK111Y023["ITEM_CODE1"] == "10101"].copy()  # 총고정자본형성
BOK111Y023_01["L4_CAPEXP"] = BOK111Y023_01["DATA_VALUE"].shift(4)
BOK111Y023_01["Growth_Rate"] = (BOK111Y023_01["DATA_VALUE"] / BOK111Y023_01["L4_CAPEXP"] - 1) * 100

# S&P 편입 기업들의 주당순익 (전년동기대비변동률, %)
# NBER, 데이터가이드

# 실업률(%) - 노동통계국
# 17. 거시경제분석 지표 [901Y001][MM, QQ, YY] (1960.01, 1960Q1 부터)
BOK901Y001 = get_bok_data(STAT_CODE="901Y001", CYCLE_TYPE="QQ", START_DATE="19601", END_DATE=QQ_END_DATE)
BOK901Y001.groupby(["ITEM_CODE1", "ITEM_NAME1"]).size()
BOK901Y001_01 = BOK901Y001[BOK901Y001["ITEM_CODE1"] == "AI1AJ"]  # 실업률






