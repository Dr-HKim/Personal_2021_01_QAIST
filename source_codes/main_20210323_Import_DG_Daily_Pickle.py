# Created by Kim Hyeongjun on 03/22/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.

import pandas as pd


def get_processed_daily_data(dg_daily, dg_header):
    row_index = dg_daily.iloc[:, 0]  # 첫번째 열의 자료를 인덱스로 설정
    dg_daily_data = dg_daily.iloc[:, 1:]  # 두번째 열부터 데이터 따로 저장
    dg_daily_data.index = row_index  # row 인덱스 설정

    symbol_names = dg_header.iloc[0, 1:]
    item_names = dg_header.iloc[4, 1:]
    column_index = pd.MultiIndex.from_arrays([symbol_names, item_names], names=["Symbol", "Item"])
    dg_daily_data.columns = column_index  # column 인덱스 설정

    dg_daily_data_stacked = dg_daily_data.stack(level=0).reset_index()
    dg_daily_data_stacked = dg_daily_data_stacked.rename(columns={0: "Date"})
    dg_daily_data_stacked = dg_daily_data_stacked.sort_values(by=["Symbol", "Date"])
    dg_daily_data_stacked = dg_daily_data_stacked.reset_index(drop=True)

    cols = dg_daily_data_stacked.columns.tolist()
    new_cols = [cols[1], cols[0], cols[2], cols[3], cols[4], cols[5], cols[6]]
    dg_daily_data_stacked = dg_daily_data_stacked[new_cols]

    return dg_daily_data_stacked


########################################################################################################################
# Import Pickle Dataset
dg_daily1_test = pd.read_pickle('./data_processed/dg_daily1_test.pkl')
dg_daily2_test = pd.read_pickle('./data_processed/dg_daily2_test.pkl')
dg_daily3_test = pd.read_pickle('./data_processed/dg_daily3_test.pkl')
dg_header1_test = pd.read_pickle('./data_processed/dg_header1_test.pkl')
dg_header2_test = pd.read_pickle('./data_processed/dg_header2_test.pkl')
dg_header3_test = pd.read_pickle('./data_processed/dg_header3_test.pkl')

dg_daily1_20000101_20201231 = pd.read_pickle('./data_processed/dg_daily1_20000101_20201231.pkl')
dg_daily2_20000101_20201231 = pd.read_pickle('./data_processed/dg_daily2_20000101_20201231.pkl')
dg_daily3_20000101_20201231 = pd.read_pickle('./data_processed/dg_daily3_20000101_20201231.pkl')
dg_header1_20000101_20201231 = pd.read_pickle('./data_processed/dg_header1_20000101_20201231.pkl')
dg_header2_20000101_20201231 = pd.read_pickle('./data_processed/dg_header2_20000101_20201231.pkl')
dg_header3_20000101_20201231 = pd.read_pickle('./data_processed/dg_header3_20000101_20201231.pkl')

dg_daily1_20210101_Current = pd.read_pickle('./data_processed/dg_daily1_20210101_Current.pkl')
dg_daily2_20210101_Current = pd.read_pickle('./data_processed/dg_daily2_20210101_Current.pkl')
dg_daily3_20210101_Current = pd.read_pickle('./data_processed/dg_daily3_20210101_Current.pkl')
dg_header1_20210101_Current = pd.read_pickle('./data_processed/dg_header1_20210101_Current.pkl')
dg_header2_20210101_Current = pd.read_pickle('./data_processed/dg_header2_20210101_Current.pkl')
dg_header3_20210101_Current = pd.read_pickle('./data_processed/dg_header3_20210101_Current.pkl')


########################################################################################################################
# 자료 병합 테스트
processed_daily1 = get_processed_daily_data(dg_daily1_test, dg_header1_test)
processed_daily2 = get_processed_daily_data(dg_daily2_test, dg_header2_test)
processed_daily3 = get_processed_daily_data(dg_daily3_test, dg_header3_test)

