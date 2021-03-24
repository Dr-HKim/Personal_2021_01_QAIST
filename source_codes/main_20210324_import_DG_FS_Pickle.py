# Created by Kim Hyeongjun on 03/22/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.

import pandas as pd


########################################################################################################################
# Import Pickle Dataset
dg_fs_20200519_1981_1989_data = pd.read_pickle('./data_processed/dg_fs_20200519_1981_1989_data.pkl')
dg_fs_20200519_1990_1999_data = pd.read_pickle('./data_processed/dg_fs_20200519_1990_1999_data.pkl')
dg_fs_20200519_2000_2015_data = pd.read_pickle('./data_processed/dg_fs_20200519_2000_2015_data.pkl')
dg_fs_20200519_2016_2020_data = pd.read_pickle('./data_processed/dg_fs_20200519_2016_2020_data.pkl')

dg_fs_20200519_1981_1989_header = pd.read_pickle('./data_processed/dg_fs_20200519_1981_1989_header.pkl')
dg_fs_20200519_1990_1999_header = pd.read_pickle('./data_processed/dg_fs_20200519_1990_1999_header.pkl')
dg_fs_20200519_2000_2015_header = pd.read_pickle('./data_processed/dg_fs_20200519_2000_2015_header.pkl')
dg_fs_20200519_2016_2020_header = pd.read_pickle('./data_processed/dg_fs_20200519_2016_2020_header.pkl')

########################################################################################################################
# 데이터 합치기
processed_fs_1981_2020 = pd.concat([
    dg_fs_20200519_1981_1989_data, dg_fs_20200519_1990_1999_data,
    dg_fs_20200519_2000_2015_data, dg_fs_20200519_2016_2020_data])

# Column Index 설정하기
column_index1 = dg_fs_20200519_2016_2020_header.iloc[3, 0:5].tolist()
column_index2 = dg_fs_20200519_2016_2020_header.iloc[2, 5:].tolist()
column_index = column_index1 + column_index2
processed_fs_1981_2020.columns = column_index  # Column Index 설정

# 데이터 정렬하기
processed_fs_1981_2020 = processed_fs_1981_2020.sort_values(by=["Symbol", "회계년", "주기"])

# 데이터 저장하기
processed_fs_1981_2020.to_pickle('./data_processed/processed_fs_1981_2020.pkl')
