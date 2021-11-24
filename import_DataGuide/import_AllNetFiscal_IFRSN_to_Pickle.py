# Created by Kim Hyeongjun on 03/22/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.

import pandas as pd
import numpy as np

########################################################################################################################
# Import Pickle Dataset
dg_fs_IFRSN_2000_2009_data = pd.read_pickle('./DataGuide_processed/dg_fs_IFRSN_2000_2009_data.pkl')
dg_fs_IFRSN_2010_2019_data = pd.read_pickle('./DataGuide_processed/dg_fs_IFRSN_2010_2019_data.pkl')
dg_fs_IFRSN_2020_2021_data = pd.read_pickle('./DataGuide_processed/dg_fs_IFRSN_2020_2021_data.pkl')

dg_fs_IFRSN_2000_2009_header = pd.read_pickle('./DataGuide_processed/dg_fs_IFRSN_2000_2009_header.pkl')
dg_fs_IFRSN_2010_2019_header = pd.read_pickle('./DataGuide_processed/dg_fs_IFRSN_2010_2019_header.pkl')
dg_fs_IFRSN_2020_2021_header = pd.read_pickle('./DataGuide_processed/dg_fs_IFRSN_2020_2021_header.pkl')

########################################################################################################################
# 데이터 합치기
fs_IFRSN = pd.concat([
    dg_fs_IFRSN_2000_2009_data, dg_fs_IFRSN_2010_2019_data, dg_fs_IFRSN_2020_2021_data])

# Column Index 설정하기
column_index1 = dg_fs_IFRSN_2020_2021_header.iloc[3, 0:5].tolist()
column_index2 = dg_fs_IFRSN_2020_2021_header.iloc[2, 5:].tolist()
column_index = column_index1 + column_index2
fs_IFRSN.columns = column_index  # Column Index 설정

# 데이터 정렬하기
fs_IFRSN = fs_IFRSN.sort_values(by=["Symbol", "회계년", "주기"])

########################################################################################################################
# Import Pickle Dataset
dg_GeneralHistoric_Quarterly = pd.read_pickle('./DataGuide_processed/dg_GeneralHistoric_Quarterly.pkl')

# 기업x회계년 마다 GeneralHistoric_Quarterly 연결
fs_IFRSN = pd.merge(
    fs_IFRSN, dg_GeneralHistoric_Quarterly[["Symbol", "회계년", "주기", "결산월(Hist)", "거래소(시장)"]],
    left_on=["Symbol", "회계년", "주기"], right_on=["Symbol", "회계년", "주기"], how='left')


########################################################################################################################
# 결산월(Hist) 과 주기(1Q, 2Q, 3Q, 4Q)에 따라서 보고서 제출연도 및 제출월 작성
# 사업보고서: 결산 후 90일 이내 (12월 결산법인 03/31)
# 분기보고서: 분기 경과 후 45일 이내 (12월 결산법인 05/17)
# 반기보고서: 반기 경과 후 45일 이내 (12월 결산법인 08/16)
# 분기보고서: 분기 경과 후 45일 이내 (12월 결산법인 11/15)
# 이베스트투자증권 결산월이 3월에서 12월로 변경
# 유유제약 결산월 3월에서 9월로 변경 2017년

fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 1) & (fs_IFRSN["주기"] == "1Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 1) & (fs_IFRSN["주기"] == "1Q"), "제출월"] = 6
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 1) & (fs_IFRSN["주기"] == "2Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 1) & (fs_IFRSN["주기"] == "2Q"), "제출월"] = 9
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 1) & (fs_IFRSN["주기"] == "3Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 1) & (fs_IFRSN["주기"] == "3Q"), "제출월"] = 12
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 1) & (fs_IFRSN["주기"] == "4Q"), "제출년"] = fs_IFRSN["회계년"] + 1
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 1) & (fs_IFRSN["주기"] == "4Q"), "제출월"] = 4

fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 2) & (fs_IFRSN["주기"] == "1Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 2) & (fs_IFRSN["주기"] == "1Q"), "제출월"] = 7
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 2) & (fs_IFRSN["주기"] == "2Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 2) & (fs_IFRSN["주기"] == "2Q"), "제출월"] = 10
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 2) & (fs_IFRSN["주기"] == "3Q"), "제출년"] = fs_IFRSN["회계년"] + 1
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 2) & (fs_IFRSN["주기"] == "3Q"), "제출월"] = 1
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 2) & (fs_IFRSN["주기"] == "4Q"), "제출년"] = fs_IFRSN["회계년"] + 1
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 2) & (fs_IFRSN["주기"] == "4Q"), "제출월"] = 5

fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 3) & (fs_IFRSN["주기"] == "1Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 3) & (fs_IFRSN["주기"] == "1Q"), "제출월"] = 8
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 3) & (fs_IFRSN["주기"] == "2Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 3) & (fs_IFRSN["주기"] == "2Q"), "제출월"] = 11
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 3) & (fs_IFRSN["주기"] == "3Q"), "제출년"] = fs_IFRSN["회계년"] + 1
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 3) & (fs_IFRSN["주기"] == "3Q"), "제출월"] = 2
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 3) & (fs_IFRSN["주기"] == "4Q"), "제출년"] = fs_IFRSN["회계년"] + 1
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 3) & (fs_IFRSN["주기"] == "4Q"), "제출월"] = 6


fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 4) & (fs_IFRSN["주기"] == "1Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 4) & (fs_IFRSN["주기"] == "1Q"), "제출월"] = 9
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 4) & (fs_IFRSN["주기"] == "2Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 4) & (fs_IFRSN["주기"] == "2Q"), "제출월"] = 12
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 4) & (fs_IFRSN["주기"] == "3Q"), "제출년"] = fs_IFRSN["회계년"] + 1
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 4) & (fs_IFRSN["주기"] == "3Q"), "제출월"] = 3
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 4) & (fs_IFRSN["주기"] == "4Q"), "제출년"] = fs_IFRSN["회계년"] + 1
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 4) & (fs_IFRSN["주기"] == "4Q"), "제출월"] = 7

fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 5) & (fs_IFRSN["주기"] == "1Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 5) & (fs_IFRSN["주기"] == "1Q"), "제출월"] = 10
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 5) & (fs_IFRSN["주기"] == "2Q"), "제출년"] = fs_IFRSN["회계년"] + 1
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 5) & (fs_IFRSN["주기"] == "2Q"), "제출월"] = 1
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 5) & (fs_IFRSN["주기"] == "3Q"), "제출년"] = fs_IFRSN["회계년"] + 1
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 5) & (fs_IFRSN["주기"] == "3Q"), "제출월"] = 4
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 5) & (fs_IFRSN["주기"] == "4Q"), "제출년"] = fs_IFRSN["회계년"] + 1
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 5) & (fs_IFRSN["주기"] == "4Q"), "제출월"] = 8

fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 6) & (fs_IFRSN["주기"] == "1Q"), "제출년"] = fs_IFRSN["회계년"] - 1
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 6) & (fs_IFRSN["주기"] == "1Q"), "제출월"] = 11
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 6) & (fs_IFRSN["주기"] == "2Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 6) & (fs_IFRSN["주기"] == "2Q"), "제출월"] = 2
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 6) & (fs_IFRSN["주기"] == "3Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 6) & (fs_IFRSN["주기"] == "3Q"), "제출월"] = 5
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 6) & (fs_IFRSN["주기"] == "4Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 6) & (fs_IFRSN["주기"] == "4Q"), "제출월"] = 9


fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 7) & (fs_IFRSN["주기"] == "1Q"), "제출년"] = fs_IFRSN["회계년"] - 1
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 7) & (fs_IFRSN["주기"] == "1Q"), "제출월"] = 12
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 7) & (fs_IFRSN["주기"] == "2Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 7) & (fs_IFRSN["주기"] == "2Q"), "제출월"] = 3
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 7) & (fs_IFRSN["주기"] == "3Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 7) & (fs_IFRSN["주기"] == "3Q"), "제출월"] = 6
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 7) & (fs_IFRSN["주기"] == "4Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 7) & (fs_IFRSN["주기"] == "4Q"), "제출월"] = 10

fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 8) & (fs_IFRSN["주기"] == "1Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 8) & (fs_IFRSN["주기"] == "1Q"), "제출월"] = 1
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 8) & (fs_IFRSN["주기"] == "2Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 8) & (fs_IFRSN["주기"] == "2Q"), "제출월"] = 4
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 8) & (fs_IFRSN["주기"] == "3Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 8) & (fs_IFRSN["주기"] == "3Q"), "제출월"] = 7
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 8) & (fs_IFRSN["주기"] == "4Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 8) & (fs_IFRSN["주기"] == "4Q"), "제출월"] = 11

fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 9) & (fs_IFRSN["주기"] == "1Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 9) & (fs_IFRSN["주기"] == "1Q"), "제출월"] = 2
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 9) & (fs_IFRSN["주기"] == "2Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 9) & (fs_IFRSN["주기"] == "2Q"), "제출월"] = 5
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 9) & (fs_IFRSN["주기"] == "3Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 9) & (fs_IFRSN["주기"] == "3Q"), "제출월"] = 8
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 9) & (fs_IFRSN["주기"] == "4Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 9) & (fs_IFRSN["주기"] == "4Q"), "제출월"] = 12


fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 10) & (fs_IFRSN["주기"] == "1Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 10) & (fs_IFRSN["주기"] == "1Q"), "제출월"] = 3
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 10) & (fs_IFRSN["주기"] == "2Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 10) & (fs_IFRSN["주기"] == "2Q"), "제출월"] = 6
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 10) & (fs_IFRSN["주기"] == "3Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 10) & (fs_IFRSN["주기"] == "3Q"), "제출월"] = 9
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 10) & (fs_IFRSN["주기"] == "4Q"), "제출년"] = fs_IFRSN["회계년"] + 1
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 10) & (fs_IFRSN["주기"] == "4Q"), "제출월"] = 1

fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 11) & (fs_IFRSN["주기"] == "1Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 11) & (fs_IFRSN["주기"] == "1Q"), "제출월"] = 4
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 11) & (fs_IFRSN["주기"] == "2Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 11) & (fs_IFRSN["주기"] == "2Q"), "제출월"] = 7
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 11) & (fs_IFRSN["주기"] == "3Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 11) & (fs_IFRSN["주기"] == "3Q"), "제출월"] = 10
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 11) & (fs_IFRSN["주기"] == "4Q"), "제출년"] = fs_IFRSN["회계년"] + 1
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 11) & (fs_IFRSN["주기"] == "4Q"), "제출월"] = 2

fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 12) & (fs_IFRSN["주기"] == "1Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 12) & (fs_IFRSN["주기"] == "1Q"), "제출월"] = 5
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 12) & (fs_IFRSN["주기"] == "2Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 12) & (fs_IFRSN["주기"] == "2Q"), "제출월"] = 8
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 12) & (fs_IFRSN["주기"] == "3Q"), "제출년"] = fs_IFRSN["회계년"]
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 12) & (fs_IFRSN["주기"] == "3Q"), "제출월"] = 11
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 12) & (fs_IFRSN["주기"] == "4Q"), "제출년"] = fs_IFRSN["회계년"] + 1
fs_IFRSN.loc[(fs_IFRSN["결산월(Hist)"] == 12) & (fs_IFRSN["주기"] == "4Q"), "제출월"] = 3

# 예외처리
fs_IFRSN.loc[(fs_IFRSN["Name"] == "KBI메탈") & (fs_IFRSN["회계년"] == 2004) & (fs_IFRSN["결산월"] == 10), "제출월"] = 12  # 4월 결산법인
fs_IFRSN.loc[(fs_IFRSN["Name"] == "잉크테크") & (fs_IFRSN["회계년"] == 2004) & (fs_IFRSN["결산월"] == 11), "제출년"] = 2005  # 5월 결산법인
fs_IFRSN.loc[(fs_IFRSN["Name"] == "잉크테크") & (fs_IFRSN["회계년"] == 2004) & (fs_IFRSN["결산월"] == 11), "제출월"] = 1  # 5월 결산법인
fs_IFRSN.loc[(fs_IFRSN["Name"] == "대한방직") & (fs_IFRSN["회계년"] == 2000) & (fs_IFRSN["결산월"] == 1), "제출월"] = 3  # 7월 결산법인


########################################################################################################################
# # 결산월 및 회계연도에 따른 재무제표 제출연월 계산
# tmp = fs_IFRSN[["Symbol", "Name", "결산월", "회계년", "주기", "총자산(천원)"]].copy()
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
# 각 주기(1Q, 2Q, 3Q, 4Q) 별로 결산월이 (3, 6, 9, 12) 가 아니라 (12, 12, 12, 12) 로 입력된 자료들이 있다.
# 이런 자료들은 분기 데이터가 없고 annual 자료만 있을 가능성 높다. 따라서 골라내야 한다.

# 인덱스 자료(Symbol, Name, 결산월, 회계년, 주기)만 따로 저장
df_index0 = fs_IFRSN.iloc[:, 0:6]

# 주기(1Q, 2Q, 3Q, 4Q)에 따라 결산월을 각 기업x회계년마다 한줄로 변환
df_index1 = df_index0.pivot(index=["Symbol", "회계년"], columns="주기", values="결산월")
df_index1.index = df_index1.index.set_names(['Symbol', '회계년'])
df_index1.reset_index(inplace=True)

# 주기(1Q, 2Q, 3Q, 4Q)에 따라 총자산(천원) 을 각 기업x회계년마다 한줄로 변환
df_index2 = df_index0.pivot(index=["Symbol", "회계년"], columns="주기", values="총자산(천원)")
df_index2.index = df_index2.index.set_names(['Symbol', '회계년'])
df_index2.reset_index(inplace=True)
df_index2.rename(columns={"1Q":"AT_1Q", "2Q":"AT_2Q", "3Q":"AT_3Q", "4Q":"AT_4Q"}, inplace=True)

df_index3 = pd.merge(
    df_index1, df_index2,
    left_on=["Symbol", "회계년"], right_on=["Symbol", "회계년"], how='left')