processed_daily = pd.merge(processed_daily1, processed_daily2, left_on=["Date", "Symbol"], right_on=["Date", "Symbol"], how='outer')
processed_daily = pd.merge(processed_daily, processed_daily3, left_on=["Date", "Symbol"], right_on=["Date", "Symbol"], how='outer')

# 20000101 부터 20201231 까지 자료 병합
processed_daily1_20000101_20201231 = get_processed_daily_data(dg_daily1_20000101_20201231, dg_header1_20000101_20201231)
processed_daily2_20000101_20201231 = get_processed_daily_data(dg_daily2_20000101_20201231, dg_header2_20000101_20201231)
processed_daily3_20000101_20201231 = get_processed_daily_data(dg_daily3_20000101_20201231, dg_header3_20000101_20201231)

processed_daily_20000101_20201231 = pd.merge(processed_daily1_20000101_20201231, processed_daily2_20000101_20201231, left_on=["Date", "Symbol"], right_on=["Date", "Symbol"], how='outer')
processed_daily_20000101_20201231 = pd.merge(processed_daily_20000101_20201231, processed_daily3_20000101_20201231, left_on=["Date", "Symbol"], right_on=["Date", "Symbol"], how='outer')

# 20210101 부터 Current 까지 자료 병합
processed_daily1_20210101_Current = get_processed_daily_data(dg_daily1_20210101_Current, dg_header1_20210101_Current)
processed_daily2_20210101_Current = get_processed_daily_data(dg_daily2_20210101_Current, dg_header2_20210101_Current)
processed_daily3_20210101_Current = get_processed_daily_data(dg_daily3_20210101_Current, dg_header3_20210101_Current)

processed_daily_20210101_Current = pd.merge(processed_daily1_20210101_Current, processed_daily2_20210101_Current, left_on=["Date", "Symbol"], right_on=["Date", "Symbol"], how='outer')
processed_daily_20210101_Current = pd.merge(processed_daily_20210101_Current, processed_daily3_20210101_Current, left_on=["Date", "Symbol"], right_on=["Date", "Symbol"], how='outer')

########################################################################################################################
# 모든 자료를 합치고 정렬
processed_daily_20000101_Current = pd.concat([processed_daily_20000101_20201231, processed_daily_20210101_Current])
processed_daily_20000101_Current = processed_daily_20000101_Current.sort_values(by=["Symbol", "Date"])

# df_symbol_names 생성: Symbol 과 Symbol Name 을 연결하는 자료
df_symbol_names0 = dg_header1_20210101_Current.transpose()
column_index = df_symbol_names0.iloc[0, :]  # 첫번째 열의 자료를 인덱스로 설정
df_symbol_names1 = df_symbol_names0.iloc[1:, :]  # 두번째 열부터 데이터 따로 저장
df_symbol_names1.columns = column_index  # row 인덱스 설정
df_symbol_names2 = df_symbol_names1.loc[df_symbol_names1["Item Name"]=="기준가(원)"]
df_symbol_names = df_symbol_names2[["Symbol", "Symbol Name"]]

# Symbol Name 을 연결하고 자료 순서 바꾸기
processed_daily_20000101_Current = pd.merge(processed_daily_20000101_Current, df_symbol_names, left_on=["Symbol"], right_on=["Symbol"], how='outer')
column_names = processed_daily_20000101_Current.columns.tolist()
new_column_names1 = [column_names[0], column_names[-1]]
new_column_names2 = column_names[1:-1]
new_column_names = new_column_names1 + new_column_names2
processed_daily_20000101_Current = processed_daily_20000101_Current[new_column_names]

# NaN 데이터 제거하기
processed_daily_20000101_Current = processed_daily_20000101_Current[~pd.isnull(processed_daily_20000101_Current["Date"])]

# 데이터 저장하기
processed_daily_20000101_Current.to_pickle('./data_processed/processed_daily_20000101_Current.pkl')