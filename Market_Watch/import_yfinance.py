# Created by Kim Hyeongjun on 05/01/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.
# investpy 패키지의 종목명은 investing.com 에서 검색 가능
# pip install investpy --upgrade
# 빠르게 많이 받으면 ConnectionError: ERR#0015: error 429, try again later. 에러가 뜨므로
# sleep 함수와 VPN 서비스를 활용
# vpn 사용시 line speed 로 정렬 (9,8,7 순서이며 자릿수는 고려안함)

import pandas as pd
import numpy as np
# import investpy
import yfinance as yf
import datetime as dt
from time import sleep

# import matplotlib.pyplot as plt
# import mplfinance as mpf  # 캔들차트

DD_END_DATE = "26/05/2023"  # "DD/MM/YYYY"

sleep_secs = 5
########################################################################################################################
# KOSPI (1996.12.10 부터)
ks11 = yf.Ticker("^KS11")
yfinance_kospi0 = ks11.history(period="max")
yfinance_kospi1 = yfinance_kospi0.reset_index()
yfinance_kospi1["datetime"] = yfinance_kospi1["Date"].copy()
yfinance_kospi1['Date'] = yfinance_kospi1['datetime'].dt.date  # 날짜-시간 자료에서 날짜만 추출
yfinance_kospi1['Date'] = pd.to_datetime(yfinance_kospi1['Date'])  # Timezone 정보 제거
yfinance_kospi1.columns = [col if col == yfinance_kospi1.columns[0] else col + '_kospi' for col in yfinance_kospi1.columns]  # 첫번째 변수 외에 변수명에 _종목명 붙이기
yfinance_kospi = yfinance_kospi1.copy()
yfinance_kospi.to_pickle('./Market_Watch_Data/yfinance_kospi.pkl')
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤

# IEF (2002.07.30 부터)
ief = yf.Ticker("IEF")
yfinance_ief0 = ief.history(period="max")
yfinance_ief1 = yfinance_ief0.reset_index()
yfinance_ief1["datetime"] = yfinance_ief1["Date"].copy()
yfinance_ief1['Date'] = yfinance_ief1['datetime'].dt.date  # 날짜-시간 자료에서 날짜만 추출
yfinance_ief1['Date'] = pd.to_datetime(yfinance_ief1['Date'])  # Timezone 정보 제거
yfinance_ief1.columns = [col if col == yfinance_ief1.columns[0] else col + '_ief' for col in yfinance_ief1.columns]  # 첫번째 변수 외에 변수명에 _종목명 붙이기
yfinance_ief = yfinance_ief1.copy()
yfinance_ief.to_pickle('./Market_Watch_Data/yfinance_ief.pkl')
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤

# 달러/원 환율 (2003.12.01 부터)
usdkrw = yf.Ticker("KRW=X")
yfinance_usdkrw0 = usdkrw.history(period="max")
yfinance_usdkrw1 = yfinance_usdkrw0.reset_index()
yfinance_usdkrw1["datetime"] = yfinance_usdkrw1["Date"].copy()
yfinance_usdkrw1['Date'] = yfinance_usdkrw1['datetime'].dt.date  # 날짜-시간 자료에서 날짜만 추출
yfinance_usdkrw1['Date'] = pd.to_datetime(yfinance_usdkrw1['Date'])  # Timezone 정보 제거
yfinance_usdkrw1.columns = [col if col == yfinance_usdkrw1.columns[0] else col + '_usdkrw' for col in yfinance_usdkrw1.columns]  # 첫번째 변수 외에 변수명에 _종목명 붙이기
yfinance_usdkrw = yfinance_usdkrw1.copy()
yfinance_usdkrw.to_pickle('./Market_Watch_Data/yfinance_usdkrw.pkl')
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤

# 수익률 측정 위해서 병합
merged_df = pd.merge(yfinance_kospi, yfinance_ief, on='Date')
merged_df = pd.merge(merged_df, yfinance_usdkrw, on='Date')
merged_df["Close_ief_krw"] = merged_df["Close_ief"] * merged_df["Close_usdkrw"]

# Define the base date
base_date = '2023-03-23'
base_date_dt = dt.datetime.strptime(base_date, "%Y-%m-%d")

# Get the price on the base date
base_price_ief_krw = merged_df[merged_df['Date'] == base_date]['Close_ief_krw'].values[0]
base_price_kospi = merged_df[merged_df['Date'] == base_date]['Close_kospi'].values[0]

