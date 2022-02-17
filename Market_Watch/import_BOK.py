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


DD_END_DATE = "20220215"
MM_END_DATE = "202201"
QQ_END_DATE = "20214"
YY_END_DATE = "2021"

# MM_START_DATE = "200301"
# QQ_START_DATE = "20031"

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
# 2.6 한국은행 기준금리 및 여수신금리 [098Y001][DD, MM, QQ, YY] (1994.01.03 부터)
BOK_098Y001_DD = get_bok_data(STAT_CODE="098Y001", CYCLE_TYPE="DD", START_DATE="19940103", END_DATE=DD_END_DATE)
BOK_098Y001_DD.to_pickle('./Market_Watch_Data/BOK_098Y001_DD.pkl')

# 4.1.1 시장금리(일별) [060Y001] (1995.01.03 부터)
BOK_060Y001 = get_bok_data(STAT_CODE="060Y001", CYCLE_TYPE="DD", START_DATE="19950103", END_DATE=DD_END_DATE)
BOK_060Y001.to_pickle('./Market_Watch_Data/BOK_060Y001.pkl')

# 4.1.2 시장금리(월,분기,년) [028Y001] (1987.01, 1987Q1, 1987 부터)
BOK_028Y001 = get_bok_data(STAT_CODE="028Y001", CYCLE_TYPE="MM", START_DATE="198701", END_DATE=MM_END_DATE)
BOK_028Y001.to_pickle('./Market_Watch_Data/BOK_028Y001.pkl')

# 4.2.1.1 예금은행 가중평균금리 - 수신금리 - 신규취급액 기준 [005Y001] (1996.01 부터)
BOK_005Y001 = get_bok_data(STAT_CODE="005Y001", CYCLE_TYPE="MM", START_DATE="199601", END_DATE=MM_END_DATE)
BOK_005Y001.to_pickle('./Market_Watch_Data/BOK_005Y001.pkl')

# 4.2.2.1 예금은행 가중평균금리 - 대출금리 - 신규취급액 기준 [005Y003] (1996.01 부터)
BOK_005Y003 = get_bok_data(STAT_CODE="005Y003", CYCLE_TYPE="MM", START_DATE="199601", END_DATE=MM_END_DATE)
BOK_005Y003.to_pickle('./Market_Watch_Data/BOK_005Y003.pkl')

BOK_060Y001_01 = BOK_060Y001[BOK_060Y001["ITEM_NAME1"] == "CD(91일)"]
BOK_028Y001_01 = BOK_028Y001[BOK_028Y001["ITEM_NAME1"] == "국고채(5년)"]
BOK_005Y003_01 = BOK_005Y003[BOK_005Y003["ITEM_NAME1"] == " 주택담보대출"]

########################################################################################################################
# 6.1.1 증권/재정 - 주식거래 및 주가지수 - 주식시장(일별) [064Y001] (1995.01.03 부터)
# BOK_064Y001_19950103_20210131 불러오기
BOK_064Y001_19950103_20210131 = pd.read_pickle('./Market_Watch_Data/BOK_064Y001_19950103_20210131.pkl')

