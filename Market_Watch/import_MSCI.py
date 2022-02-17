# Created by Kim Hyeongjun on 05/01/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.

import pandas as pd
import investpy
from datetime import datetime
import matplotlib.pyplot as plt


def get_yyyymm_add_months(n_yyyymm, n_months):
    n_yyyy, n_mm = divmod(n_yyyymm, 100)
    n_months_y, n_months_m = divmod(n_mm + n_months - 1, 12)
    output_yyyy = n_yyyy + n_months_y
    output_mm = n_months_m + 1
    output_yyyymm = output_yyyy * 100 + output_mm
    return output_yyyymm


def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny+dy, maxy+dy)


DD_END_DATE = "28/12/2021"

########################################################################################################################
# MXEF: MSCI Emerging Markets Index
# MXWO: MSCI World Index

# 데이터 불러오기
df_msci0 = pd.read_excel(
    './BOK_raw/MSCI_19800101_20210430_MXEF_MXWO.xlsx', sheet_name="Sheet1", header=0, skiprows=4, skipfooter=0)

# 변수명 바꾸기
df_msci0.rename(columns={
    "Dates": "Date",
    "PX_LAST": "MXEF_Close", "PX_OPEN": "MXEF_Open", "PX_HIGH": "MXEF_High", "PX_LOW": "MXEF_Low",
    "PX_LAST.1": "MXWO_Close", "PX_OPEN.1": "MXWO_Open", "PX_HIGH.1": "MXWO_High", "PX_LOW.1": "MXWO_Low"},
    inplace=True)

# 20210331 자료까지만 사용
df_msci1 = df_msci0[df_msci0["Date"] < pd.to_datetime("20210401", errors='coerce', format='%Y%m%d')]

# 필요한 변수만 추려내기
df_msci_em0 = df_msci1[["Date", "MXEF_Open", "MXEF_High", "MXEF_Low", "MXEF_Close"]]
df_msci_world0 = df_msci1[["Date", "MXWO_Open", "MXWO_High", "MXWO_Low", "MXWO_Close"]]

########################################################################################################################
# investpy 패키지를 사용하여 MSCI 자료 업데이트 받기
df_msci_em_update = investpy.get_index_historical_data(
    index="MSCI Emerging Markets", country="world", from_date="01/04/2021", to_date=DD_END_DATE)
df_msci_world_update = investpy.get_index_historical_data(
    index="MSCI World", country="world", from_date="01/04/2021", to_date=DD_END_DATE)

df_msci_em_update.reset_index(level=0, inplace=True)
df_msci_world_update.reset_index(level=0, inplace=True)

# 변수명 바꾸기
df_msci_em_update.rename(
    columns={"Open": "MXEF_Open", "High": "MXEF_High", "Low": "MXEF_Low", "Close": "MXEF_Close"}, inplace=True)
df_msci_world_update.rename(
    columns={"Open": "MXWO_Open", "High": "MXWO_High", "Low": "MXWO_Low", "Close": "MXWO_Close"}, inplace=True)

# 필요한 변수만 추려내기
df_msci_em_update = df_msci_em_update[["Date", "MXEF_Open", "MXEF_High", "MXEF_Low", "MXEF_Close"]]
df_msci_world_update = df_msci_world_update[["Date", "MXWO_Open", "MXWO_High", "MXWO_Low", "MXWO_Close"]]

# 블룸버그 + investpy 업데이트 자료 합치기
df_msci_em1 = pd.concat([df_msci_em0, df_msci_em_update])
df_msci_world1 = pd.concat([df_msci_world0, df_msci_world_update])

# MSCI Wold, MSCI Emerging Markets 데이터 합치고 정렬
df_msci_index = pd.merge(df_msci_em1, df_msci_world1, left_on="Date", right_on="Date", how="outer")
df_msci_index.sort_values(by=["Date"], inplace=True)

# 데이터 저장
df_msci_index.to_pickle('./BOK_raw/MSCI_DAILY.pkl')


########################################################################################################################
# investpy 패키지를 사용하여 KOSPI 자료 받기
df_kospi = investpy.get_index_historical_data(
    index="KOSPI", country="south korea", from_date="30/01/1900", to_date=DD_END_DATE)
df_kospi.reset_index(level=0, inplace=True)  # 날짜 인덱스를 칼럼으로
df_kospi.rename(
    columns={"Open": "KOSPI_Open", "High": "KOSPI_High", "Low": "KOSPI_Low", "Close": "KOSPI_Close"}, inplace=True)
df_kospi = df_kospi[["Date", "KOSPI_Open", "KOSPI_High", "KOSPI_Low", "KOSPI_Close"]]
df_kospi.sort_values(by=["Date"], inplace=True)

# 데이터 저장
df_kospi.to_pickle('./BOK_raw/KOSPI_DAILY.pkl')