# 1,2,3분기의 총자산이 nan이고 4분기 총자산이 입력되어 있는 경우를 표시
cond_nan_123Q = np.isnan(df_index3["AT_1Q"]) & np.isnan(df_index3["AT_2Q"]) & np.isnan(df_index3["AT_3Q"]) & (~np.isnan(df_index3["AT_4Q"]))
df_index3['check_nan_123Q'] = np.where(cond_nan_123Q, True, False)

# 기업x회계년 마다 더미변수를 연결
fs_IFRSN = pd.merge(
    fs_IFRSN, df_index3[["Symbol", "회계년", "check_nan_123Q"]],
    left_on=["Symbol", "회계년"], right_on=["Symbol", "회계년"], how='left')

########################################################################################################################
# 기업코드x회계연도 별로 결산월 값이 하나인(unique) 기업코드x회계연도 체크
check_unique_settle_month = fs_IFRSN.groupby(["Symbol", "회계년"])["결산월"].nunique().eq(1)
fs_IFRSN = pd.merge(fs_IFRSN, check_unique_settle_month, left_on=["Symbol", "회계년"], right_index=True, how='left')
fs_IFRSN.rename(columns={"결산월_x":"결산월", "결산월_y":"check_unique_settle_month"}, inplace=True)

# 기업코드 별로 결산월(Hist) 값이 모두 비어있는 기업코드 체크
check_null_settle_month_hist = fs_IFRSN.groupby("Symbol")['결산월(Hist)'].apply(lambda x: x.isnull().all())
fs_IFRSN = pd.merge(fs_IFRSN, check_null_settle_month_hist, left_on=["Symbol"], right_index=True, how='left')
fs_IFRSN.rename(columns={"결산월(Hist)_x":"결산월(Hist)", "결산월(Hist)_y":"check_null_settle_month_hist"}, inplace=True)

# 기업코드 별로 결산월(Hist) 값이 하나인(unique) 기업코드 체크
check_unique_settle_month_hist = fs_IFRSN.groupby(["Symbol"])["결산월(Hist)"].nunique().eq(1)
fs_IFRSN = pd.merge(fs_IFRSN, check_unique_settle_month_hist, left_on=["Symbol"], right_index=True, how='left')
fs_IFRSN.rename(columns={"결산월(Hist)_x":"결산월(Hist)", "결산월(Hist)_y":"check_unique_settle_month_hist"}, inplace=True)

########################################################################################################################
# 제출날짜 구하기
fs_IFRSN["제출월2"] = fs_IFRSN["제출월"] + 1
fs_IFRSN["제출년2"] = fs_IFRSN["제출년"]
fs_IFRSN.loc[fs_IFRSN["제출월2"] > 12, "제출년2"] = fs_IFRSN["제출년"] + 1
fs_IFRSN.loc[fs_IFRSN["제출월2"] > 12, "제출월2"] = fs_IFRSN["제출월2"] - 12
fs_IFRSN["제출날짜"] = fs_IFRSN["제출년2"]*10000 + fs_IFRSN["제출월2"]*100 + 1
fs_IFRSN["제출날짜"] = pd.to_datetime(fs_IFRSN["제출날짜"].astype(str), errors='coerce', format='%Y%m%d')
fs_IFRSN["제출날짜"] = fs_IFRSN["제출날짜"] - pd.Timedelta(days=1)
fs_IFRSN["사용가능날짜"] = fs_IFRSN["제출날짜"] + pd.Timedelta(days=1)
fs_IFRSN.pop("제출월2")
fs_IFRSN.pop("제출년2")

########################################################################################################################
# 컬럼 순서 바꾸기
column_names = fs_IFRSN.columns.tolist()
new_column_names1 = column_names[0:5]
new_column_names2 = column_names[-10:]
new_column_names3 = column_names[5:-10]

new_column_names0 = ['Symbol', 'Name', '거래소(시장)', '결산월(Hist)', '회계년', '결산월', '주기', '제출년', '제출월',
                     '제출날짜', "사용가능날짜", 'check_unique_settle_month_hist', 'check_null_settle_month_hist',
                     'check_unique_settle_month', 'check_nan_123Q']

new_column_names = new_column_names0 + new_column_names3
fs_IFRSN = fs_IFRSN[new_column_names]

########################################################################################################################
# 데이터 저장하기
fs_IFRSN.to_pickle('./DataGuide_processed/fs_IFRSN.pkl')

# 재무제표 자료는 2011년 이후부터 분기별 자료 사용 가능
fs_IFRSN = pd.read_pickle('./DataGuide_processed/fs_IFRSN.pkl')
fs_IFRSN_sample = fs_IFRSN.loc[fs_IFRSN["회계년"] > 2015]

fs_IFRSN_sample.to_pickle('./DataGuide_processed/fs_IFRSN_sample.pkl')


