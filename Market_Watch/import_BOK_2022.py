# Created by Kim Hyeongjun on 08/23/2022.
# Copyright © 2022 dr-hkim.github.io. All rights reserved.
# https://ecos.bok.or.kr/api/#/
# ecos.bok.or.kr 접속 (E-mail: yuii7890@naver.com)
# 개발 가이드 > 통계코드검색
# 2022년 ECOS 개편과 함께 Open API 도 크게 개편되면서 STAT_CODE 가 많이 변경됨

import datetime
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from data_raw.def_authentication import *


def get_bok_data(STAT_CODE, CYCLE_TYPE, START_DATE, END_DATE, AUTH_KEY=get_bok_auth_key(), REQ_TYPE="xml", LANG="kr",
                 START_COUNT="1", END_COUNT="100000", ITEM_1="?", ITEM_2="?", ITEM_3="?", ITEM_4="?"):
    # 호출하려는 OpenAPI URL 정의
    BOK_url = "".join(
        ["http://ecos.bok.or.kr/api/StatisticSearch/", AUTH_KEY, "/", REQ_TYPE, "/", LANG, "/", START_COUNT, "/",
         END_COUNT, "/", STAT_CODE, "/", CYCLE_TYPE, "/", START_DATE, "/", END_DATE, "/", ITEM_1, "/", ITEM_2, "/",
         ITEM_3, "/", ITEM_4])
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

        except Exception as e:
            print(str(e))
            # 예외가 발생했을때 처리
    return df_BOK


DD_END_DATE = "20230115"
MM_END_DATE = "202212"
QQ_END_DATE = "2022Q4"
YY_END_DATE = "2022"

# MM_START_DATE = "200301"
# QQ_START_DATE = "20031"


# macOS 일 경우 폴더 경로 변경
# Import the os module
import os
os.getcwd()

# path = '/Users/hkim/PycharmProjects/Personal_2021_01_QAIST'
# try:
#     os.chdir(path)
#     print("Current working directory: {0}".format(os.getcwd()))
# except FileNotFoundError:
#     print("Directory: {0} does not exist".format(path))
# except NotADirectoryError:
#     print("{0} is not a directory".format(path))
# except PermissionError:
#     print("You do not have permissions to change to {0}".format(path))

########################################################################################################################
# # 6.1.1 증권/재정 - 주식거래 및 주가지수 - 주식시장(일별) [064Y001] (1995.01.03 부터)
# BOK_064Y001_19950103_20210131 = get_bok_data(
#     STAT_CODE="064Y001", CYCLE_TYPE="DD", START_DATE="19950103", END_DATE="20210131")
# # 에러 수정: 20110827은 토요일이며, 모든 값에 0 입력되어 있음
# BOK_064Y001_19950103_20210131 = BOK_064Y001_19950103_20210131[BOK_064Y001_19950103_20210131["TIME"] != 20110827].copy()
# # 에러 수정: 20210118 거래량 단위 잘못 입력되어 있음
# BOK_064Y001_19950103_20210131["DATA_VALUE"][(BOK_064Y001_19950103_20210131["ITEM_CODE1"] == "0002000") &
#                                            (BOK_064Y001_19950103_20210131["TIME"] == 20210118)] = 147204
#
# # BOK_064Y001_19950103_20210131 저장
# BOK_064Y001_19950103_20210131.to_pickle('./BOK_raw/BOK_064Y001_19950103_20210131.pkl')

########################################################################################################################
# KOSIS 데이터 불러오기
# KOSIS Open API >  서비스이용 > 통계자료 > 자료등록
kosis_auth_key = get_kosis_auth_key()
kosis_user_id = get_kosis_user_id()

# KOSIS 제조업 생산능력 및 가동률지수 (2015=100, 계절조정) (1980.01 시작)
kosis_url = \
    "https://kosis.kr/openapi/statisticsData.do?method=getList&apiKey=" + kosis_auth_key \
    + "&format=json&jsonVD=Y&userStatsId=" + kosis_user_id + "/101/DT_1F31501/2/1/20211225210033_6&prdSe=M&startPrdDe=" \
    + "197101" + "&endPrdDe=" + MM_END_DATE
