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






