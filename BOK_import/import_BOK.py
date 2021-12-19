# Created by Kim Hyeongjun on 01/19/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.

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


DD_END_DATE = "20211217"
MM_END_DATE = "202111"
QQ_END_DATE = "20213"

MM_START_DATE = "200301"
QQ_START_DATE = "20031"

########################################################################################################################
# # 6.1.1 증권/재정 - 주식거래 및 주가지수 - 주식시장(일별) [064Y001] (1995.01.03 부터)
# BOK064Y001_19950103_20210131 = get_bok_data(
#     STAT_CODE="064Y001", CYCLE_TYPE="DD", START_DATE="19950103", END_DATE="20210131")
# # 에러 수정: 20110827은 토요일이며, 모든 값에 0 입력되어 있음
# BOK064Y001_19950103_20210131 = BOK064Y001_19950103_20210131[BOK064Y001_19950103_20210131["TIME"] != 20110827].copy()
# # 에러 수정: 20210118 거래량 단위 잘못 입력되어 있음
# BOK064Y001_19950103_20210131["DATA_VALUE"][(BOK064Y001_19950103_20210131["ITEM_CODE1"] == "0002000") &
#                                            (BOK064Y001_19950103_20210131["TIME"] == 20210118)] = 147204
#
# # BOK064Y001_19950103_20210131 저장
# BOK064Y001_19950103_20210131.to_pickle('./BOK_processed/BOK064Y001_19950103_20210131.pkl')

########################################################################################################################
# 6.1.1 증권/재정 - 주식거래 및 주가지수 - 주식시장(일별) [064Y001] (1995.01.03 부터)
# BOK064Y001_19950103_20210131 불러오기
BOK064Y001_19950103_20210131 = pd.read_pickle('./BOK_processed/BOK064Y001_19950103_20210131.pkl')

BOK064Y001_UPDATE = get_bok_data(STAT_CODE="064Y001", CYCLE_TYPE="DD", START_DATE="20210201", END_DATE=DD_END_DATE)
BOK064Y001 = pd.concat([BOK064Y001_19950103_20210131, BOK064Y001_UPDATE])
BOK064Y001 = BOK064Y001.sort_values(by=['ITEM_CODE1', 'TIME'])

BOK064Y001_01 = BOK064Y001[BOK064Y001["ITEM_CODE1"] == "0001000"]  # KOSPI지수
BOK064Y001_02 = BOK064Y001[BOK064Y001["ITEM_CODE1"] == "0002000"]  # 거래량(주식시장, 잠정치)
BOK064Y001_03 = BOK064Y001[BOK064Y001["ITEM_CODE1"] == "0003000"]  # 거래대금(주식시장 , 잠정치)
BOK064Y001_04 = BOK064Y001[BOK064Y001["ITEM_CODE1"] == "0030000"]  # 외국인 순매수(주식시장, 잠정치)
BOK064Y001_05 = BOK064Y001[BOK064Y001["ITEM_CODE1"] == "0087000"]  # 주식시장-거래량(만주, 시간외거래분 포함)
BOK064Y001_06 = BOK064Y001[BOK064Y001["ITEM_CODE1"] == "0088000"]  # 주식시장-거래대금(억원, 시간외거래분 포함)
BOK064Y001_07 = BOK064Y001[BOK064Y001["ITEM_CODE1"] == "0089000"]  # KOSDAQ지수
BOK064Y001_08 = BOK064Y001[BOK064Y001["ITEM_CODE1"] == "0090000"]  # 거래량(만주 : 코스닥시장, 잠정치)
BOK064Y001_09 = BOK064Y001[BOK064Y001["ITEM_CODE1"] == "0091000"]  # 거래대금(억원 : 코스닥시장, 잠정치)
BOK064Y001_10 = BOK064Y001[BOK064Y001["ITEM_CODE1"] == "0113000"]  # 외국인 순매수(코스닥시장, 잠정치)
BOK064Y001_11 = BOK064Y001[BOK064Y001["ITEM_CODE1"] == "0183000"]  # 시가총액(주식시장, 잠정치)

########################################################################################################################
# 10.1.2 국민계정(2015년 기준년) - 주요지표 - 분기지표 [111Y055] (1960Q1 부터)
BOK111Y055 = get_bok_data(STAT_CODE="111Y055", CYCLE_TYPE="QQ", START_DATE="19601", END_DATE=QQ_END_DATE)
BOK111Y055.groupby(["ITEM_CODE1", "ITEM_NAME1"]).size()
BOK111Y055_01 = BOK111Y055[BOK111Y055["ITEM_CODE1"] == "10111"]  # 국내총생산(GDP)(실질, 계절조정, 전기비)

# 10.7.1.1.2. 가계의 목적별 최종소비지출(계절조정, 실질, 분기) [111Y027] (1970Q1 부터)
BOK111Y027 = get_bok_data(STAT_CODE="111Y027", CYCLE_TYPE="QQ", START_DATE="19701", END_DATE=QQ_END_DATE)
BOK111Y027.groupby(["ITEM_CODE1", "ITEM_NAME1"]).size()
BOK111Y027_01 = BOK111Y027[BOK111Y027["ITEM_CODE1"] == "10116"]  # 가계 최종소비지출


########################################################################################################################
# 시각화
plt.plot(BOK064Y001_01["DATETIME"], BOK064Y001_01["DATA_VALUE"], color='r', label="KOSPI")
plt.plot(BOK064Y001_02["DATETIME"], BOK064Y001_02["DATA_VALUE"], color='g', label="KOSPI(volume)")
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Rates (%)', fontsize=10)
plt.legend(loc='upper left')
plt.show()

