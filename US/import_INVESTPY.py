# Created by Kim Hyeongjun on 05/01/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.
# investpy 패키지의 종목명은 investing.com 에서 검색 가능
import pandas as pd
import numpy as np
import investpy
import mplfinance as mpf
import datetime as dt
import matplotlib.pyplot as plt

DD_END_DATE = "30/01/2022"

# 미국 S&P 500 지수 (1979.12.26 부터)
df_snp500 = investpy.get_index_historical_data(
    index="S&P 500", country="United States", from_date="30/01/1900", to_date=DD_END_DATE)
df_snp500.to_pickle('./US_raw/df_snp500.pkl')

# investpy 패키지를 사용하여 KOSPI 자료 받기
df_kospi = investpy.get_index_historical_data(
    index="KOSPI", country="south korea", from_date="30/01/1900", to_date=DD_END_DATE)
df_kospi.to_pickle('./US_raw/df_kospi.pkl')



df_snp500 = pd.read_pickle('./US_raw/df_snp500.pkl')
df_kospi = pd.read_pickle('./US_raw/df_kospi.pkl')
df_snp500["snp500"] = df_snp500["Close"]
df_kospi["KOSPI"] = df_kospi["Close"]

df_index = pd.merge(df_snp500[["snp500"]], df_kospi[["KOSPI"]], left_index=True, right_index=True, how='outer')
df_index["snp500"] = df_index["snp500"].fillna(method='ffill')
df_index["KOSPI"] = df_index["KOSPI"].fillna(method='ffill')

dt_start = pd.to_datetime("2010-01-01", errors='coerce', format='%Y-%m-%d')
df_index = df_index[dt_start:]
df_index["snp500_2000"] = df_index["snp500"] / (df_index["snp500"][0]) * 100
df_index["KOSPI_2000"] = df_index["KOSPI"] / (df_index["KOSPI"][0]) * 100

# 시각화: 월별 시계열 자료 3개를 같은 y 축으로 표시
fig = plt.figure()
# fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
fig.set_size_inches(1800/300, 1200/300)  # 그래프 크기 지정, DPI=300

plt.plot(df_index.index, df_index["snp500_2000"], color='r', label="S&P 500 (2010=100)")
plt.plot(df_index.index, df_index["KOSPI_2000"], color='b', label="KOSPI (2010=100)")

# xlim_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')
# plt.xlim(xlim_start, )
#plt.ylim(-1, 20)
plt.axhline(y=100, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Index', fontsize=10)
plt.legend(loc='upper left')
plt.show()

plt.savefig("./BOK_processed/fig1.4_snp500_kospi.png")





df = df_snp500.copy()
df["Date"] = df.index
#Adding columns for weekly, monthly,6 month,Yearly,
df['WkEnd'] = df.Date.dt.to_period('W').apply(lambda r: r.start_time) + dt.timedelta(days=6)
df['MEnd'] = (df.Date.dt.to_period('M').apply(lambda r: r.end_time)).dt.date
df['6Mend'] = np.where(df.Date.dt.month <= 6, (df.Date.dt.year).astype(str)+'-1H',(df['Date'].dt.year).astype(str)+'-2H')
df['YEnd'] = (df.Date.dt.to_period('Y').apply(lambda r: r.end_time)).dt.date


# MDD (Maximum Drawdown) 계산하기
df_snp500_n = df_snp500.copy()
df_snp500_n.index = pd.to_datetime(df_snp500_n.index.values.astype('datetime64[M]'))
df_snp500_n.index

df_snp500.index
# We are going to use a trailing 252 trading day window

# Calculate the max drawdown in the past window days for each day in the series.
# Use min_periods=1 if you want to let the first 252 days data have an expanding window

# 52주 최고가 계산 (비영업일이 포함되므로 제외할 필요)
window = 52*7
Roll_Max = df_snp500['Close'].asfreq('D').rolling(window, min_periods=1).max()
Roll_idxmax = df_snp500['Close'].asfreq('D').rolling(window, min_periods=1).idxmax()

Daily_Drawdown = df_snp500['Close']/Roll_Max - 1.0
Max_Daily_Drawdown = Daily_Drawdown.asfreq('D').rolling(window, min_periods=1).min()

tmp = df_snp500.index[df_snp500['Close'].asfreq('D').rolling(window, min_periods=1).apply(np.argmax)[2:].astype(int)+np.arange(len(df_snp500)-2)]

# Next we calculate the minimum (negative) daily drawdown in that window.
# Again, use min_periods=1 if you want to allow the expanding window

# Plot the results
Daily_Drawdown.plot()
Max_Daily_Drawdown.plot()
plt.show()


df_snp500.index

df_snp500_A = df_snp500.resample("1Y")

df_snp500.Close.resample("1Y").first()
df_snp500.Close.resample("1Y").last()


# 그래프: 캔들차트 그리기
xlim_start = pd.to_datetime("2021-01-01", errors='coerce', format='%Y-%m-%d')
xlim_end = pd.to_datetime("2022-02-01", errors='coerce', format='%Y-%m-%d')
df_candle_chart = df_snp500[xlim_start:xlim_end]
# df_candle_chart.index = df_candle_chart["Date"]
# df_candle_chart = df_candle_chart[["Adj_Open", "Adj_High", "Adj_Low", "Adj_Close", "Volume"]]
# df_candle_chart = df_candle_chart.rename(columns={
#     "Adj_Open": "Open", "Adj_High": "High", "Adj_Low": "Low", "Adj_Close": "Close"})

# 그래프: 캔들차트 그리기
mpf.plot(df_candle_chart, title="S&P 500 Candle Chart", type="candle")

# 그래프: OHLC 차트 그리기
mpf.plot(df_candle_chart, title="S&P 500 OHLC Chart", type="ohlc")

# 그래프: 캔들차트(컬러) 그리기
kwargs = dict(title="S&P 500 Customized Chart", type="candle", mav=(2, 4, 6), volume=True, ylabel="OHLC Candles")
mc = mpf.make_marketcolors(up="r", down="b", inherit=True)
s = mpf.make_mpf_style(marketcolors=mc)
mpf.plot(df_candle_chart, **kwargs, style=s)



########################################################################################################################
# 현재 접근 가능한 국가 리스트
countriesAvailable = investpy.get_certificate_countries()
print(countriesAvailable)

# 현재 접근 가능한 주식
currentCountry = countriesAvailable[1]
stocks = investpy.get_stocks(currentCountry)
print(stocks)
print(type(stocks))

# 미국 ETF 리스트
df = investpy.get_etfs(country='United States')

countriesAvailable = investpy.get_index_countries()

investpy.indices.get_indices_list(country=None)
list_indices = investpy.indices.get_indices_list(country='United States')


# investpy 패키지를 사용하여 KOSPI 자료 받기
df_kospi = investpy.get_index_historical_data(
    index="KOSPI", country="south korea", from_date="30/01/1900", to_date=DD_END_DATE)
df_kospi.reset_index(level=0, inplace=True)  # 날짜 인덱스를 칼럼으로
df_kospi.rename(
    columns={"Open": "KOSPI_Open", "High": "KOSPI_High", "Low": "KOSPI_Low", "Close": "KOSPI_Close"}, inplace=True)
df_kospi = df_kospi[["Date", "KOSPI_Open", "KOSPI_High", "KOSPI_Low", "KOSPI_Close"]]
df_kospi.sort_values(by=["Date"], inplace=True)

# 데이터 저장
df_kospi.to_pickle('./US_raw/KOSPI_DAILY.pkl')
