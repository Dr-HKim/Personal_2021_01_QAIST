# Created by Kim Hyeongjun on 03/22/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.

import pandas as pd

########################################################################################################################
# Import Pickle Dataset
dg_fs_IFRSC_2000_2009_data = pd.read_pickle('./data_processed/dg_fs_IFRSC_2000_2009_data.pkl')
dg_fs_IFRSC_2010_2019_data = pd.read_pickle('./data_processed/dg_fs_IFRSC_2010_2019_data.pkl')
dg_fs_IFRSC_2020_2021_data = pd.read_pickle('./data_processed/dg_fs_IFRSC_2020_2021_data.pkl')

dg_fs_IFRSC_2000_2009_header = pd.read_pickle('./data_processed/dg_fs_IFRSC_2000_2009_header.pkl')
dg_fs_IFRSC_2010_2019_header = pd.read_pickle('./data_processed/dg_fs_IFRSC_2010_2019_header.pkl')
dg_fs_IFRSC_2020_2021_header = pd.read_pickle('./data_processed/dg_fs_IFRSC_2020_2021_header.pkl')

########################################################################################################################
# 데이터 합치기
fs_IFRSC = pd.concat([
    dg_fs_IFRSC_2000_2009_data, dg_fs_IFRSC_2010_2019_data, dg_fs_IFRSC_2020_2021_data])

# Column Index 설정하기
column_index1 = dg_fs_IFRSC_2020_2021_header.iloc[3, 0:5].tolist()
column_index2 = dg_fs_IFRSC_2020_2021_header.iloc[2, 5:].tolist()
column_index = column_index1 + column_index2
fs_IFRSC.columns = column_index  # Column Index 설정

# 데이터 정렬하기
fs_IFRSC = fs_IFRSC.sort_values(by=["Symbol", "회계년", "주기"])


########################################################################################################################
# 결산월(Hist) 과 주기(1Q, 2Q, 3Q, 4Q)에 따라서 보고서 제출연도 및 제출월 작성
# 사업보고서: 결산 후 90일 이내 (12월 결산법인 03/31)
# 분기보고서: 분기 경과 후 45일 이내 (12월 결산법인 05/17)
# 반기보고서: 반기 경과 후 45일 이내 (12월 결산법인 08/16)
# 분기보고서: 분기 경과 후 45일 이내 (12월 결산법인 11/15)

fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 1) & (fs_IFRSC["주기"] == "1Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 1) & (fs_IFRSC["주기"] == "1Q"), "제출월"] = 6
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 1) & (fs_IFRSC["주기"] == "2Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 1) & (fs_IFRSC["주기"] == "2Q"), "제출월"] = 9
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 1) & (fs_IFRSC["주기"] == "3Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 1) & (fs_IFRSC["주기"] == "3Q"), "제출월"] = 12
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 1) & (fs_IFRSC["주기"] == "4Q"), "제출년"] = fs_IFRSC["회계년"] + 1
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 1) & (fs_IFRSC["주기"] == "4Q"), "제출월"] = 4

fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 2) & (fs_IFRSC["주기"] == "1Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 2) & (fs_IFRSC["주기"] == "1Q"), "제출월"] = 7
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 2) & (fs_IFRSC["주기"] == "2Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 2) & (fs_IFRSC["주기"] == "2Q"), "제출월"] = 10
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 2) & (fs_IFRSC["주기"] == "3Q"), "제출년"] = fs_IFRSC["회계년"] + 1
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 2) & (fs_IFRSC["주기"] == "3Q"), "제출월"] = 1
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 2) & (fs_IFRSC["주기"] == "4Q"), "제출년"] = fs_IFRSC["회계년"] + 1
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 2) & (fs_IFRSC["주기"] == "4Q"), "제출월"] = 5

fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 3) & (fs_IFRSC["주기"] == "1Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 3) & (fs_IFRSC["주기"] == "1Q"), "제출월"] = 8
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 3) & (fs_IFRSC["주기"] == "2Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 3) & (fs_IFRSC["주기"] == "2Q"), "제출월"] = 11
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 3) & (fs_IFRSC["주기"] == "3Q"), "제출년"] = fs_IFRSC["회계년"] + 1
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 3) & (fs_IFRSC["주기"] == "3Q"), "제출월"] = 2
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 3) & (fs_IFRSC["주기"] == "4Q"), "제출년"] = fs_IFRSC["회계년"] + 1
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 3) & (fs_IFRSC["주기"] == "4Q"), "제출월"] = 6


fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 4) & (fs_IFRSC["주기"] == "1Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 4) & (fs_IFRSC["주기"] == "1Q"), "제출월"] = 9
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 4) & (fs_IFRSC["주기"] == "2Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 4) & (fs_IFRSC["주기"] == "2Q"), "제출월"] = 12
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 4) & (fs_IFRSC["주기"] == "3Q"), "제출년"] = fs_IFRSC["회계년"] + 1
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 4) & (fs_IFRSC["주기"] == "3Q"), "제출월"] = 3
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 4) & (fs_IFRSC["주기"] == "4Q"), "제출년"] = fs_IFRSC["회계년"] + 1
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 4) & (fs_IFRSC["주기"] == "4Q"), "제출월"] = 7

fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 5) & (fs_IFRSC["주기"] == "1Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 5) & (fs_IFRSC["주기"] == "1Q"), "제출월"] = 10
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 5) & (fs_IFRSC["주기"] == "2Q"), "제출년"] = fs_IFRSC["회계년"] + 1
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 5) & (fs_IFRSC["주기"] == "2Q"), "제출월"] = 1
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 5) & (fs_IFRSC["주기"] == "3Q"), "제출년"] = fs_IFRSC["회계년"] + 1
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 5) & (fs_IFRSC["주기"] == "3Q"), "제출월"] = 4
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 5) & (fs_IFRSC["주기"] == "4Q"), "제출년"] = fs_IFRSC["회계년"] + 1
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 5) & (fs_IFRSC["주기"] == "4Q"), "제출월"] = 8

fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 6) & (fs_IFRSC["주기"] == "1Q"), "제출년"] = fs_IFRSC["회계년"] - 1
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 6) & (fs_IFRSC["주기"] == "1Q"), "제출월"] = 11
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 6) & (fs_IFRSC["주기"] == "2Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 6) & (fs_IFRSC["주기"] == "2Q"), "제출월"] = 2
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 6) & (fs_IFRSC["주기"] == "3Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 6) & (fs_IFRSC["주기"] == "3Q"), "제출월"] = 5
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 6) & (fs_IFRSC["주기"] == "4Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 6) & (fs_IFRSC["주기"] == "4Q"), "제출월"] = 9


fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 7) & (fs_IFRSC["주기"] == "1Q"), "제출년"] = fs_IFRSC["회계년"] - 1
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 7) & (fs_IFRSC["주기"] == "1Q"), "제출월"] = 12
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 7) & (fs_IFRSC["주기"] == "2Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 7) & (fs_IFRSC["주기"] == "2Q"), "제출월"] = 3
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 7) & (fs_IFRSC["주기"] == "3Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 7) & (fs_IFRSC["주기"] == "3Q"), "제출월"] = 6
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 7) & (fs_IFRSC["주기"] == "4Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 7) & (fs_IFRSC["주기"] == "4Q"), "제출월"] = 10

fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 8) & (fs_IFRSC["주기"] == "1Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 8) & (fs_IFRSC["주기"] == "1Q"), "제출월"] = 1
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 8) & (fs_IFRSC["주기"] == "2Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 8) & (fs_IFRSC["주기"] == "2Q"), "제출월"] = 4
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 8) & (fs_IFRSC["주기"] == "3Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 8) & (fs_IFRSC["주기"] == "3Q"), "제출월"] = 7
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 8) & (fs_IFRSC["주기"] == "4Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 8) & (fs_IFRSC["주기"] == "4Q"), "제출월"] = 11

fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 9) & (fs_IFRSC["주기"] == "1Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 9) & (fs_IFRSC["주기"] == "1Q"), "제출월"] = 2
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 9) & (fs_IFRSC["주기"] == "2Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 9) & (fs_IFRSC["주기"] == "2Q"), "제출월"] = 5
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 9) & (fs_IFRSC["주기"] == "3Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 9) & (fs_IFRSC["주기"] == "3Q"), "제출월"] = 8
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 9) & (fs_IFRSC["주기"] == "4Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 9) & (fs_IFRSC["주기"] == "4Q"), "제출월"] = 12


fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 10) & (fs_IFRSC["주기"] == "1Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 10) & (fs_IFRSC["주기"] == "1Q"), "제출월"] = 3
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 10) & (fs_IFRSC["주기"] == "2Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 10) & (fs_IFRSC["주기"] == "2Q"), "제출월"] = 6
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 10) & (fs_IFRSC["주기"] == "3Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 10) & (fs_IFRSC["주기"] == "3Q"), "제출월"] = 9
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 10) & (fs_IFRSC["주기"] == "4Q"), "제출년"] = fs_IFRSC["회계년"] + 1
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 10) & (fs_IFRSC["주기"] == "4Q"), "제출월"] = 1

fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 11) & (fs_IFRSC["주기"] == "1Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 11) & (fs_IFRSC["주기"] == "1Q"), "제출월"] = 4
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 11) & (fs_IFRSC["주기"] == "2Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 11) & (fs_IFRSC["주기"] == "2Q"), "제출월"] = 7
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 11) & (fs_IFRSC["주기"] == "3Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 11) & (fs_IFRSC["주기"] == "3Q"), "제출월"] = 10
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 11) & (fs_IFRSC["주기"] == "4Q"), "제출년"] = fs_IFRSC["회계년"] + 1
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 11) & (fs_IFRSC["주기"] == "4Q"), "제출월"] = 2

fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 12) & (fs_IFRSC["주기"] == "1Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 12) & (fs_IFRSC["주기"] == "1Q"), "제출월"] = 5
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 12) & (fs_IFRSC["주기"] == "2Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 12) & (fs_IFRSC["주기"] == "2Q"), "제출월"] = 8
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 12) & (fs_IFRSC["주기"] == "3Q"), "제출년"] = fs_IFRSC["회계년"]
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 12) & (fs_IFRSC["주기"] == "3Q"), "제출월"] = 11
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 12) & (fs_IFRSC["주기"] == "4Q"), "제출년"] = fs_IFRSC["회계년"] + 1
fs_IFRSC.loc[(fs_IFRSC["결산월(Hist)"] == 12) & (fs_IFRSC["주기"] == "4Q"), "제출월"] = 3

# 예외처리
fs_IFRSC.loc[(fs_IFRSC["Name"] == "KBI메탈") & (fs_IFRSC["회계년"] == 2004) & (fs_IFRSC["결산월"] == 10), "제출월"] = 12  # 4월 결산법인
fs_IFRSC.loc[(fs_IFRSC["Name"] == "잉크테크") & (fs_IFRSC["회계년"] == 2004) & (fs_IFRSC["결산월"] == 11), "제출년"] = 2005  # 5월 결산법인
fs_IFRSC.loc[(fs_IFRSC["Name"] == "잉크테크") & (fs_IFRSC["회계년"] == 2004) & (fs_IFRSC["결산월"] == 11), "제출월"] = 1  # 5월 결산법인
fs_IFRSC.loc[(fs_IFRSC["Name"] == "대한방직") & (fs_IFRSC["회계년"] == 2000) & (fs_IFRSC["결산월"] == 1), "제출월"] = 3  # 7월 결산법인


########################################################################################################################
# # 결산월 및 회계연도에 따른 재무제표 제출연월 계산
# tmp = fs_IFRSC[["Symbol", "Name", "결산월", "회계년", "주기", "총자산(천원)"]].copy()
# tmp["제출년"] = tmp["회계년"].copy()
#
# # 분기 및 반기보고서는 45일, 사업보고서는 90일 제출기한
# tmp.loc[tmp["주기"] == "1Q", "제출월"] = tmp.loc[tmp["주기"] == "1Q", "결산월"].copy() + 2
# tmp.loc[tmp["주기"] == "2Q", "제출월"] = tmp.loc[tmp["주기"] == "2Q", "결산월"].copy() + 2
# tmp.loc[tmp["주기"] == "3Q", "제출월"] = tmp.loc[tmp["주기"] == "3Q", "결산월"].copy() + 2
# tmp.loc[tmp["주기"] == "4Q", "제출월"] = tmp.loc[tmp["주기"] == "4Q", "결산월"].copy() + 3
#
# tmp.loc[tmp["제출월"] > 12, "제출년"] = tmp.loc[tmp["제출월"] > 12, "제출년"].copy() + 1
# tmp.loc[tmp["제출월"] > 12, "제출월"] = tmp.loc[tmp["제출월"] > 12, "제출월"].copy() - 12

########################################################################################################################
# 데이터 저장하기
fs_IFRSC.to_pickle('./data_processed/fs_IFRSC.pkl')

# 재무제표 자료는 2011년 이후부터 분기별 자료 사용 가능
fs_IFRSC = pd.read_pickle('./data_processed/fs_IFRSC.pkl')
fs_IFRSC_sample = fs_IFRSC.loc[fs_IFRSC["회계년"] > 2015]

fs_IFRSC_sample.to_pickle('./data_processed/fs_IFRSC_sample.pkl')