# 시각화
fig, (ax1, ax2) = plt.subplots(2, sharex=True)
fig.suptitle('Aligning x-axis using sharex')
ax1.plot(BOK064Y001_01["DATETIME"], BOK064Y001_01["DATA_VALUE"], color='b', label="KOSPI")
plt.legend(loc='upper left')
ax2.plot(BOK064Y001_02["DATETIME"], BOK064Y001_02["DATA_VALUE"], color='g', label="KOSPI(volume)")
plt.legend(loc='upper left')
plt.show()

BOK064Y001.groupby(["ITEM_CODE1", "ITEM_NAME1"]).size()


# 4.1.1 시장금리(일별) [060Y001] (1995.01.03 부터)
BOK060Y001 = get_bok_data(STAT_CODE="060Y001", CYCLE_TYPE="DD", START_DATE="19950103", END_DATE="19970103")
BOK060Y001_01 = BOK060Y001[BOK060Y001["ITEM_NAME1"] == "CD(91일)"]

# 4.1.2 시장금리(월,분기,년) [028Y001] (1987.01, 1987Q1, 1987 부터)
BOK028Y001 = get_bok_data(STAT_CODE="028Y001", CYCLE_TYPE="MM", START_DATE="198701", END_DATE="201912")
BOK028Y001_01 = BOK028Y001[BOK028Y001["ITEM_NAME1"] == "국고채(3년)"]

# 4.2.2.1 예금은행 가중평균금리 - 대출금리 - 신규취급액 기준 [005Y003] (1996.01 부터)
BOK005Y003 = get_bok_data(STAT_CODE="005Y003", CYCLE_TYPE="MM", START_DATE="199601", END_DATE=MM_END_DATE)
BOK005Y003_01 = BOK005Y003[BOK005Y003["ITEM_NAME1"] == " 주택담보대출"]


# 시각화
plt.plot(BOK005Y003_01["DATETIME"], BOK005Y003_01["DATA_VALUE"], color='g', label="Mortgage Rate")
plt.plot(BOK028Y001_01["DATETIME"], BOK028Y001_01["DATA_VALUE"], color='y', label="KTB3Y")
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Rates (%)', fontsize=10)
plt.legend(loc='upper left')
plt.show()

BOK028Y001["ITEM_NAME1"].value_counts()


# 7.7.1 주택매매가격지수(KB) [085Y021] 2019.01 = 100
BOK085Y021 = get_bok_data(STAT_CODE="085Y021", CYCLE_TYPE="MM", START_DATE=MM_START_DATE, END_DATE=MM_END_DATE)




# 전체자료: 9.1.1.1 기업경기실사지수(BSI)-전국실적 (STAT_CODE="041Y013")
BOK041Y013 = get_bok_data(STAT_CODE="041Y013", CYCLE_TYPE="MM", START_DATE=MM_START_DATE, END_DATE=MM_END_DATE)

# 전체자료: 9.1.1.2 기업경기실사지수(BSI)-전국전망
BOK041Y014 = get_bok_data(STAT_CODE="041Y014", CYCLE_TYPE="MM", START_DATE=MM_START_DATE, END_DATE=MM_END_DATE)

# 전체자료: 12.15.1 기업경영분석(분기) - 성장성에 관한 지표(027Y215)
BOK027Y215 = get_bok_data(STAT_CODE="027Y215", CYCLE_TYPE="QQ", START_DATE=QQ_START_DATE, END_DATE=QQ_END_DATE)

# 전체자료: 15.1 대출행태서베이 - 대출태도(093Y001)
BOK093Y001 = get_bok_data(STAT_CODE="093Y001", CYCLE_TYPE="QQ", START_DATE=QQ_START_DATE, END_DATE=QQ_END_DATE)

# 전체자료: 15.2 대출행태서베이 - 신용위험(093Y002)
BOK093Y002 = get_bok_data(STAT_CODE="093Y002", CYCLE_TYPE="QQ", START_DATE=QQ_START_DATE, END_DATE=QQ_END_DATE)

# 전체자료: 3.6.1 가계신용(분기별)
BOK008Y001 = get_bok_data(STAT_CODE="008Y001", CYCLE_TYPE="QQ", START_DATE=QQ_START_DATE, END_DATE=QQ_END_DATE)

########################################################################################################################
STAT_CODE="060Y001"
CYCLE_TYPE="DD"
START_DATE="19950103"
END_DATE="19970103"
AUTH_KEY=get_bok_auth_key()
REQ_TYPE="xml"
LANG="kr"
START_COUNT="1"
END_COUNT="100000"
ITEM_1="?"
ITEM_2="?"
ITEM_3="?"

# 호출하려는 OpenAPI URL 정의
BOK_url = "".join(
    ["http://ecos.bok.or.kr/api/StatisticSearch/", AUTH_KEY, "/", REQ_TYPE, "/", LANG, "/", START_COUNT, "/",
     END_COUNT, "/", STAT_CODE, "/", CYCLE_TYPE, "/", START_DATE, "/", END_DATE, "/", ITEM_1, "/", ITEM_2, "/",
     ITEM_3])
# 정의된 OpenAPI URL을 호출합니다.
BOK_response = requests.get(BOK_url)

BOK_xml = BeautifulSoup(BOK_response.text, "xml")
BOK_xml_row = BOK_xml.find_all("row")

print(BOK_xml_row[1])

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
list_DATETIME = []

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
    item_DATETIME = datetime.datetime.strptime(item_TIME, "%Y%m%d")

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
    list_DATETIME.append(item_DATETIME)

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
df_BOK["DATA_VALUE"] = list_DATA_VALUE
df_BOK["DATETIME"] = list_DATETIME
df_BOK["TIME"] = df_BOK["TIME"].apply(pd.to_numeric)

