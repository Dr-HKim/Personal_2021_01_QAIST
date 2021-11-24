# Created by Kim Hyeongjun on 03/22/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.
# 데이터가이드 일간 데이터 엑셀을 불러와서 Pickle 형태로 저장
# 전체 약 5시간 소요

import pandas as pd
from datetime import datetime


########################################################################################################################
# Import Pickle Dataset
dg_GeneralHistoric_Annual_2000_2021_data = \
    pd.read_pickle('./DataGuide_processed/dg_GeneralHistoric_Annual_2000_2021_data.pkl')
dg_GeneralHistoric_Annual_2000_2021_header = \
    pd.read_pickle('./DataGuide_processed/dg_GeneralHistoric_Annual_2000_2021_header.pkl')

dg_GeneralHistoric_Annual = dg_GeneralHistoric_Annual_2000_2021_data.copy()

# Column Index 설정하기
column_index1 = dg_GeneralHistoric_Annual_2000_2021_header.iloc[3, 0:5].tolist()
column_index2 = dg_GeneralHistoric_Annual_2000_2021_header.iloc[2, 5:].tolist()
column_index = column_index1 + column_index2
dg_GeneralHistoric_Annual.columns = column_index  # Column Index 설정

# 데이터 정렬하기
dg_GeneralHistoric_Annual = dg_GeneralHistoric_Annual.sort_values(by=["Symbol", "회계년", "주기"])

# 데이터 저장하기
dg_GeneralHistoric_Annual.to_pickle('./DataGuide_processed/dg_GeneralHistoric_Annual.pkl')


########################################################################################################################
# Import Pickle Dataset
dg_GeneralHistoric_2020_2021_data = \
    pd.read_pickle('./DataGuide_processed/dg_GeneralHistoric_2020_2021_data.pkl')
dg_GeneralHistoric_2013_2019_data = \
    pd.read_pickle('./DataGuide_processed/dg_GeneralHistoric_2013_2019_data.pkl')
dg_GeneralHistoric_2009_2012_data = \
    pd.read_pickle('./DataGuide_processed/dg_GeneralHistoric_2009_2012_data.pkl')
dg_GeneralHistoric_2005_2008_data = \
    pd.read_pickle('./DataGuide_processed/dg_GeneralHistoric_2005_2008_data.pkl')
dg_GeneralHistoric_2001_2004_data = \
    pd.read_pickle('./DataGuide_processed/dg_GeneralHistoric_2001_2004_data.pkl')
dg_GeneralHistoric_1997_2000_data = \
    pd.read_pickle('./DataGuide_processed/dg_GeneralHistoric_1997_2000_data.pkl')
dg_GeneralHistoric_2020_2021_header = \
    pd.read_pickle('./DataGuide_processed/dg_GeneralHistoric_2020_2021_header.pkl')

# 데이터 합치기
dg_GeneralHistoric_Quarterly = pd.concat([
    dg_GeneralHistoric_2020_2021_data, dg_GeneralHistoric_2013_2019_data, dg_GeneralHistoric_2009_2012_data,
    dg_GeneralHistoric_2005_2008_data, dg_GeneralHistoric_2001_2004_data, dg_GeneralHistoric_1997_2000_data])

# Column Index 설정하기
column_index1 = dg_GeneralHistoric_2020_2021_header.iloc[3, 0:5].tolist()
column_index2 = dg_GeneralHistoric_2020_2021_header.iloc[2, 5:].tolist()
column_index = column_index1 + column_index2
dg_GeneralHistoric_Quarterly.columns = column_index  # Column Index 설정

# 데이터 정렬하기
dg_GeneralHistoric_Quarterly = dg_GeneralHistoric_Quarterly.sort_values(by=["Symbol", "회계년", "주기"])

# 데이터 저장하기
dg_GeneralHistoric_Quarterly.to_pickle('./DataGuide_processed/dg_GeneralHistoric_Quarterly.pkl')
