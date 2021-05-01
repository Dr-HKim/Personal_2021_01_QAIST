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


########################################################################################################################
# MXEF: MSCI Emerging Markets Index
# MXWO: MSCI World Index

# 데이터 불러오기
df_msci0 = pd.read_excel(
    './data_raw/msci_index.xlsx', sheet_name="Sheet1", header=0, skiprows=4, skipfooter=0)

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

# investpy 패키지를 사용하여 MSCI 자료 업데이트 받기
df_msci_em_update = investpy.get_index_historical_data(
    index="MSCI Emerging Markets", country="world", from_date="01/04/2021", to_date="30/04/2021")
df_msci_world_update = investpy.get_index_historical_data(
    index="MSCI World", country="world", from_date="01/04/2021", to_date="30/04/2021")

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

# investpy 패키지를 사용하여 KOSPI 자료 받기
df_kospi = investpy.get_index_historical_data(
    index="KOSPI", country="south korea", from_date="30/01/1900", to_date="30/04/2021")
df_kospi.reset_index(level=0, inplace=True)  # 날짜 인덱스를 칼럼으로
df_kospi.rename(
    columns={"Open": "KOSPI_Open", "High": "KOSPI_High", "Low": "KOSPI_Low", "Close": "KOSPI_Close"}, inplace=True)
df_kospi = df_kospi[["Date", "KOSPI_Open", "KOSPI_High", "KOSPI_Low", "KOSPI_Close"]]

# MSCI Wold, MSCI Emerging Markets, KOSPI 데이터 합치고 정렬
df_index_daily = pd.merge(df_msci_em1, df_msci_world1, left_on="Date", right_on="Date", how="outer")
df_index_daily = pd.merge(df_index_daily, df_kospi, left_on="Date", right_on="Date", how="outer")
df_index_daily.sort_values(by=["Date"], inplace=True)


# 데이터 저장
df_index_daily.to_pickle('./data_processed/df_index_daily_20210430.pkl')

########################################################################################################################
# 데이터 불러오기
df_index_daily0 = pd.read_pickle('./data_processed/df_index_daily_20210430.pkl')

# Daily to Monthly
# 날짜를 YYYYMM 형태로 변환
df_index_daily0["YYYYMM"] = df_index_daily0["Date"].dt.year * 100 + df_index_daily0["Date"].dt.month

# YYYYMM 그룹별 OHLC 구하기
df_index_monthly0 = df_index_daily0.groupby(by='YYYYMM', as_index=False).agg({
    "MXEF_Close": "last", "MXEF_Open": "first", "MXEF_High": "max", "MXEF_Low": "min",
    "MXWO_Close": "last", "MXWO_Open": "first", "MXWO_High": "max", "MXWO_Low": "min",
    "KOSPI_Close": "last", "KOSPI_Open": "first", "KOSPI_High": "max", "KOSPI_Low": "min"})

# YYYYMM 을 기준으로 그 달의 가장 마지막 날짜 입력
df_index_monthly0["Date"] = pd.to_datetime(
    get_yyyymm_add_months(df_index_monthly0["YYYYMM"], 1) * 100 + 1, errors='coerce', format='%Y%m%d') + pd.Timedelta(days=-1)

########################################################################################################################
# 그림: MSCI Emerging Markets and KOSPI

fig, ax1 = plt.subplots()

color1 = "tab:red"
ax1.set_xlim([pd.to_datetime("1990-01-01 00:00:00"), pd.to_datetime("2021-03-31 00:00:00")])
ax1.set_xlabel("Date")
ax1.set_ylabel("KOSPI(1980.1.4=100)", color=color1)
ax1.plot(df_index_monthly0["Date"], df_index_monthly0["KOSPI_Close"], color=color1)
ax1.tick_params(axis="y")

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color2 = "tab:blue"
ax2.set_ylabel("MSCI Emerging Markets (1987.12.31=100)", color=color2)  # we already handled the x-label with ax1
ax2.plot(df_index_monthly0["Date"], df_index_monthly0["MXEF_Close"], color=color2, linestyle='-')
ax2.tick_params(axis='y')

fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.set_size_inches(2400/300, 1800/300)  # 그래프 크기 지정, DPI=300
align_yaxis(ax1, 0, ax2, 0)  # 두 축이 동일한 0 값을 가지도록 조정
plt.show()

# 그림 저장
plt.savefig("./data_processed/fig3_kospi_and_msci_emerging_markets.png")

########################################################################################################################
