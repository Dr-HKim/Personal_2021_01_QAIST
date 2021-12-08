# Created by Kim Hyeongjun on 03/22/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.
# 데이터가이드 일간 데이터 엑셀을 불러와서 Pickle 형태로 저장
# 20000101_20201231 약 2시간 30분 소요
# 20210101_Current 약 30분 소요

import pandas as pd
from datetime import datetime


########################################################################################################################
# 데이터가이드 일간 데이터 불러오기
# 파일: DG_DAILY_20000101_20201231.xlsx
# 날짜: 2000-01-01 ~ 2020-12-31
# Sheet DG_DAILY1: 기준가(원), 시가(원), 고가(원), 저가(원), 종가(원)
# Sheet DG_DAILY2: 수정시가(원), 수정고가(원), 수정저가(원), 수정주가(원), 수정계수
# Sheet DG_DAILY3: 거래량(주), 거래대금(원), 상장주식수(주), 상장예정주식수(주), 외국인보유주식수(티커)(주)
# 자료: B:WOM
# A9: Symbol (A000010)
# A10: Symbol Name (조흥은행)
# A11: Kind (SSC)
# A12: Item (S410000200)
# A13: Item Name (기준가(원))
# A14: Frequency (DAILY)
# A15: 날짜 시작 (2000-01-04)
# A5198: 날짜 종료 (2020-12-30)


# StopWatch: 코드 시작
time_start = datetime.now()
print("Procedure started at: " + str(time_start))

# 각 1시간 41분씩 총 5시간 소요
dg_daily1_data_20000101_20201231 = pd.read_excel(
    './DataGuide/DG_DAILY1_20000101_20201231.xlsx', sheet_name="DAILY1", header=None, skiprows=14, skipfooter=0)
dg_daily1_data_20000101_20201231.to_pickle('./DataGuide_processed/dg_daily1_data_20000101_20201231.pkl')

dg_daily1_header_20000101_20201231 = pd.read_excel(
    './DataGuide/DG_DAILY1_20000101_20201231.xlsx', sheet_name="DAILY1", header=None, skiprows=8, nrows=6)
dg_daily1_header_20000101_20201231.to_pickle('./DataGuide_processed/dg_daily1_header_20000101_20201231.pkl')

# StopWatch
time_tmp1 = datetime.now()
print("Load Daily1 finished at: " + str(time_tmp1))
print("Elapsed (in total): " + str(time_tmp1 - time_start))

dg_daily2_data_20000101_20201231 = pd.read_excel(
    './DataGuide/DG_DAILY2_20000101_20201231.xlsx', sheet_name="DAILY2", header=None, skiprows=14, skipfooter=0)
dg_daily2_data_20000101_20201231.to_pickle('./DataGuide_processed/dg_daily2_data_20000101_20201231.pkl')

dg_daily2_header_20000101_20201231 = pd.read_excel(
    './DataGuide/DG_DAILY2_20000101_20201231.xlsx', sheet_name="DAILY2", header=None, skiprows=8, nrows=6)
dg_daily2_header_20000101_20201231.to_pickle('./DataGuide_processed/dg_daily2_header_20000101_20201231.pkl')

dg_daily3_data_20000101_20201231 = pd.read_excel(
    './DataGuide/DG_DAILY3_20000101_20201231.xlsx', sheet_name="DAILY3", header=None, skiprows=14, skipfooter=0)
dg_daily3_data_20000101_20201231.to_pickle('./DataGuide_processed/dg_daily3_data_20000101_20201231.pkl')

dg_daily3_header_20000101_20201231 = pd.read_excel(
    './DataGuide/DG_DAILY3_20000101_20201231.xlsx', sheet_name="DAILY3", header=None, skiprows=8, nrows=6)
dg_daily3_header_20000101_20201231.to_pickle('./DataGuide_processed/dg_daily3_header_20000101_20201231.pkl')

dg_daily4_data_20000101_20201231 = pd.read_excel(
    './DataGuide/DG_DAILY4_20000101_20201231.xlsx', sheet_name="DAILY4", header=None, skiprows=14, skipfooter=0)
dg_daily4_data_20000101_20201231.to_pickle('./DataGuide_processed/dg_daily4_data_20000101_20201231.pkl')

dg_daily4_header_20000101_20201231 = pd.read_excel(
    './DataGuide/DG_DAILY4_20000101_20201231.xlsx', sheet_name="DAILY4", header=None, skiprows=8, nrows=6)
dg_daily4_header_20000101_20201231.to_pickle('./DataGuide_processed/dg_daily4_header_20000101_20201231.pkl')

# StopWatch
time_tmp4 = datetime.now()
print("Load Daily4 finished at: " + str(time_tmp4))
print("Elapsed (in total): " + str(time_tmp4 - time_start))

dg_daily5_data_20000101_20201231 = pd.read_excel(
    './DataGuide/DG_DAILY5_20000101_20201231.xlsx', sheet_name="DAILY5", header=None, skiprows=14, skipfooter=0)
dg_daily5_data_20000101_20201231.to_pickle('./DataGuide_processed/dg_daily5_data_20000101_20201231.pkl')

dg_daily5_header_20000101_20201231 = pd.read_excel(
    './DataGuide/DG_DAILY5_20000101_20201231.xlsx', sheet_name="DAILY5", header=None, skiprows=8, nrows=6)
dg_daily5_header_20000101_20201231.to_pickle('./DataGuide_processed/dg_daily5_header_20000101_20201231.pkl')

# StopWatch
time_tmp5 = datetime.now()
print("Load Daily5 finished at: " + str(time_tmp5))
print("Elapsed (in total): " + str(time_tmp5 - time_start))