# Calculate the return compared to the base price
merged_df['return_kospi'] = merged_df['Close_kospi'] / base_price_kospi - 1
merged_df['return_ief'] = merged_df['Close_ief_krw'] / base_price_ief_krw - 1
merged_df['return_portfolio'] = 0.46*merged_df['return_kospi'] + 0.54*merged_df['return_ief']



# 그림 9.2 자산배분 포트폴리오 수익률 비교
# 시각화: 월별 시계열 자료 1개를 표시
import matplotlib.pyplot as plt
import seaborn as sns

fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300

colors = sns.color_palette('hls', 6)  # observation 개수만큼 색상 사용
plt.plot(merged_df.Date, merged_df["return_kospi"], color=colors[0], label="KOSPI")
plt.plot(merged_df.Date, merged_df["return_ief"], color=colors[1], label="IEF")
plt.plot(merged_df.Date, merged_df["return_portfolio"], color=colors[2], label="Portfolio")
xlim_start = dt.datetime.strptime("2023-03-23", "%Y-%m-%d")
xlim_end = dt.datetime.strptime("2023-05-26", "%Y-%m-%d")
plt.xlim(xlim_start, xlim_end)
plt.ylim(-0.10, 0.10)
#plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Index (2015.01 = 100)', fontsize=10)
plt.legend(loc='upper left')
plt.show()

plt.savefig("./Lecture_Figures_output/result_20230526.png")  # 그림 저장






########################################################################################################################
investpy.get_indices(country=None)
list_index_us = investpy.get_indices(country="United States")
list_index_us_search = list_index_us[list_index_us['full_name'].str.contains("MSCI")]

list_index_kr = investpy.get_indices(country="south korea")
list_index_kr_search = list_index_kr[list_index_kr['full_name'].str.contains("MSCI")]

list_index_kr2 = list_index_kr.sort_values(by=['name'])


# 미국 S&P 500 지수 (1979.12.26 부터)
investpy_snp500 = investpy.get_index_historical_data(
    index="S&P 500", country="United States", from_date="30/01/1900", to_date=DD_END_DATE)
investpy_snp500.to_pickle('./Market_Watch_Data/investpy_snp500.pkl')
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤

# 미국 MSCI US REIT 지수 (2015.01.12 부터)
investpy_msci_us_reit = investpy.get_index_historical_data(
    index="MSCI US REIT", country="United States", from_date="30/01/1900", to_date=DD_END_DATE)
investpy_msci_us_reit.to_pickle('./Market_Watch_Data/investpy_msci_us_reit.pkl')
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤


# KOSPI (1981.05.01 부터)
investpy_kospi = investpy.get_index_historical_data(
    index="KOSPI", country="south korea", from_date="30/01/1900", to_date=DD_END_DATE)
investpy_kospi.to_pickle('./Market_Watch_Data/investpy_kospi.pkl')
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤

# investpy 패키지를 사용하여 KOSPI 200 자료 받기
investpy_kospi_200 = investpy.get_index_historical_data(
    index="KOSPI 200", country="south korea", from_date="30/01/1900", to_date=DD_END_DATE)
investpy_kospi_200.to_pickle('./Market_Watch_Data/investpy_kospi_200.pkl')
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤

# KOSPI 200 Energy & Chemicals (KS200ENER)
investpy_KS200ENER = investpy.get_index_historical_data(
    index="KOSPI 200 Energy & Chemicals", country="south korea", from_date="30/01/1900", to_date=DD_END_DATE)
investpy_KS200ENER.to_pickle('./Market_Watch_Data/investpy_KS200ENER.pkl')
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤

# KRX Energy & Chemical (KRXENER)
investpy_KRXENER = investpy.get_index_historical_data(
    index="KRX Energy & Chemical", country="south korea", from_date="30/01/1900", to_date=DD_END_DATE)
investpy_KRXENER.to_pickle('./Market_Watch_Data/investpy_KRXENER.pkl')
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤

# KTB (2014.05.19 부터)
investpy_KTB = investpy.get_index_historical_data(
    index="KTB", country="south korea", from_date="30/01/1900", to_date=DD_END_DATE)
investpy_KTB.to_pickle('./Market_Watch_Data/investpy_KTB.pkl')
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤


########################################################################################################################
# Commodities
# investpy.get_commodities_list()

# Gold Futures (ZGJ2)
investpy_Gold = investpy.get_commodity_historical_data(
    commodity="Gold", from_date="30/01/1900", to_date=DD_END_DATE, country=None, as_json=False,
    order='ascending', interval='Daily')