BOK_064Y001_UPDATE = get_bok_data(STAT_CODE="064Y001", CYCLE_TYPE="DD", START_DATE="20210201", END_DATE=DD_END_DATE)
BOK_064Y001 = pd.concat([BOK_064Y001_19950103_20210131, BOK_064Y001_UPDATE])
BOK_064Y001 = BOK_064Y001.sort_values(by=['ITEM_CODE1', 'TIME'])
BOK_064Y001.to_pickle('./Market_Watch_Data/BOK_064Y001.pkl')
# BOK_064Y001_01 = BOK_064Y001[BOK_064Y001["ITEM_CODE1"] == "0001000"]  # KOSPI지수
# BOK_064Y001_02 = BOK_064Y001[BOK_064Y001["ITEM_CODE1"] == "0002000"]  # 거래량(주식시장, 잠정치)
# BOK_064Y001_03 = BOK_064Y001[BOK_064Y001["ITEM_CODE1"] == "0003000"]  # 거래대금(주식시장 , 잠정치)
# BOK_064Y001_04 = BOK_064Y001[BOK_064Y001["ITEM_CODE1"] == "0030000"]  # 외국인 순매수(주식시장, 잠정치)
# BOK_064Y001_05 = BOK_064Y001[BOK_064Y001["ITEM_CODE1"] == "0087000"]  # 주식시장-거래량(만주, 시간외거래분 포함)
# BOK_064Y001_06 = BOK_064Y001[BOK_064Y001["ITEM_CODE1"] == "0088000"]  # 주식시장-거래대금(억원, 시간외거래분 포함)
# BOK_064Y001_07 = BOK_064Y001[BOK_064Y001["ITEM_CODE1"] == "0089000"]  # KOSDAQ지수
# BOK_064Y001_08 = BOK_064Y001[BOK_064Y001["ITEM_CODE1"] == "0090000"]  # 거래량(만주 : 코스닥시장, 잠정치)
# BOK_064Y001_09 = BOK_064Y001[BOK_064Y001["ITEM_CODE1"] == "0091000"]  # 거래대금(억원 : 코스닥시장, 잠정치)
# BOK_064Y001_10 = BOK_064Y001[BOK_064Y001["ITEM_CODE1"] == "0113000"]  # 외국인 순매수(코스닥시장, 잠정치)
# BOK_064Y001_11 = BOK_064Y001[BOK_064Y001["ITEM_CODE1"] == "0183000"]  # 시가총액(주식시장, 잠정치)

# 6.1.2 증권/재정 - 주식거래 및 주가지수 [028Y015][MM, YY] (200002, 1976 부터)
BOK_028Y015 = get_bok_data(STAT_CODE="028Y015", CYCLE_TYPE="YY", START_DATE="1976", END_DATE="2020")
BOK_028Y015.to_pickle('./Market_Watch_Data/BOK_028Y015.pkl')
# BOK_028Y015_01 = BOK_028Y015[BOK_028Y015["ITEM_NAME1"] == "KOSPI_종가"].copy()  # 국내총생산(GDP)(실질, 원계열, 전년동기)
BOK_028Y015_MM = get_bok_data(STAT_CODE="028Y015", CYCLE_TYPE="MM", START_DATE="200002", END_DATE=MM_END_DATE)
BOK_028Y015_MM.to_pickle('./Market_Watch_Data/BOK_028Y015_MM.pkl')


# 7.1.1 생산자물가지수(2015=100)(기본분류)  [013Y202][MM,QQ,YY] (1965.01 부터)
BOK_013Y202 = get_bok_data(STAT_CODE="013Y202", CYCLE_TYPE="MM", START_DATE="196501", END_DATE=MM_END_DATE)
BOK_013Y202.to_pickle('./Market_Watch_Data/BOK_013Y202.pkl')
# BOK_013Y202_AA = BOK_013Y202[BOK_013Y202["ITEM_CODE1"] == "*AA"].copy()  # 총지수
# BOK_013Y202_AA["pct_change_DATA_VALUE"] = (BOK_013Y202_AA["DATA_VALUE"].pct_change(12)) * 100  # 퍼센트 변화량 (전년비)

# 7.4.2 소비자물가지수(2015=100)(전국, 특수분류)  [021Y126][MM,QQ,YY] (1975.01 부터)
BOK_021Y126 = get_bok_data(STAT_CODE="021Y126", CYCLE_TYPE="MM", START_DATE="197501", END_DATE=MM_END_DATE)
BOK_021Y126.to_pickle('./Market_Watch_Data/BOK_021Y126.pkl')

