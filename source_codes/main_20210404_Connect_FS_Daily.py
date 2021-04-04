# Created by Kim Hyeongjun on 03/22/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.

import pandas as pd
import numpy as np

########################################################################################################################
# Import Pickle Dataset
fs_IFRSC = pd.read_pickle('./data_processed/fs_IFRSC.pkl')
fs_IFRSC_sample = pd.read_pickle('./data_processed/fs_IFRSC_sample.pkl')
dg_GeneralHistoric_Annual = pd.read_pickle('./data_processed/dg_GeneralHistoric_Annual.pkl')
dg_GeneralHistoric_Quarterly = pd.read_pickle('./data_processed/dg_GeneralHistoric_Quarterly.pkl')

# df_dataset = fs_IFRSC_sample[fs_IFRSC_sample["회계년"] <= 2021].copy()
df_dataset = fs_IFRSC.copy()
########################################################################################################################
# 각 주기(1Q, 2Q, 3Q, 4Q) 별로 결산월이 (3, 6, 9, 12) 가 아니라 (12, 12, 12, 12) 로 입력된 자료들이 있다.
# 이런 자료들은 분기 데이터가 없고 annual 자료만 있을 가능성 높다. 따라서 골라내야 한다.

# 인덱스 자료(Symbol, Name, 결산월, 회계년, 주기)만 따로 저장
df_index0 = df_dataset.iloc[:, 0:6]

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

# 주기(1Q, 2Q, 3Q, 4Q)에 따라 결산월자료가 모두 동일하면 1, 아니면 0 을 입력
cond_same_settle_month = \
    (df_index3["1Q"] == df_index3["2Q"]) & (df_index3["1Q"] == df_index3["3Q"]) & (df_index3["1Q"] == df_index3["4Q"])
df_index3['d_same_settle_month'] = np.where(cond_same_settle_month, 1, 0)

# 1,2,3분기의 총자산이 nan이고 4분기 총자산이 입력되어 있는 경우를 표시
cond_nan_123Q = np.isnan(df_index3["AT_1Q"]) & np.isnan(df_index3["AT_2Q"]) & np.isnan(df_index3["AT_3Q"]) & (~np.isnan(df_index3["AT_4Q"]))
df_index3['d_nan_123Q'] = np.where(cond_nan_123Q, 1, 0)

# 기업x회계년 마다 더미변수를 연결
df_index4 = pd.merge(
    df_index0, df_index3[["Symbol", "회계년", "d_same_settle_month", "d_nan_123Q"]],
    left_on=["Symbol", "회계년"], right_on=["Symbol", "회계년"], how='left')

# 기업x회계년 마다 GeneralHistoric_Quarterly 연결
df_index5 = pd.merge(
    df_index4, dg_GeneralHistoric_Quarterly[["Symbol", "회계년", "주기", "결산월(Hist)", "거래소(시장)"]],
    left_on=["Symbol", "회계년", "주기"], right_on=["Symbol", "회계년", "주기"], how='left')


# 기업코드 별로 결산월(Hist) 값이 모두 비어있는 기업코드 체크
check_null_settle_month = df_index5.groupby("Symbol")['결산월(Hist)'].apply(lambda x: x.isnull().all())

# 기업코드 별로 결산월(Hist) 값이 하나인(unique) 기업코드 체크
check_unique_settle_month = df_index5.groupby(df_index5["Symbol"])["결산월(Hist)"].nunique().eq(1)

df_index5 = pd.merge(df_index5, check_null_settle_month, left_on=["Symbol"], right_index=True, how='left')
df_index5.rename(columns={"결산월(Hist)_x":"결산월(Hist)", "결산월(Hist)_y":"check_null_settle_month"}, inplace=True)
df_index5 = pd.merge(df_index5, check_unique_settle_month, left_on=["Symbol"], right_index=True, how='left')
df_index5.rename(columns={"결산월(Hist)_x":"결산월(Hist)", "결산월(Hist)_y":"check_unique_settle_month"}, inplace=True)

########################################################################################################################



# tmp = df_index5[(df_index5["check_null_settle_month"] == False) & (df_index5["check_unique_settle_month"] == False)]
tmp = df_index5[(df_index5["결산월(Hist)"] == 11)]
tmp2 = df_index5[(df_index5["Name"] == "농우바이오")]

########################################################################################################################
# 기업x회계년 마다 더미변수를 연결
df_dataset1 = pd.merge(
    df_dataset, df_index1[["Symbol", "회계년", "d_same_settle_month"]],
    left_on=["Symbol", "회계년"], right_on=["Symbol", "회계년"], how='left')


# 이베스트투자증권 결산월이 3월에서 12월로 변경
# 유유제약 결산월 3월에서 9월로 변경 2017년

