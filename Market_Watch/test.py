# Created by Kim Hyeongjun on 01/19/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.
# https://ecos.bok.or.kr/jsp/openapi/OpenApiController.jsp
# ecos.bok.or.kr 접속 (E-mail: yuii7890@naver.com)
# 개발 가이드 > 통계코드검색

import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom


## 호출하려는 OpenAPI URL를 정의합니다.
url = "http://ecos.bok.or.kr/api/StatisticItemList/sample/xml/kr/1/1/901Y009/"

## 정의된 OpenAPI URL을 호출합니다.
response = requests.get(url)

## http 요청이 성공했을때 API의 리턴값을 가져옵니다.
if response.status_code == 200:
    try:
        contents = response.text
        ecosRoot = ET.fromstring(contents)
        ## 호출결과에 오류가 있었는지 확인합니다.
        if ecosRoot[0].text[:4] in ("INFO", "ERRO"):
            print(ecosRoot[0].text + " : " + ecosRoot[1].text)
        ## 오류메세지를 확인하고 처리합니다.
        else:
            ## 결과값을 활용하여 필요한 프로그램을 작성합니다.
            # print(contents)
            # dom = xml.dom.minidom.parse(xml_fname) # or
            dom = xml.dom.minidom.parseString(contents)
            pretty_xml_as_string = dom.toprettyxml(indent=" ")
            print(pretty_xml_as_string)
    except Exception as e:
        print(str(e))
        ##예외가 발생했을때 처리합니다.



########################################################################################################################
import datetime
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from data_raw.def_authentication import *


DD_END_DATE = "20220819"
MM_END_DATE = "202207"
QQ_END_DATE = "2022Q2"
YY_END_DATE = "2021"

AUTH_KEY=get_bok_auth_key()
STAT_CODE="200Y002"
CYCLE_TYPE="Q"
START_DATE="1960Q1"
END_DATE="2022Q2"
REQ_TYPE="xml"
LANG="kr"
START_COUNT="1"
END_COUNT="100000"
ITEM_1="?"
ITEM_2="?"
ITEM_3="?"
ITEM_4="?"

# 호출하려는 OpenAPI URL 정의
BOK_url = "".join(
    ["http://ecos.bok.or.kr/api/StatisticSearch/", AUTH_KEY, "/", REQ_TYPE, "/", LANG, "/", START_COUNT, "/",
     END_COUNT, "/", STAT_CODE, "/", CYCLE_TYPE, "/", START_DATE, "/", END_DATE, "/", ITEM_1, "/", ITEM_2, "/",
     ITEM_3, "/", ITEM_4])

# BOK_url = "http://ecos.bok.or.kr/api/StatisticSearch/sample/xml/kr/1/10/200Y001/A/2015/2021/10101/?/?/?"
# BOK_url = "".join(
#     ["http://ecos.bok.or.kr/api/StatisticSearch/", AUTH_KEY, "/xml/kr/1/100/200Y001/A/2015/2021/?/?/?/?"])
# BOK_url

# 정의된 OpenAPI URL을 호출합니다.
BOK_url
BOK_response = requests.get(BOK_url)
BOK_response.text

BOK_xml = BeautifulSoup(BOK_response.text, "xml")  # 이 코드가 현재 실행 안됨 (2023.01.16)
BOK_xml_row = BOK_xml.find_all("row")

BOK_xml = BeautifulSoup(BOK_response.text, "html.parser")
BOK_xml = BeautifulSoup(BOK_response.text, "xml")

list_STAT_CODE = []
list_STAT_NAME = []
list_ITEM_CODE1 = []
list_ITEM_NAME1 = []
list_ITEM_CODE2 = []
list_ITEM_NAME2 = []
list_ITEM_CODE3 = []
list_ITEM_NAME3 = []
list_ITEM_CODE4 = []
list_ITEM_NAME4 = []
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
    item_ITEM_CODE4 = item.find("ITEM_CODE4").text
    item_ITEM_NAME4 = item.find("ITEM_NAME4").text
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
    list_ITEM_CODE4.append(item_ITEM_CODE4)
    list_ITEM_NAME4.append(item_ITEM_NAME4)
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
df_BOK["ITEM_CODE4"] = list_ITEM_CODE4
df_BOK["ITEM_NAME4"] = list_ITEM_NAME4
df_BOK["UNIT_NAME"] = list_UNIT_NAME

df_BOK["TIME"] = list_TIME
if CYCLE_TYPE == "M":
    df_BOK["TIME"] = df_BOK["TIME"].apply(pd.to_numeric)
    df_BOK["DATETIME"] = pd.to_datetime(df_BOK['TIME'].astype(str), errors='coerce', format='%Y%m')
elif CYCLE_TYPE == "D":
    df_BOK["TIME"] = df_BOK["TIME"].apply(pd.to_numeric)
    df_BOK["DATETIME"] = pd.to_datetime(df_BOK['TIME'].astype(str), errors='coerce', format='%Y%m%d')
elif CYCLE_TYPE == "A":
    df_BOK["TIME"] = df_BOK["TIME"].apply(pd.to_numeric)

df_BOK["DATA_VALUE"] = list_DATA_VALUE

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
        list_ITEM_CODE4 = []
        list_ITEM_NAME4 = []
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
            item_ITEM_CODE4 = item.find("ITEM_CODE4").text
            item_ITEM_NAME4 = item.find("ITEM_NAME4").text
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
            list_ITEM_CODE4.append(item_ITEM_CODE4)
            list_ITEM_NAME4.append(item_ITEM_NAME4)
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
        df_BOK["ITEM_CODE4"] = list_ITEM_CODE4
        df_BOK["ITEM_NAME4"] = list_ITEM_NAME4
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

########################################################################################################################
# 2.6 한국은행 기준금리 및 여수신금리 [098Y001][DD, MM, QQ, YY] (1994.01.03 부터)
BOK_098Y001_DD = get_bok_data(STAT_CODE="722Y001", CYCLE_TYPE="DD", START_DATE="19940103", END_DATE=DD_END_DATE)
BOK_098Y001_DD.to_pickle('./Market_Watch_Data/BOK_098Y001_DD.pkl')


# 호출하려는 OpenAPI URL 정의
BOK_url = "".join(
    ["http://ecos.bok.or.kr/api/StatisticSearch/", AUTH_KEY, "/", REQ_TYPE, "/", LANG, "/", START_COUNT, "/",
     END_COUNT, "/", STAT_CODE, "/", CYCLE_TYPE, "/", START_DATE, "/", END_DATE, "/", ITEM_1, "/", ITEM_2, "/",
     ITEM_3])
# 정의된 OpenAPI URL을 호출합니다.
BOK_response = requests.get(BOK_url)



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


DD_END_DATE = "20220819"
MM_END_DATE = "202207"
QQ_END_DATE = "20222"
YY_END_DATE = "2021"

# MM_START_DATE = "200301"
# QQ_START_DATE = "20031"
