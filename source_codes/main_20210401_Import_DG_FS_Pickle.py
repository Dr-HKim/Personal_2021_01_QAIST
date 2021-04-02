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
# 결산월 및 회계연도에 따른 재무제표 제출연월 계산
tmp = fs_IFRSC[["Symbol", "Name", "결산월", "회계년", "주기", "총자산(천원)"]].copy()
tmp["제출년"] = tmp["회계년"].copy()

# 분기 및 반기보고서는 45일, 사업보고서는 90일 제출기한
tmp.loc[tmp["주기"] == "1Q", "제출월"] = tmp.loc[tmp["주기"] == "1Q", "결산월"].copy() + 2
tmp.loc[tmp["주기"] == "2Q", "제출월"] = tmp.loc[tmp["주기"] == "2Q", "결산월"].copy() + 2
tmp.loc[tmp["주기"] == "3Q", "제출월"] = tmp.loc[tmp["주기"] == "3Q", "결산월"].copy() + 2
tmp.loc[tmp["주기"] == "4Q", "제출월"] = tmp.loc[tmp["주기"] == "4Q", "결산월"].copy() + 3

tmp.loc[tmp["제출월"] > 12, "제출년"] = tmp.loc[tmp["제출월"] > 12, "제출년"].copy() + 1
tmp.loc[tmp["제출월"] > 12, "제출월"] = tmp.loc[tmp["제출월"] > 12, "제출월"].copy() - 12

########################################################################################################################
# 결산월이 3, 6, 9, 12 가 아니라 12, 12, 12, 12 라는 식으로 입력된 것들이 있다.
tmp_group = tmp.groupby(by=["Symbol", "회계년"], as_index=False).agg({"결산월": [min, max]})
tmp_group.columns = ["_".join(x) for x in tmp_group.columns.ravel()]  # 인덱스 구조를 단순화
tmp_group.rename(columns={'Symbol_': 'Symbol', '회계년_': '회계년'}, inplace=True)  # 필요시 이름 변경
tmp_group2 = tmp_group[tmp_group["결산월_min"] == tmp_group["결산월_max"]]




########################################################################################################################
# 데이터 저장하기
fs_IFRSC.to_pickle('./data_processed/fs_IFRSC.pkl')