kosis_response = requests.get(kosis_url)  # Open API URL 호출
data = kosis_response.json()
KOSIS_DT_1F31501 = pd.DataFrame.from_records(data)
KOSIS_DT_1F31501['PRD_DE2'] = KOSIS_DT_1F31501['PRD_DE'] + "01"  # 날짜 입력 준비
KOSIS_DT_1F31501["DATETIME"] = pd.to_datetime(KOSIS_DT_1F31501['PRD_DE2'], errors='coerce', format='%Y%m%d')  # 날짜
KOSIS_DT_1F31501["DATA_VALUE"] = pd.to_numeric(KOSIS_DT_1F31501["DT"])  # 텍스트를 숫자로 변환
KOSIS_DT_1F31501.to_pickle('./Market_Watch_Data/KOSIS_DT_1F31501.pkl')

# KOSIS 제조업 평균가동률 (1980.01 시작)
kosis_url = \
    "https://kosis.kr/openapi/statisticsData.do?method=getList&apiKey=" + kosis_auth_key \
    + "&format=json&jsonVD=Y&userStatsId=" + kosis_user_id + "/101/DT_1F31502/2/1/20211225194325_2&prdSe=M&startPrdDe=" \
    + "198001" + "&endPrdDe=" + MM_END_DATE
kosis_response = requests.get(kosis_url)  # Open API URL 호출
data = kosis_response.json()
KOSIS_DT_1F31502 = pd.DataFrame.from_records(data)
KOSIS_DT_1F31502['PRD_DE2'] = KOSIS_DT_1F31502['PRD_DE'] + "01"  # 날짜 입력 준비
KOSIS_DT_1F31502["DATETIME"] = pd.to_datetime(KOSIS_DT_1F31502['PRD_DE2'], errors='coerce', format='%Y%m%d')  # 날짜
KOSIS_DT_1F31502["DATA_VALUE"] = pd.to_numeric(KOSIS_DT_1F31502["DT"])  # 텍스트를 숫자로 변환
KOSIS_DT_1F31502.to_pickle('./Market_Watch_Data/KOSIS_DT_1F31502.pkl')


########################################################################################################################
# 1.3.1. 한국은행 기준금리 및 여수신금리 [722Y001][A,D,M,Q] (1994.01.03 부터)
BOK_722Y001_DD = get_bok_data(STAT_CODE="722Y001", CYCLE_TYPE="D", START_DATE="19940103", END_DATE=DD_END_DATE)
BOK_722Y001_DD.to_pickle('./Market_Watch_Data/BOK_722Y001_DD.pkl')

# 1.3.2.1. 시장금리(일별) [817Y002][D] (1995.01.03 부터)
BOK_817Y002 = get_bok_data(STAT_CODE="817Y002", CYCLE_TYPE="D", START_DATE="19950103", END_DATE=DD_END_DATE)
BOK_817Y002.to_pickle('./Market_Watch_Data/BOK_817Y002.pkl')

# 1.3.2.2. 시장금리(월,분기,년) [721Y001][A,M,Q] (1987.01, 1987Q1, 1987 부터)
BOK_721Y001 = get_bok_data(STAT_CODE="721Y001", CYCLE_TYPE="M", START_DATE="198701", END_DATE=MM_END_DATE)
BOK_721Y001.to_pickle('./Market_Watch_Data/BOK_721Y001.pkl')

# 1.3.3.1.1. 예금은행 가중평균금리 > 수신금리 - 신규취급액 기준 [121Y002][A,M,Q] (1996.01 부터)
BOK_121Y002 = get_bok_data(STAT_CODE="121Y002", CYCLE_TYPE="M", START_DATE="199601", END_DATE=MM_END_DATE)
BOK_121Y002.to_pickle('./Market_Watch_Data/BOK_121Y002.pkl')

# 1.3.3.2.1. 예금은행 가중평균금리 - 대출금리 - 신규취급액 기준 [121Y006][A,M,Q] (1996.01 부터)
BOK_121Y006 = get_bok_data(STAT_CODE="121Y006", CYCLE_TYPE="M", START_DATE="199601", END_DATE=MM_END_DATE)
BOK_121Y006.to_pickle('./Market_Watch_Data/BOK_121Y006.pkl')

BOK_817Y002_01 = BOK_817Y002[BOK_817Y002["ITEM_NAME1"] == "CD(91일)"]
BOK_721Y001_01 = BOK_721Y001[BOK_721Y001["ITEM_NAME1"] == "국고채(5년)"]
BOK_121Y006_01 = BOK_121Y006[BOK_121Y006["ITEM_NAME1"] == "주택담보대출"]

# 1.5.1.1. 주식/채권/재정 - 주식거래/주가지수 - 주식시장(일) [802Y001][D] (1995.01.03 부터)
# # BOK_802Y001_19950103_20220731 저장하기
# BOK_802Y001_19950103_20220731 = get_bok_data(STAT_CODE="802Y001", CYCLE_TYPE="D", START_DATE="19950103", END_DATE="20220731")
# BOK_802Y001_19950103_20220731.to_pickle('./Market_Watch_Data/BOK_802Y001_19950103_20220731.pkl')

