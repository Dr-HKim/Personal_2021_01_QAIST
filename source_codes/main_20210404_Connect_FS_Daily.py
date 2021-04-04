# Created by Kim Hyeongjun on 03/22/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.

import pandas as pd
import numpy as np


########################################################################################################################
# Import Pickle Dataset
fs_IFRSC = pd.read_pickle('./data_processed/fs_IFRSC.pkl')
fs_IFRSN = pd.read_pickle('./data_processed/fs_IFRSN.pkl')
fs_GAAPC = pd.read_pickle('./data_processed/fs_GAAPC.pkl')
fs_GAAPN = pd.read_pickle('./data_processed/fs_GAAPN.pkl')

tmp_fs_IFRSN = fs_IFRSN.loc[fs_IFRSN["Name"] == "현대차"]
tmp_fs_IFRSC = fs_IFRSC.loc[fs_IFRSC["Name"] == "현대차"]
tmp_fs_GAAPC = fs_GAAPC.loc[fs_GAAPC["Name"] == "현대차"]
tmp_fs_GAAPN = fs_GAAPN.loc[fs_GAAPN["Name"] == "현대차"]

processed_daily_20000101_Current = pd.read_pickle('./data_processed/processed_daily_20000101_Current.pkl')

processed_daily_sample = pd.read_pickle('./data_processed/processed_daily_sample.pkl')
fs_IFRSC_sample = pd.read_pickle('./data_processed/fs_IFRSC_sample.pkl')

########################################################################################################################
# 만약 사용가능날짜가 2021-04-01 인데, 아직 DataGuide 업데이트가 안된 거라면 그 전 정보를 사용
# 아직 업데이트 안된 기업들 추려내기
date_current = pd.to_datetime("20210401", errors='coerce', format='%Y%m%d')
df_not_updated = fs_IFRSN.loc[(fs_IFRSN["사용가능날짜"] == date_current) & np.isnan(fs_IFRSN["총자산(천원)"])]

########################################################################################################################
# 기업코드x월별 자료를 만들고 각 월마다 들어가야하는 최신 레포트 사용가능날짜를 연결
list_symbol = fs_IFRSC["Symbol"]
list_symbol = list_symbol.drop_duplicates()
list_symbol = list_symbol.tolist()

list_YYYYMMDD = []
for year in range(2000, 2022):
    for month in range(1, 13):
        YYYYMMDD = year * 10000 + month * 100 + 1
        list_YYYYMMDD.append(YYYYMMDD)

index_symbol_YYYYMMDD = pd.MultiIndex.from_product([list_symbol, list_YYYYMMDD], names=["Symbol", "YYYYMMDD"])
df_fs_monthly = pd.DataFrame(index=index_symbol_YYYYMMDD)
df_fs_monthly = df_fs_monthly.reset_index()
df_fs_monthly["FS_DATE"] = pd.to_datetime(df_fs_monthly["YYYYMMDD"], errors='coerce', format='%Y%m%d')

df_fs_monthly = pd.merge(
    df_fs_monthly, fs_IFRSC[["Symbol", "사용가능날짜"]],
    left_on=["Symbol", "FS_DATE"], right_on=["Symbol", "사용가능날짜"], how='left')

df_fs_monthly["사용가능날짜"] = df_fs_monthly.groupby("Symbol")["사용가능날짜"].transform(lambda x: x.fillna(method='ffill'))

# 아직 업데이트가 되지 않은 기업들은 그 전 자료 사용
cond_tmp = (df_fs_monthly['Symbol'].isin(df_not_updated['Symbol'])) & (df_fs_monthly['FS_DATE'] == date_current)
df_fs_monthly.loc[cond_tmp, "FS_DATE"] = pd.to_datetime("20210301", errors='coerce', format='%Y%m%d')


########################################################################################################################
# FS_DATE: 일간 자료의 날짜를 매월 1일로 조정
processed_daily_sample["FS_DATE"] = \
    processed_daily_sample["Date"].dt.year * 10000 + processed_daily_sample["Date"].dt.month * 100 + 1
processed_daily_sample["FS_DATE"] = pd.to_datetime(processed_daily_sample["FS_DATE"], errors='coerce', format='%Y%m%d')

# FS_DATE 를 기준으로 매달 사용 가능한 최근 재무정보의 사용가능날짜 연결
processed_daily_sample = pd.merge(
    processed_daily_sample, df_fs_monthly[["Symbol", "FS_DATE", "사용가능날짜"]],
    left_on=["Symbol", "FS_DATE"], right_on=["Symbol", "FS_DATE"], how='left')

########################################################################################################################
# 사용가능날짜를 기준으로 재무제표 정보를 연결
cond = (fs_IFRSN["check_nan_123Q"] == False)

processed_daily_sample = pd.merge(
    processed_daily_sample, fs_IFRSN.loc[cond, ["Symbol", "사용가능날짜", "당기순이익(직전4분기)(천원)"]],
    left_on=["Symbol", "사용가능날짜"], right_on=["Symbol", "사용가능날짜"], how='left')