dg_daily7_data_20000101_20201231 = pd.read_excel(
    './DataGuide/DG_DAILY7_20000101_20201231.xlsx', sheet_name="DAILY7", header=None, skiprows=14, skipfooter=0)
dg_daily7_data_20000101_20201231.to_pickle('./DataGuide_processed/dg_daily7_data_20000101_20201231.pkl')

dg_daily7_header_20000101_20201231 = pd.read_excel(
    './DataGuide/DG_DAILY7_20000101_20201231.xlsx', sheet_name="DAILY7", header=None, skiprows=8, nrows=6)
dg_daily7_header_20000101_20201231.to_pickle('./DataGuide_processed/dg_daily7_header_20000101_20201231.pkl')

# StopWatch
time_tmp7 = datetime.now()
print("Load Daily7 finished at: " + str(time_tmp7))
print("Elapsed (in total): " + str(time_tmp7 - time_start))

########################################################################################################################
# 데이터가이드 일간 데이터 불러오기
# 파일: DG_DAILY_20210101_Current.xlsx
# 날짜: 2021-01-01 ~ Current

# StopWatch: 코드 시작
time_start = datetime.now()
print("Procedure started at: " + str(time_start))

dg_daily1_data_20210101_Current = pd.read_excel(
    './DataGuide/DG_DAILY_20210101_Current.xlsx', sheet_name="DAILY1", header=None, skiprows=14, skipfooter=0)
dg_daily1_data_20210101_Current.to_pickle('./DataGuide_processed/dg_daily1_data_20210101_Current.pkl')

dg_daily2_data_20210101_Current = pd.read_excel(
    './DataGuide/DG_DAILY_20210101_Current.xlsx', sheet_name="DAILY2", header=None, skiprows=14, skipfooter=0)
dg_daily2_data_20210101_Current.to_pickle('./DataGuide_processed/dg_daily2_data_20210101_Current.pkl')

dg_daily3_data_20210101_Current = pd.read_excel(
    './DataGuide/DG_DAILY_20210101_Current.xlsx', sheet_name="DAILY3", header=None, skiprows=14, skipfooter=0)
dg_daily3_data_20210101_Current.to_pickle('./DataGuide_processed/dg_daily3_data_20210101_Current.pkl')

dg_daily4_data_20210101_Current = pd.read_excel(
    './DataGuide/DG_DAILY_20210101_Current.xlsx', sheet_name="DAILY4", header=None, skiprows=14, skipfooter=0)
dg_daily4_data_20210101_Current.to_pickle('./DataGuide_processed/dg_daily4_data_20210101_Current.pkl')

dg_daily5_data_20210101_Current = pd.read_excel(
    './DataGuide/DG_DAILY_20210101_Current.xlsx', sheet_name="DAILY5", header=None, skiprows=14, skipfooter=0)
dg_daily5_data_20210101_Current.to_pickle('./DataGuide_processed/dg_daily5_data_20210101_Current.pkl')


dg_daily1_header_20210101_Current = pd.read_excel(
    './DataGuide/DG_DAILY_20210101_Current.xlsx', sheet_name="DAILY1", header=None, skiprows=8, nrows=6)
dg_daily1_header_20210101_Current.to_pickle('./DataGuide_processed/dg_daily1_header_20210101_Current.pkl')

dg_daily2_header_20210101_Current = pd.read_excel(
    './DataGuide/DG_DAILY_20210101_Current.xlsx', sheet_name="DAILY2", header=None, skiprows=8, nrows=6)
dg_daily2_header_20210101_Current.to_pickle('./DataGuide_processed/dg_daily2_header_20210101_Current.pkl')

dg_daily3_header_20210101_Current = pd.read_excel(
    './DataGuide/DG_DAILY_20210101_Current.xlsx', sheet_name="DAILY3", header=None, skiprows=8, nrows=6)
dg_daily3_header_20210101_Current.to_pickle('./DataGuide_processed/dg_daily3_header_20210101_Current.pkl')

dg_daily4_header_20210101_Current = pd.read_excel(
    './DataGuide/DG_DAILY_20210101_Current.xlsx', sheet_name="DAILY4", header=None, skiprows=8, nrows=6)
dg_daily4_header_20210101_Current.to_pickle('./DataGuide_processed/dg_daily4_header_20210101_Current.pkl')

dg_daily5_header_20210101_Current = pd.read_excel(
    './DataGuide/DG_DAILY_20210101_Current.xlsx', sheet_name="DAILY5", header=None, skiprows=8, nrows=6)
dg_daily5_header_20210101_Current.to_pickle('./DataGuide_processed/dg_daily5_header_20210101_Current.pkl')



dg_daily7_data_20210101_Current = pd.read_excel(
    './DataGuide/DG_DAILY7_20210101_Current.xlsx', sheet_name="DAILY7", header=None, skiprows=14, skipfooter=0)
dg_daily7_data_20210101_Current.to_pickle('./DataGuide_processed/dg_daily7_data_20210101_Current.pkl')

dg_daily7_header_20210101_Current = pd.read_excel(
    './DataGuide/DG_DAILY7_20210101_Current.xlsx', sheet_name="DAILY7", header=None, skiprows=8, nrows=6)
dg_daily7_header_20210101_Current.to_pickle('./DataGuide_processed/dg_daily7_header_20210101_Current.pkl')



# StopWatch
time_end_headers = datetime.now()
print("Load Headers finished at: " + str(time_end_headers))
print("Elapsed (in total): " + str(time_end_headers - time_start))