# BOK_802Y001_19950103_20220731 불러오기
BOK_802Y001_19950103_20220731 = pd.read_pickle('./Market_Watch_Data/BOK_802Y001_19950103_20220731.pkl')

# 업데이트 해서 이어붙이기
BOK_802Y001_UPDATE = get_bok_data(STAT_CODE="802Y001", CYCLE_TYPE="D", START_DATE="20220801", END_DATE=DD_END_DATE)
BOK_802Y001 = pd.concat([BOK_802Y001_19950103_20220731, BOK_802Y001_UPDATE])
BOK_802Y001 = BOK_802Y001.sort_values(by=['ITEM_CODE1', 'TIME'])
BOK_802Y001.to_pickle('./Market_Watch_Data/BOK_802Y001.pkl')
# BOK_802Y001_01 = BOK_802Y001[BOK_802Y001["ITEM_CODE1"] == "0001000"]  # KOSPI지수 / 코스피
# BOK_802Y001_02 = BOK_802Y001[BOK_802Y001["ITEM_CODE1"] == "0002000"]  # 거래량(주식시장, 잠정치)
# BOK_802Y001_03 = BOK_802Y001[BOK_802Y001["ITEM_CODE1"] == "0003000"]  # 거래대금(주식시장 , 잠정치)
# BOK_802Y001_04 = BOK_802Y001[BOK_802Y001["ITEM_CODE1"] == "0030000"]  # 외국인 순매수(주식시장, 잠정치)
# BOK_802Y001_05 = BOK_802Y001[BOK_802Y001["ITEM_CODE1"] == "0087000"]  # 주식시장-거래량(만주, 시간외거래분 포함)
# BOK_802Y001_06 = BOK_802Y001[BOK_802Y001["ITEM_CODE1"] == "0088000"]  # 주식시장-거래대금(억원, 시간외거래분 포함)
# BOK_802Y001_07 = BOK_802Y001[BOK_802Y001["ITEM_CODE1"] == "0089000"]  # KOSDAQ지수 / 코스닥
# BOK_802Y001_08 = BOK_802Y001[BOK_802Y001["ITEM_CODE1"] == "0090000"]  # 거래량(만주 : 코스닥시장, 잠정치)
# BOK_802Y001_09 = BOK_802Y001[BOK_802Y001["ITEM_CODE1"] == "0091000"]  # 거래대금(억원 : 코스닥시장, 잠정치)
# BOK_802Y001_10 = BOK_802Y001[BOK_802Y001["ITEM_CODE1"] == "0113000"]  # 외국인 순매수(코스닥시장, 잠정치)
# BOK_802Y001_11 = BOK_802Y001[BOK_802Y001["ITEM_CODE1"] == "0183000"]  # 시가총액(주식시장, 잠정치)

# 1.5.1.2. 주식/채권/재정 - 주식거래/주가지수 - 주식시장(월,년) [901Y014][A,M] (200002, 1976 부터)
BOK_901Y014 = get_bok_data(STAT_CODE="901Y014", CYCLE_TYPE="A", START_DATE="1976", END_DATE=YY_END_DATE)
BOK_901Y014.to_pickle('./Market_Watch_Data/BOK_901Y014.pkl')
BOK_901Y014_MM = get_bok_data(STAT_CODE="901Y014", CYCLE_TYPE="M", START_DATE="200002", END_DATE=MM_END_DATE)
BOK_901Y014_MM.to_pickle('./Market_Watch_Data/BOK_901Y014_MM.pkl')

########################################################################################################################
# 2.1.1.1. 국민소득통계(2015년 기준년) > 주요지표 > 주요지표(연간지표) [200Y001][A] (1953 부터)
BOK_200Y001 = get_bok_data(STAT_CODE="200Y001", CYCLE_TYPE="A", START_DATE="1970", END_DATE=YY_END_DATE)
BOK_200Y001.to_pickle('./Market_Watch_Data/BOK_200Y001.pkl')
# BOK_200Y001_00 = BOK_200Y001[BOK_200Y001["ITEM_CODE1"] == "10101"].copy()  # 국내총생산(GDP)(명목, 십억원)
# BOK_200Y001_01 = BOK_200Y001[BOK_200Y001["ITEM_CODE1"] == "1010101"].copy()  # 국내총생산(GDP)(명목, 억달러)
# BOK_200Y001_02 = BOK_200Y001[BOK_200Y001["ITEM_CODE1"] == "20101"].copy()  # 국내총생산(실질성장률)[%]
# BOK_200Y001_03 = BOK_200Y001[BOK_200Y001["ITEM_CODE1"] == "90103"].copy()  # GDP 디플레이터 (2015=100)
# BOK_200Y001_04 = BOK_200Y001[BOK_200Y001["ITEM_CODE1"] == "9010301"].copy()  # GDP 디플레이터 등락률 (%)