BOK_021Y126_YY = get_bok_data(STAT_CODE="021Y126", CYCLE_TYPE="YY", START_DATE="1975", END_DATE=YY_END_DATE)
BOK_021Y126_YY.to_pickle('./Market_Watch_Data/BOK_021Y126_YY.pkl')
# BOK_021Y126_00 = BOK_021Y126[BOK_021Y126["ITEM_CODE1"] == "00"].copy()  # 총지수
# BOK_021Y126_QB = BOK_021Y126[BOK_021Y126["ITEM_CODE1"] == "QB"].copy()  # 농산물및석유류제외지수 (근원 소비자물가지수)
# BOK_021Y126_00["pct_change_DATA_VALUE"] = (BOK_021Y126_00["DATA_VALUE"].pct_change(12)) * 100  # 퍼센트 변화량 (전년비)
# BOK_021Y126_QB["pct_change_DATA_VALUE"] = (BOK_021Y126_QB["DATA_VALUE"].pct_change(12)) * 100  # 퍼센트 변화량 (전년비)

# 8.1.1 국제수지 [022Y013][MM,QQ,YY] (1980.01, 1980Q1 부터)
BOK_022Y013 = get_bok_data(STAT_CODE="022Y013", CYCLE_TYPE="MM", START_DATE="198001", END_DATE=MM_END_DATE)
BOK_022Y013.to_pickle('./Market_Watch_Data/BOK_022Y013.pkl')
# BOK_022Y013_00 = BOK_022Y013[BOK_022Y013["ITEM_CODE1"] == "000000"].copy()  # 경상수지 (current account) (백만달러)

# 8.8.2.1 평균환율, 기말환율 > 주요국통화의 대원화 환율 통계자료 [036Y004][HY,MM,QQ,YY] (1964.05 부터)
BOK_036Y004 = get_bok_data(STAT_CODE="036Y004", CYCLE_TYPE="MM", START_DATE="196405", END_DATE=MM_END_DATE)
BOK_036Y004.to_pickle('./Market_Watch_Data/BOK_036Y004.pkl')
# BOK_036Y004_00 = BOK_036Y004[(BOK_036Y004["ITEM_CODE1"] == "0000001") & (BOK_036Y004["ITEM_CODE2"] == "0000200")].copy()  # 원달러환율 말일자료
# BOK_036Y004_01 = BOK_036Y004[(BOK_036Y004["ITEM_CODE1"] == "0000001") & (BOK_036Y004["ITEM_CODE2"] == "0000200")].copy()  # 원/미국달러 말일자료


########################################################################################################################
# 10.1.1 국민계정(2015년 기준년) - 주요지표 - 연간지표 [111Y002][YY] (1953 부터)
BOK_111Y002 = get_bok_data(STAT_CODE="111Y002", CYCLE_TYPE="YY", START_DATE="1970", END_DATE=YY_END_DATE)
BOK_111Y002.to_pickle('./Market_Watch_Data/BOK_111Y002.pkl')
# BOK_111Y002_00 = BOK_111Y002[BOK_111Y002["ITEM_CODE1"] == "10101"].copy()  # 국내총생산(GDP)(명목, 십억원)
# BOK_111Y002_01 = BOK_111Y002[BOK_111Y002["ITEM_CODE1"] == "1010101"].copy()  # 국내총생산(GDP)(명목, 억달러)
# BOK_111Y002_02 = BOK_111Y002[BOK_111Y002["ITEM_CODE1"] == "20101"].copy()  # 국내총생산(실질성장률)[%]
# BOK_111Y002_03 = BOK_111Y002[BOK_111Y002["ITEM_CODE1"] == "90103"].copy()  # GDP 디플레이터 (2015=100)
# BOK_111Y002_04 = BOK_111Y002[BOK_111Y002["ITEM_CODE1"] == "9010301"].copy()  # GDP 디플레이터 등락률 (%)

# 10.1.2 국민계정(2015년 기준년) - 주요지표 - 분기지표 [111Y055] (1960Q1 부터)
BOK_111Y055 = get_bok_data(STAT_CODE="111Y055", CYCLE_TYPE="QQ", START_DATE="19601", END_DATE=QQ_END_DATE)
BOK_111Y055.to_pickle('./Market_Watch_Data/BOK_111Y055.pkl')
# BOK_111Y055_01 = BOK_111Y055[BOK_111Y055["ITEM_CODE1"] == "10111"].copy()  # 국내총생산(GDP)(실질, 계절조정, 전기비)