investpy_Gold.to_pickle('./Market_Watch_Data/investpy_Gold.pkl')
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤

########################################################################################################################
# Crypto Currencies
# df_cryptos = investpy.get_cryptos()

investpy_bitcoin = investpy.get_crypto_historical_data(crypto='bitcoin', from_date="30/01/1900", to_date=DD_END_DATE,
                                                       interval='Daily')
investpy_bitcoin.to_pickle('./Market_Watch_Data/investpy_bitcoin.pkl')
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤

investpy_Ethereum = investpy.get_crypto_historical_data(crypto='Ethereum', from_date="30/01/1900", to_date=DD_END_DATE, interval='Daily')
investpy_Ethereum.to_pickle('./Market_Watch_Data/investpy_Ethereum.pkl')
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤

investpy_Ripple = investpy.get_crypto_historical_data(crypto='XRP', from_date="30/01/1900", to_date=DD_END_DATE, interval='Daily')
investpy_Ripple.to_pickle('./Market_Watch_Data/investpy_Ripple.pkl')
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤



########################################################################################################################
# investpy 패키지를 사용하여 삼성전자 자료 받기
investpy_005930 = investpy.get_stock_historical_data(
    stock="005930", country="south korea", from_date="30/01/1900", to_date=DD_END_DATE)
investpy_005930.to_pickle('./Market_Watch_Data/investpy_005930.pkl')
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤

########################################################################################################################
# investpy 패키지를 사용하여 ETF 자료 받기 (069500 = 코덱스200)
investpy_069500 = investpy.get_etf_historical_data(
    etf="Samsung KODEX KOSPI 200 Securities", country="south korea", from_date="30/01/1900", to_date=DD_END_DATE)
investpy_069500.to_pickle('./Market_Watch_Data/investpy_069500.pkl')
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤

# investpy 패키지를 사용하여 미국 국채 ETF 자료 받기 (IEF)
investpy_IEF = investpy.get_etf_historical_data(
    etf="iShares 7-10 Year Treasury Bond", country="United States", from_date="30/01/1900", to_date=DD_END_DATE)
investpy_IEF.to_pickle('./Market_Watch_Data/investpy_IEF.pkl')
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤

# investpy 패키지를 사용하여 한국 국채 ETF 자료 받기 (Kiwoom KOSEF 10Y Treasury Bond)
investpy_148070 = investpy.get_etf_historical_data(
    etf="Kiwoom KOSEF 10Y Treasury Bond", country="south korea", from_date="30/01/1900", to_date=DD_END_DATE)
investpy_148070.to_pickle('./Market_Watch_Data/investpy_148070.pkl')
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤

# 미국 ETF 리스트 검색
df_us_etf = investpy.get_etfs(country='United States')
df_us_etf_search = df_us_etf[df_us_etf['symbol'].str.contains("IEF")]
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤

# 한국 ETF 리스트 검색
df_kr_etf = investpy.get_etfs(country='south korea')
df_kr_etf_search = df_kr_etf[df_kr_etf['symbol'].str.contains("148070")]
df_kr_etf_search["name"]
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤

########################################################################################################################
# Economic Calendar
# investpy_economic_calendar_us_20000101_20220215 = investpy.economic_calendar(
#     countries=["united states"], from_date="01/01/2000", to_date="15/02/2022")
# investpy_economic_calendar_us_20000101_20220215.to_pickle('./Market_Watch_Data/investpy_economic_calendar_us_20000101_20220215.pkl')

# # Economic Calendar US (20000101~20220131)
# investpy_economic_calendar_us_20000101_20220131 = investpy.economic_calendar(
#     countries=["united states"], from_date="01/01/2000", to_date="31/01/2022")
# investpy_economic_calendar_us_20000101_20220131.to_pickle('./Market_Watch_Data/investpy_economic_calendar_us_20000101_20220131.pkl')

# Economic Calendar US (20000101~20220131)
investpy_economic_calendar_us_20000101_20220131 = \
    pd.read_pickle('./Market_Watch_Data/investpy_economic_calendar_us_20000101_20220131.pkl')

# Economic Calendar US (20220201~Current)
investpy_economic_calendar_us_20220201_current = investpy.economic_calendar(
    countries=["united states"], from_date="01/02/2022", to_date=DD_END_DATE)
investpy_economic_calendar_us_20220201_current.to_pickle(
    './Market_Watch_Data/investpy_economic_calendar_us_20220201_current.pkl')
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤

# Economic Calendar US 합치기
investpy_economic_calendar_us = pd.concat(
    [investpy_economic_calendar_us_20000101_20220131, investpy_economic_calendar_us_20220201_current])