# 2.1.1.2. 국민소득통계(2015년 기준년) > 주요지표 > 주요지표(분기지표) [200Y002][Q] (1960Q1 부터)
BOK_200Y002 = get_bok_data(STAT_CODE="200Y002", CYCLE_TYPE="Q", START_DATE="1960Q1", END_DATE=QQ_END_DATE)
BOK_200Y002.to_pickle('./Market_Watch_Data/BOK_200Y002.pkl')
# BOK_200Y002_01 = BOK_200Y002[BOK_200Y002["ITEM_CODE1"] == "10111"].copy()  # 국내총생산(GDP)(실질, 계절조정, 전기비)

# 2.1.7.1.2. 가계의 목적별 최종소비지출(계절조정, 실질, 분기) [200Y041][Q] (1970Q1 부터)
BOK_200Y041 = get_bok_data(STAT_CODE="200Y041", CYCLE_TYPE="Q", START_DATE="1970Q1", END_DATE=QQ_END_DATE)
BOK_200Y041.to_pickle('./Market_Watch_Data/BOK_200Y041.pkl')
# BOK_200Y041_01 = BOK_111Y027[BOK_111Y027["ITEM_CODE1"] == "10116"].copy()  # 가계 최종소비지출

# 2.5.1.1. 국제수지 [301Y013][A,M,Q] (1980.01, 1980Q1 부터)
BOK_301Y013 = get_bok_data(STAT_CODE="301Y013", CYCLE_TYPE="M", START_DATE="198001", END_DATE=MM_END_DATE)
BOK_301Y013.to_pickle('./Market_Watch_Data/BOK_301Y013.pkl')
# BOK_301Y013_00 = BOK_301Y013[BOK_301Y013["ITEM_CODE1"] == "000000"].copy()  # 경상수지 (current account) (백만달러)

# 2.5.1.2. 경상수지(계절조정) [301Y017][M] (1980.01, 1980Q1 부터)
BOK_301Y017 = get_bok_data(STAT_CODE="301Y017", CYCLE_TYPE="M", START_DATE="198001", END_DATE=MM_END_DATE)
BOK_301Y017.to_pickle('./Market_Watch_Data/BOK_301Y017.pkl')
# BOK_022Y013_00 = BOK_022Y013[BOK_022Y013["ITEM_CODE1"] == "000000"].copy()  # 경상수지 (current account) (백만달러)

########################################################################################################################
# 3.1.2.1. 평균환율/기말환율 > 주요국통화의 대원화 환율 [731Y004][A,M,Q,S] (1964.05 부터)
BOK_731Y004 = get_bok_data(STAT_CODE="731Y004", CYCLE_TYPE="M", START_DATE="196405", END_DATE=MM_END_DATE)
BOK_731Y004.to_pickle('./Market_Watch_Data/BOK_731Y004.pkl')
# BOK_731Y004_00 = BOK_731Y004[(BOK_731Y004["ITEM_CODE1"] == "0000001") & (BOK_731Y004["ITEM_CODE2"] == "0000200")].copy()  # 원달러환율 말일자료
# BOK_731Y004_01 = BOK_731Y004[(BOK_731Y004["ITEM_CODE1"] == "0000001") & (BOK_731Y004["ITEM_CODE2"] == "0000200")].copy()  # 원/미국달러 말일자료

########################################################################################################################
# 4.1.1.1. 생산자물가지수(2015=100)(기본분류) [404Y014][A,M,Q] (1965.01 부터) (1910~1964 자료는 따로 있음)
BOK_404Y014 = get_bok_data(STAT_CODE="404Y014", CYCLE_TYPE="M", START_DATE="196501", END_DATE=MM_END_DATE)
BOK_404Y014.to_pickle('./Market_Watch_Data/BOK_404Y014.pkl')
# BOK_404Y014_AA = BOK_404Y014[BOK_404Y014["ITEM_CODE1"] == "*AA"].copy()  # 총지수
# BOK_404Y014_AA["pct_change_DATA_VALUE"] = (BOK_404Y014_AA["DATA_VALUE"].pct_change(12)) * 100  # 퍼센트 변화량 (전년비)