# 10.7.1.1.2. 가계의 목적별 최종소비지출(계절조정, 실질, 분기) [111Y027] (1970Q1 부터)
BOK_111Y027 = get_bok_data(STAT_CODE="111Y027", CYCLE_TYPE="QQ", START_DATE="19701", END_DATE=QQ_END_DATE)
BOK_111Y027.to_pickle('./Market_Watch_Data/BOK_111Y027.pkl')
# BOK_111Y027_01 = BOK_111Y027[BOK_111Y027["ITEM_CODE1"] == "10116"].copy()  # 가계 최종소비지출

# 12.1.1 기업경영분석 - 기업경영분석지표 - 기업경영분석지표(~2007)[027Y131][YY] (1960 부터)
BOK_027Y131 = get_bok_data(STAT_CODE="027Y131", CYCLE_TYPE="YY", START_DATE="1960", END_DATE="2006")
BOK_027Y131.to_pickle('./Market_Watch_Data/BOK_027Y131.pkl')
# BOK_027Y131_01 = BOK_027Y131[(BOK_027Y131["ITEM_NAME1"] == "전산업") & (BOK_027Y131["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
# BOK_027Y131_02 = BOK_027Y131[(BOK_027Y131["ITEM_NAME1"] == "제조업") & (BOK_027Y131["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
# BOK_027Y131_03 = BOK_027Y131[(BOK_027Y131["ITEM_NAME1"] == "제조업") & (BOK_027Y131["ITEM_NAME2"] == "매출액경상이익률(~2006)")].copy()  # 국내총생산(실질성장률)[%]

# 12.1.1 기업경영분석 - 기업경영분석지표 - 기업경영분석지표(2007~2010)[027Y331][YY]
BOK_027Y331 = get_bok_data(STAT_CODE="027Y331", CYCLE_TYPE="YY", START_DATE="2007", END_DATE="2008")
BOK_027Y331.to_pickle('./Market_Watch_Data/BOK_027Y331.pkl')
# BOK_027Y331_01 = BOK_027Y331[(BOK_027Y331["ITEM_NAME1"] == "전산업") & (BOK_027Y331["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
# BOK_027Y331_02 = BOK_027Y331[(BOK_027Y331["ITEM_NAME1"] == "제조업") & (BOK_027Y331["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
# BOK_027Y331_03 = BOK_027Y331[(BOK_027Y331["ITEM_NAME1"] == "제조업") & (BOK_027Y331["ITEM_NAME2"] == "매출액세전순이익률")].copy()  # 국내총생산(실질성장률)[%]

# 12.1.1 기업경영분석 - 기업경영분석지표 - 기업경영분석지표(2009~, 전수조사) [027Y431][YY]
BOK_027Y431 = get_bok_data(STAT_CODE="027Y431", CYCLE_TYPE="YY", START_DATE="2009", END_DATE="2020")
BOK_027Y431.to_pickle('./Market_Watch_Data/BOK_027Y431.pkl')
# BOK_027Y431_01 = BOK_027Y431[(BOK_027Y431["ITEM_NAME1"] == "전산업") & (BOK_027Y431["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
# BOK_027Y431_02 = BOK_027Y431[(BOK_027Y431["ITEM_NAME1"] == "제조업") & (BOK_027Y431["ITEM_NAME2"] == "매출액영업이익률")].copy()  # 국내총생산(실질성장률)[%]
# BOK_027Y431_03 = BOK_027Y431[(BOK_027Y431["ITEM_NAME1"] == "제조업") & (BOK_027Y431["ITEM_NAME2"] == "매출액세전순이익률")].copy()  # 국내총생산(실질성장률)[%]

# BOK_028Y015.groupby(["ITEM_CODE1", "ITEM_NAME1"]).size()

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