# 데이터 저장
investpy_economic_calendar_us.to_pickle('./Market_Watch_Data/investpy_economic_calendar_us.pkl')


########################################################################################################################
# investpy 패키지를 사용하여 MSCI 자료 업데이트 받기
# MXEF: MSCI Emerging Markets Index
# MXWO: MSCI World Index

# 기존 데이터 불러오기
df_msci0 = pd.read_excel(
    './Market_Watch_Data/MSCI_19800101_20210430_MXEF_MXWO.xlsx', sheet_name="Sheet1", header=0, skiprows=4, skipfooter=0)

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

# investpy 로 업데이트
df_msci_em_update = investpy.get_index_historical_data(
    index="MSCI Emerging Markets", country="world", from_date="01/04/2021", to_date=DD_END_DATE)
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤

df_msci_world_update = investpy.get_index_historical_data(
    index="MSCI World", country="world", from_date="01/04/2021", to_date=DD_END_DATE)
sleep(sleep_secs)  # 에러 막기 위해 잠시 멈춤

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
df_msci_index.to_pickle('./Market_Watch_Data/investpy_msci.pkl')



########################################################################################################################
investpy_economic_calendar = pd.read_pickle('./Market_Watch_Data/investpy_economic_calendar_us_20000101_20220215.pkl')

investpy_PMI = investpy_economic_calendar[investpy_economic_calendar['event'].str.contains("ISM Manufacturing PMI")].copy()
investpy_PMI["datetime_announced"] = pd.to_datetime(investpy_PMI["date"], errors='coerce', format="%d/%m/%Y")
investpy_PMI["datetime"] = investpy_PMI["datetime_announced"] + pd.DateOffset(months=-1)
investpy_PMI["datetime"] = investpy_PMI["datetime"].apply(lambda dt: dt.replace(day=1))



########################################################################################################################
investpy_snp500 = pd.read_pickle('./Market_Watch_Data/investpy_snp500.pkl')
investpy_kospi = pd.read_pickle('./Market_Watch_Data/investpy_kospi.pkl')
investpy_snp500["snp500"] = investpy_snp500["Close"]
investpy_kospi["KOSPI"] = investpy_kospi["Close"]

investpy_index = pd.merge(investpy_snp500[["snp500"]], investpy_kospi[["KOSPI"]], left_index=True, right_index=True, how='outer')
investpy_index["snp500"] = investpy_index["snp500"].fillna(method='ffill')
investpy_index["KOSPI"] = investpy_index["KOSPI"].fillna(method='ffill')

dt_start = pd.to_datetime("2010-01-01", errors='coerce', format='%Y-%m-%d')
investpy_index = investpy_index[dt_start:]
investpy_index["snp500_2000"] = investpy_index["snp500"] / (investpy_index["snp500"][0]) * 100
investpy_index["KOSPI_2000"] = investpy_index["KOSPI"] / (investpy_index["KOSPI"][0]) * 100

# 시각화: 월별 시계열 자료 3개를 같은 y 축으로 표시
fig = plt.figure()
# fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
fig.set_size_inches(1800/300, 1200/300)  # 그래프 크기 지정, DPI=300

plt.plot(investpy_index.index, investpy_index["snp500_2000"], color='r', label="S&P 500 (2010=100)")
plt.plot(investpy_index.index, investpy_index["KOSPI_2000"], color='b', label="KOSPI (2010=100)")