# 4.2.1 소비자물가지수(2020=100)(전국, 특수분류) [901Y010][A,M,Q] (1975.01 부터)
BOK_901Y010 = get_bok_data(STAT_CODE="901Y010", CYCLE_TYPE="M", START_DATE="197501", END_DATE=MM_END_DATE)
BOK_901Y010.to_pickle('./Market_Watch_Data/BOK_901Y010.pkl')

BOK_901Y010_YY = get_bok_data(STAT_CODE="901Y010", CYCLE_TYPE="A", START_DATE="1975", END_DATE=YY_END_DATE)
BOK_901Y010_YY.to_pickle('./Market_Watch_Data/BOK_901Y010_YY.pkl')
# BOK_901Y010_00 = BOK_901Y010[BOK_901Y010["ITEM_CODE1"] == "00"].copy()  # 총지수
# BOK_901Y010_QB = BOK_901Y010[BOK_901Y010["ITEM_CODE1"] == "QB"].copy()  # 농산물및석유류제외지수 (근원 소비자물가지수)
# BOK_901Y010_00["pct_change_DATA_VALUE"] = (BOK_901Y010_00["DATA_VALUE"].pct_change(12)) * 100  # 퍼센트 변화량 (전년비)
# BOK_901Y010_QB["pct_change_DATA_VALUE"] = (BOK_901Y010_QB["DATA_VALUE"].pct_change(12)) * 100  # 퍼센트 변화량 (전년비)

# 4.3.1.2. 수출물가지수(2015=100)(특수분류) [402Y015][A,M,Q] (1971.01 부터)
BOK_402Y015 = get_bok_data(STAT_CODE="402Y015", CYCLE_TYPE="M", START_DATE="197101", END_DATE=MM_END_DATE)
BOK_402Y015.to_pickle('./Market_Watch_Data/BOK_402Y015.pkl')
# BOK_402Y015_00 = BOK_402Y015[(BOK_402Y015["ITEM_CODE1"] == "602AA") &
#                              (BOK_402Y015["ITEM_CODE2"] == "D")].copy()  # 수출물가지수 (IT제외, 달러기준)

# 4.4.1.1. 주택매매가격지수(KB) [901Y062][M] (1986.01 부터)
BOK_901Y062 = get_bok_data(STAT_CODE="901Y062", CYCLE_TYPE="M", START_DATE="198601", END_DATE=MM_END_DATE)
BOK_901Y062.to_pickle('./Market_Watch_Data/BOK_901Y062.pkl')

########################################################################################################################
# 5.1.1.1. 기업경영분석 > 기업경영분석지표(연) > 기업경영분석지표 > 기업경영분석지표(2009~, 전수조사) [501Y011][A]
BOK_501Y011 = get_bok_data(STAT_CODE="501Y011", CYCLE_TYPE="A", START_DATE="2009", END_DATE=YY_END_DATE)
BOK_501Y011.to_pickle('./Market_Watch_Data/BOK_501Y011.pkl')
# BOK_501Y011_01 = BOK_501Y011[(BOK_501Y011["ITEM_NAME1"] == "전산업") & (BOK_501Y011["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
# BOK_501Y011_02 = BOK_501Y011[(BOK_501Y011["ITEM_NAME1"] == "제조업") & (BOK_501Y011["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
# BOK_501Y011_03 = BOK_501Y011[(BOK_501Y011["ITEM_NAME1"] == "제조업") & (BOK_501Y011["ITEM_NAME2"] == "매출액세전순이익률")].copy()  # 국내총생산(실질성장률)[%]

# 5.1.1.2. 기업경영분석 > 기업경영분석지표(연) > 기업경영분석지표 > 기업경영분석지표(2007~2010) [501Y017][A]
BOK_501Y017 = get_bok_data(STAT_CODE="501Y017", CYCLE_TYPE="A", START_DATE="2007", END_DATE="2010")
BOK_501Y017.to_pickle('./Market_Watch_Data/BOK_501Y017.pkl')
# BOK_501Y017_01 = BOK_501Y017[(BOK_501Y017["ITEM_NAME1"] == "전산업") & (BOK_501Y017["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
# BOK_501Y017_02 = BOK_501Y017[(BOK_501Y017["ITEM_NAME1"] == "제조업") & (BOK_501Y017["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
# BOK_501Y017_03 = BOK_501Y017[(BOK_501Y017["ITEM_NAME1"] == "제조업") & (BOK_501Y017["ITEM_NAME2"] == "매출액세전순이익률")].copy()  # 국내총생산(실질성장률)[%]

# 5.1.1.3. 기업경영분석 > 기업경영분석지표(연) > 기업경영분석지표 > 기업경영분석지표(~2007) [501Y018][A]
BOK_501Y018 = get_bok_data(STAT_CODE="501Y018", CYCLE_TYPE="A", START_DATE="1960", END_DATE="2007")
BOK_501Y018.to_pickle('./Market_Watch_Data/BOK_501Y018.pkl')
# BOK_501Y018_01 = BOK_501Y018[(BOK_501Y018["ITEM_NAME1"] == "전산업") & (BOK_501Y018["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
# BOK_501Y018_02 = BOK_501Y018[(BOK_501Y018["ITEM_NAME1"] == "제조업") & (BOK_501Y018["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
# BOK_501Y018_03 = BOK_501Y018[(BOK_501Y018["ITEM_NAME1"] == "제조업") & (BOK_501Y018["ITEM_NAME2"] == "매출액경상이익률(~2006)")].copy()  # 국내총생산(실질성장률)[%]

########################################################################################################################
# # 분기별 GDP 갭을 추정해보려 하였으나 실패
# # 10.2.1.2 국민계정(2015년 기준년) - 경제활동별, 지출항목별 규모 - 경제활동별 GDP 및 GNI
# # - 경제활동별 GDP 및 GNI(계절조정, 실질, 분기) [111Y013][QQ] (1960Q1 부터)
# BOK_111Y013 = get_BOK__data(STAT_CODE="111Y011", CYCLE_TYPE="QQ", START_DATE="19601", END_DATE=QQ_END_DATE)
# BOK111Y013.groupby(["ITEM_CODE1", "ITEM_NAME1"]).size()
#
# BOK111Y013_00 = BOK111Y013[BOK111Y013["ITEM_CODE1"] == "1400"].copy()  # 국내총생산(시장가격, GDP)(실질, 십억원)
# BOK111Y013_00["Year"], BOK111Y013_00["Quarter"] = BOK111Y013_00["TIME"].divmod(10)
# BOK111Y013_00["YYYYMMDD"] = BOK111Y013_00["Year"] * 10000 + (BOK111Y013_00["Quarter"] * 3 - 2) * 100 + 1
# BOK111Y013_00["DATETIME"] = pd.to_datetime(BOK111Y013_00['YYYYMMDD'].astype(str), errors='coerce', format='%Y%m%d')
#
# # BOK111Y013_00["Real_GDP"] = BOK111Y013_00["DATA_VALUE"].copy()  # 국내총생산(GDP)(실질, 십억원)
# BOK111Y013_00["Real_GDP"] = BOK111Y013_00["DATA_VALUE"].rolling(window=4).sum()  # 4분기 누적
#
# BOK111Y013_00a = BOK111Y013_00[BOK111Y013_00["Year"] >= 1970].copy()
#
# cycle, trend = sm.tsa.filters.hpfilter(BOK111Y013_00a["Real_GDP"], 50)
# BOK111Y013_00a["Potential_GDP"] = trend
# BOK111Y013_00a["GDP_Gap"] = ((BOK111Y013_00a["Real_GDP"] - BOK111Y013_00a["Potential_GDP"]) / BOK111Y013_00a["Potential_GDP"]) * 100  # GDP 갭 (%)
#
#
# # 그림: 분기별 GDP 갭 (%)
# # 시각화: 분기별 시계열 자료 1개를 표시
# fig = plt.figure()
# fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
# plt.plot(BOK111Y013_00a["DATETIME"], BOK111Y013_00a["GDP_Gap"], color='r', label="GDP_Gap")
#
# xlim_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')
# plt.xlim(xlim_start, )
# plt.ylim(-10, 20)
# plt.axhline(y=0, color='green', linestyle='dotted')
# plt.xlabel('Dates', fontsize=10)
# plt.ylabel('Current Account to GDP (%)', fontsize=10)
# plt.legend(loc='upper left')
# plt.show()
#
# plt.savefig("./BOK_processed/fig_current_account_to_gdp.png")
#
#
#
# ########################################################################################################################
# # 시각화
# plt.plot(BOK064Y001_01["DATETIME"], BOK064Y001_01["DATA_VALUE"], color='r', label="KOSPI")
# plt.plot(BOK064Y001_02["DATETIME"], BOK064Y001_02["DATA_VALUE"], color='g', label="KOSPI(volume)")
# plt.xlabel('Dates', fontsize=10)
# plt.ylabel('Rates (%)', fontsize=10)
# plt.legend(loc='upper left')
# plt.show()
#
# # 시각화
# fig, (ax1, ax2) = plt.subplots(2, sharex=True)
# fig.suptitle('Aligning x-axis using sharex')
# ax1.plot(BOK064Y001_01["DATETIME"], BOK064Y001_01["DATA_VALUE"], color='b', label="KOSPI")
# plt.legend(loc='upper left')
# ax2.plot(BOK064Y001_02["DATETIME"], BOK064Y001_02["DATA_VALUE"], color='g', label="KOSPI(volume)")
# plt.legend(loc='upper left')
# plt.show()
#
# BOK064Y001.groupby(["ITEM_CODE1", "ITEM_NAME1"]).size()
#
# ########################################################################################################################
# # 4.1.1 시장금리(일별) [060Y001] (1995.01.03 부터)
# BOK060Y001 = get_bok_data(STAT_CODE="060Y001", CYCLE_TYPE="DD", START_DATE="19950103", END_DATE="19970103")
# BOK060Y001_01 = BOK060Y001[BOK060Y001["ITEM_NAME1"] == "CD(91일)"]
#
# # 4.1.2 시장금리(월,분기,년) [028Y001] (1987.01, 1987Q1, 1987 부터)
# BOK028Y001 = get_bok_data(STAT_CODE="028Y001", CYCLE_TYPE="MM", START_DATE="198701", END_DATE="201912")
# BOK028Y001_01 = BOK028Y001[BOK028Y001["ITEM_NAME1"] == "국고채(3년)"]
#
# # 4.2.2.1 예금은행 가중평균금리 - 대출금리 - 신규취급액 기준 [005Y003] (1996.01 부터)
# BOK005Y003 = get_bok_data(STAT_CODE="005Y003", CYCLE_TYPE="MM", START_DATE="199601", END_DATE=MM_END_DATE)
# BOK005Y003_01 = BOK005Y003[BOK005Y003["ITEM_NAME1"] == " 주택담보대출"]
#
#
# # 시각화
# plt.plot(BOK005Y003_01["DATETIME"], BOK005Y003_01["DATA_VALUE"], color='g', label="Mortgage Rate")
# plt.plot(BOK028Y001_01["DATETIME"], BOK028Y001_01["DATA_VALUE"], color='y', label="KTB3Y")
# plt.xlabel('Dates', fontsize=10)
# plt.ylabel('Rates (%)', fontsize=10)
# plt.legend(loc='upper left')
# plt.show()
#
# BOK028Y001["ITEM_NAME1"].value_counts()
#
#
# # 7.7.1 주택매매가격지수(KB) [085Y021] 2019.01 = 100
# BOK085Y021 = get_bok_data(STAT_CODE="085Y021", CYCLE_TYPE="MM", START_DATE=MM_START_DATE, END_DATE=MM_END_DATE)
#
# # 전체자료: 9.1.1.1 기업경기실사지수(BSI)-전국실적 (STAT_CODE="041Y013")
# BOK041Y013 = get_bok_data(STAT_CODE="041Y013", CYCLE_TYPE="MM", START_DATE=MM_START_DATE, END_DATE=MM_END_DATE)
#
# # 전체자료: 9.1.1.2 기업경기실사지수(BSI)-전국전망
# BOK041Y014 = get_bok_data(STAT_CODE="041Y014", CYCLE_TYPE="MM", START_DATE=MM_START_DATE, END_DATE=MM_END_DATE)
#
# # 전체자료: 12.15.1 기업경영분석(분기) - 성장성에 관한 지표(027Y215)
# BOK027Y215 = get_bok_data(STAT_CODE="027Y215", CYCLE_TYPE="QQ", START_DATE=QQ_START_DATE, END_DATE=QQ_END_DATE)
#
# # 전체자료: 15.1 대출행태서베이 - 대출태도(093Y001)
# BOK093Y001 = get_bok_data(STAT_CODE="093Y001", CYCLE_TYPE="QQ", START_DATE=QQ_START_DATE, END_DATE=QQ_END_DATE)
#
# # 전체자료: 15.2 대출행태서베이 - 신용위험(093Y002)
# BOK093Y002 = get_bok_data(STAT_CODE="093Y002", CYCLE_TYPE="QQ", START_DATE=QQ_START_DATE, END_DATE=QQ_END_DATE)
#
# # 전체자료: 3.6.1 가계신용(분기별)
# BOK008Y001 = get_bok_data(STAT_CODE="008Y001", CYCLE_TYPE="QQ", START_DATE=QQ_START_DATE, END_DATE=QQ_END_DATE)
#
# ########################################################################################################################
# STAT_CODE="060Y001"
# CYCLE_TYPE="DD"
# START_DATE="19950103"
# END_DATE="19970103"
# AUTH_KEY=get_bok_auth_key()
# REQ_TYPE="xml"
# LANG="kr"
# START_COUNT="1"
# END_COUNT="100000"
# ITEM_1="?"
# ITEM_2="?"
# ITEM_3="?"
#
# # 호출하려는 OpenAPI URL 정의
# BOK_url = "".join(
#     ["http://ecos.bok.or.kr/api/StatisticSearch/", AUTH_KEY, "/", REQ_TYPE, "/", LANG, "/", START_COUNT, "/",
#      END_COUNT, "/", STAT_CODE, "/", CYCLE_TYPE, "/", START_DATE, "/", END_DATE, "/", ITEM_1, "/", ITEM_2, "/",
#      ITEM_3])
# # 정의된 OpenAPI URL을 호출합니다.
# BOK_response = requests.get(BOK_url)
#
# BOK_xml = BeautifulSoup(BOK_response.text, "xml")
# BOK_xml_row = BOK_xml.find_all("row")
#
# print(BOK_xml_row[1])
#
# list_STAT_CODE = []
# list_STAT_NAME = []
# list_ITEM_CODE1 = []
# list_ITEM_NAME1 = []
# list_ITEM_CODE2 = []
# list_ITEM_NAME2 = []
# list_ITEM_CODE3 = []
# list_ITEM_NAME3 = []
# list_UNIT_NAME = []
# list_TIME = []
# list_DATA_VALUE = []
# list_DATETIME = []
#
# for item in BOK_xml_row:
#     item_STAT_CODE = item.find("STAT_CODE").text
#     item_STAT_NAME = item.find("STAT_NAME").text
#     item_ITEM_CODE1 = item.find("ITEM_CODE1").text
#     item_ITEM_NAME1 = item.find("ITEM_NAME1").text
#     item_ITEM_CODE2 = item.find("ITEM_CODE2").text
#     item_ITEM_NAME2 = item.find("ITEM_NAME2").text
#     item_ITEM_CODE3 = item.find("ITEM_CODE3").text
#     item_ITEM_NAME3 = item.find("ITEM_NAME3").text
#     item_UNIT_NAME = item.find("UNIT_NAME").text
#     item_TIME = item.find("TIME").text
#     item_DATA_VALUE = item.find("DATA_VALUE").text
#     item_DATETIME = datetime.datetime.strptime(item_TIME, "%Y%m%d")
#
#     try:
#         item_DATA_VALUE = float(item_DATA_VALUE)
#     except:
#         item_DATA_VALUE = np.nan
#
#     list_STAT_CODE.append(item_STAT_CODE)
#     list_STAT_NAME.append(item_STAT_NAME)
#     list_ITEM_CODE1.append(item_ITEM_CODE1)
#     list_ITEM_NAME1.append(item_ITEM_NAME1)
#     list_ITEM_CODE2.append(item_ITEM_CODE2)
#     list_ITEM_NAME2.append(item_ITEM_NAME2)
#     list_ITEM_CODE3.append(item_ITEM_CODE3)
#     list_ITEM_NAME3.append(item_ITEM_NAME3)
#     list_UNIT_NAME.append(item_UNIT_NAME)
#     list_TIME.append(item_TIME)
#     list_DATA_VALUE.append(item_DATA_VALUE)
#     list_DATETIME.append(item_DATETIME)
#
# df_BOK = pd.DataFrame(list_STAT_CODE, columns=["STAT_CODE"])
# df_BOK["STAT_NAME"] = list_STAT_NAME
# df_BOK["ITEM_CODE1"] = list_ITEM_CODE1
# df_BOK["ITEM_NAME1"] = list_ITEM_NAME1
# df_BOK["ITEM_CODE2"] = list_ITEM_CODE2
# df_BOK["ITEM_NAME2"] = list_ITEM_NAME2
# df_BOK["ITEM_CODE3"] = list_ITEM_CODE3
# df_BOK["ITEM_NAME3"] = list_ITEM_NAME3
# df_BOK["UNIT_NAME"] = list_UNIT_NAME
# df_BOK["TIME"] = list_TIME
# df_BOK["DATA_VALUE"] = list_DATA_VALUE
# df_BOK["DATETIME"] = list_DATETIME
# df_BOK["TIME"] = df_BOK["TIME"].apply(pd.to_numeric)