# xlim_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')
# plt.xlim(xlim_start, )
#plt.ylim(-1, 20)
plt.axhline(y=100, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Index', fontsize=10)
plt.legend(loc='upper left')
plt.show()

plt.savefig("./BOK_processed/fig1.4_snp500_kospi.png")





df = investpy_snp500.copy()
df["Date"] = df.index
#Adding columns for weekly, monthly,6 month,Yearly,
df['WkEnd'] = df.Date.dt.to_period('W').apply(lambda r: r.start_time) + dt.timedelta(days=6)
df['MEnd'] = (df.Date.dt.to_period('M').apply(lambda r: r.end_time)).dt.date
df['6Mend'] = np.where(df.Date.dt.month <= 6, (df.Date.dt.year).astype(str)+'-1H',(df['Date'].dt.year).astype(str)+'-2H')
df['YEnd'] = (df.Date.dt.to_period('Y').apply(lambda r: r.end_time)).dt.date


# MDD (Maximum Drawdown) 계산하기
investpy_snp500_n = investpy_snp500.copy()
investpy_snp500_n.index = pd.to_datetime(investpy_snp500_n.index.values.astype('datetime64[M]'))
investpy_snp500_n.index

investpy_snp500.index
# We are going to use a trailing 252 trading day window

# Calculate the max drawdown in the past window days for each day in the series.
# Use min_periods=1 if you want to let the first 252 days data have an expanding window

# 52주 최고가 계산 (비영업일이 포함되므로 제외할 필요)
window = 52*7
Roll_Max = investpy_snp500['Close'].asfreq('D').rolling(window, min_periods=1).max()
Roll_idxmax = investpy_snp500['Close'].asfreq('D').rolling(window, min_periods=1).idxmax()

Daily_Drawdown = investpy_snp500['Close']/Roll_Max - 1.0
Max_Daily_Drawdown = Daily_Drawdown.asfreq('D').rolling(window, min_periods=1).min()

tmp = investpy_snp500.index[investpy_snp500['Close'].asfreq('D').rolling(window, min_periods=1).apply(np.argmax)[2:].astype(int)+np.arange(len(investpy_snp500)-2)]

# Next we calculate the minimum (negative) daily drawdown in that window.
# Again, use min_periods=1 if you want to allow the expanding window

# Plot the results
Daily_Drawdown.plot()
Max_Daily_Drawdown.plot()
plt.show()


investpy_snp500.index

investpy_snp500_A = investpy_snp500.resample("1Y")

investpy_snp500.Close.resample("1Y").first()
investpy_snp500.Close.resample("1Y").last()


# 그래프: 캔들차트 그리기
xlim_start = pd.to_datetime("2021-01-01", errors='coerce', format='%Y-%m-%d')
xlim_end = pd.to_datetime("2022-02-01", errors='coerce', format='%Y-%m-%d')
investpy_candle_chart = investpy_snp500[xlim_start:xlim_end]
# investpy_candle_chart.index = investpy_candle_chart["Date"]
# investpy_candle_chart = investpy_candle_chart[["Adj_Open", "Adj_High", "Adj_Low", "Adj_Close", "Volume"]]
# investpy_candle_chart = investpy_candle_chart.rename(columns={
#     "Adj_Open": "Open", "Adj_High": "High", "Adj_Low": "Low", "Adj_Close": "Close"})

# 그래프: 캔들차트 그리기
mpf.plot(investpy_candle_chart, title="S&P 500 Candle Chart", type="candle")

# 그래프: OHLC 차트 그리기
mpf.plot(investpy_candle_chart, title="S&P 500 OHLC Chart", type="ohlc")

# 그래프: 캔들차트(컬러) 그리기
kwargs = dict(title="S&P 500 Customized Chart", type="candle", mav=(2, 4, 6), volume=True, ylabel="OHLC Candles")
mc = mpf.make_marketcolors(up="r", down="b", inherit=True)
s = mpf.make_mpf_style(marketcolors=mc)
mpf.plot(investpy_candle_chart, **kwargs, style=s)



########################################################################################################################
# 현재 접근 가능한 국가 리스트
countriesAvailable = investpy.get_certificate_countries()
print(countriesAvailable)

# 현재 접근 가능한 주식
currentCountry = countriesAvailable[1]
stocks = investpy.get_stocks(currentCountry)
print(stocks)
print(type(stocks))

# 미국 ETF 리스트 검색
df_us_etf = investpy.get_etfs(country='United States')
df_us_etf_search = df_us_etf[df_us_etf['symbol'].str.contains("IEF")]


countriesAvailable = investpy.get_index_countries()

investpy.indices.get_indices_list(country=None)
list_indices = investpy.indices.get_indices_list(country='United States')


# investpy 패키지를 사용하여 KOSPI 자료 받기
investpy_kospi = investpy.get_index_historical_data(
    index="KOSPI", country="south korea", from_date="30/01/1900", to_date=DD_END_DATE)
investpy_kospi.reset_index(level=0, inplace=True)  # 날짜 인덱스를 칼럼으로
investpy_kospi.rename(
    columns={"Open": "KOSPI_Open", "High": "KOSPI_High", "Low": "KOSPI_Low", "Close": "KOSPI_Close"}, inplace=True)
investpy_kospi = investpy_kospi[["Date", "KOSPI_Open", "KOSPI_High", "KOSPI_Low", "KOSPI_Close"]]
investpy_kospi.sort_values(by=["Date"], inplace=True)

# 데이터 저장
investpy_kospi.to_pickle('./Market_Watch_Data/KOSPI_DAILY.pkl')
