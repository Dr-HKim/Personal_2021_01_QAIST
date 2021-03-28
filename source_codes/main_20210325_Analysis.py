# Created by Kim Hyeongjun on 03/22/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.
# pandas.Dataframe.rolling 이용하면 이동평균값을 구할 수 있다.
# df["mov30"] = df["Close"].rolling(30).mean()
# Finance Data Reader https://financedata.github.io/posts/finance-data-reader-users-guide.html
# 파이썬 판다스 주가 이동평균선 쉽게 계산하는 방법은? https://tariat.tistory.com/894
# 나만 모르는 파이썬 주식데이터 수집하는 방법 TOP3는? https://tariat.tistory.com/913
# 파이썬 실시간 주가, 주식시세 데이터 수집하는 방법은? https://tariat.tistory.com/892
# OHLC 데이터로 훈련하면 예쁜(?) 차트 찾는 것이 가능하지 않을까?
# pip install --upgrade mplfinance
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

########################################################################################################################
# # Import Pickle Dataset
# processed_daily_20000101_Current = pd.read_pickle('./data_processed/processed_daily_20000101_Current.pkl')
# processed_fs_1981_2020 = pd.read_pickle('./data_processed/processed_fs_1981_2020.pkl')
#
# # 재무제표 자료는 2011년 이후부터 분기별 자료 사용 가능
# sample_fs = processed_fs_1981_2020.loc[processed_fs_1981_2020["회계년"] > 2015]
#
# date_start = pd.to_datetime("20150101", errors='coerce', format='%Y%m%d')
# sample_daily = processed_daily_20000101_Current.loc[processed_daily_20000101_Current["Date"] > date_start]
#
# # 데이터 저장하기
# sample_fs.to_pickle('./data_processed/sample_fs.pkl')
# sample_daily.to_pickle('./data_processed/sample_daily.pkl')

########################################################################################################################
# Import Pickle Dataset
sample_fs = pd.read_pickle('./data_processed/sample_fs.pkl')
sample_daily = pd.read_pickle('./data_processed/sample_daily.pkl')

df_dataset = sample_daily.copy()
df_dataset = df_dataset.rename(columns={
    "Symbol Name": "Symbol_Name", "수정고가(원)": "Adj_High", "수정시가(원)": "Adj_Open", "수정저가(원)": "Adj_Low",
    "수정주가(원)": "Adj_Close", "거래량(주)": "Volume"})
df_dataset.index = df_dataset["Date"]


# 기업별로 수정주가(원) 30일 이동평균 구하기
df_dataset['MA30'] = df_dataset.groupby('Symbol')['Adj_Close'].transform(lambda x: x.rolling(5, 5).mean())

# 기업별로 수정주가(원) 30일 미래 이동평균 구하기 (forward-looking moving average)
df_dataset = df_dataset.iloc[::-1]
df_dataset['MA30_F'] = df_dataset.groupby('Symbol')['Adj_Close'].transform(lambda x: x.rolling(5, 5).mean())
df_dataset = df_dataset.iloc[::-1]

df_dataset['L1_Adj_Close'] = df_dataset.groupby('Symbol')['Adj_Close'].shift(1)
df_dataset['daily_return'] = (df_dataset["Adj_Close"] - df_dataset["L1_Adj_Close"])/df_dataset["Adj_Close"]


# 그래프: 일간 수익률 히스토그램 그리기
plt.hist(df_dataset.loc[df_dataset["Symbol Name"] == "삼성전자"]["daily_return"], bins=18)
plt.grid(True)
plt.show()


company_name = "삼성전자"
company_name = "NAVER"

date_start = pd.to_datetime("20200224", errors='coerce', format='%Y%m%d')
date_end = pd.to_datetime("20200403", errors='coerce', format='%Y%m%d')
cond_data = (df_dataset["Symbol_Name"] == company_name) & \
            (df_dataset["Date"] >= date_start) & \
            (df_dataset["Date"] <= date_end)
tmp = df_dataset.loc[cond_data]

company_code = "A005930"
company_code = "A035420"

date_start = pd.to_datetime("20200224", errors='coerce', format='%Y%m%d')
date_end = pd.to_datetime("20200403", errors='coerce', format='%Y%m%d')
cond_data = (df_dataset["Symbol"] == company_code) & \
            (df_dataset["Date"] >= date_start) & \
            (df_dataset["Date"] <= date_end)
tmp = df_dataset.loc[cond_data]
# 그래프: 날짜와 종가로 차트 그리기
plt.title("Adjusted Price")
plt.xticks(rotation=45)
plt.plot(df_dataset.loc[cond_data]["Date"],
         df_dataset.loc[cond_data]["Adj_Close"], "co-")
plt.grid(color="gray", linestyle="--")
plt.show()

# 그래프: 캔들차트 그리기
df_candle_chart = df_dataset.loc[cond_data]
df_candle_chart.index = df_candle_chart["Date"]
df_candle_chart = df_candle_chart[["Adj_Open", "Adj_High", "Adj_Low", "Adj_Close", "Volume"]]
df_candle_chart = df_candle_chart.rename(columns={
    "Adj_Open": "Open", "Adj_High": "High", "Adj_Low": "Low", "Adj_Close": "Close"})

# 그래프: 캔들차트 그리기
mpf.plot(df_candle_chart, title="Celltrion candle chart", type="candle")

# 그래프: OHLC 차트 그리기
mpf.plot(df_candle_chart, title="Celltrion OHLC chart", type="ohlc")

# 그래프: 캔들차트(컬러) 그리기
kwargs = dict(title="Celltrion Customized Chart", type="candle", mav=(2, 4, 6), volume=True, ylabel="OHLC Candles")
mc = mpf.make_marketcolors(up="r", down="b", inherit=True)
s = mpf.make_mpf_style(marketcolors=mc)
mpf.plot(df_candle_chart, **kwargs, style=s)


company_list = ["삼성전자", "SK하이닉스", "현대차", "NAVER"]
date_start = pd.to_datetime("20160104", errors='coerce', format='%Y%m%d')
date_end = pd.to_datetime("20180427", errors='coerce', format='%Y%m%d')

df_company_data = pd.DataFrame()
for company in company_list:
    cond_data = (df_dataset["Symbol_Name"] == company) & \
                (df_dataset["Date"] >= date_start) & \
                (df_dataset["Date"] <= date_end)

    df_adj_close = df_dataset.loc[cond_data]["Adj_Close"]
    df_company_data[company] = df_adj_close
    print(company)
    print(df_adj_close.head())

df_daily_return = df_company_data.pct_change()
df_annual_return = df_daily_return.mean()*252
df_daily_cov = df_daily_return.cov()
df_annual_cov = df_daily_cov*252

import numpy as np

list_portfolio_return = []
list_portfolio_risk = []
list_portfolio_weights = []
list_portfolio_sharpe = []

for _ in range(20000):
    portfolio_weights = np.random.random(len(company_list))
    portfolio_weights /= np.sum(portfolio_weights)

    portfolio_return = np.dot(portfolio_weights, df_annual_return)
    portfolio_risk = np.sqrt(np.dot(portfolio_weights.T, np.dot(df_annual_cov, portfolio_weights)))

    list_portfolio_return.append(portfolio_return)
    list_portfolio_risk.append(portfolio_risk)
    list_portfolio_weights.append(portfolio_weights)
    list_portfolio_sharpe.append(portfolio_return/portfolio_risk)

portfolio = {"Returns": list_portfolio_return, "Risk": list_portfolio_risk, "Sharpe": list_portfolio_sharpe}

for i, s in enumerate(company_list):
    portfolio[s] = [weight[i] for weight in list_portfolio_weights]

df_portfolio = pd.DataFrame(portfolio)

df_portfolio = df_portfolio[["Returns", "Risk", "Sharpe"] + [s for s in company_list]]

max_sharpe = df_portfolio.loc[df_portfolio["Sharpe"] == df_portfolio["Sharpe"].max()]
min_risk = df_portfolio[df_portfolio["Risk"] == df_portfolio["Risk"].min()]

df_portfolio.plot.scatter(x="Risk", y="Returns", figsize=(10,7), grid=True)
plt.title("Efficient Frontier")
plt.xlabel("Risk")
plt.ylabel("Expected Returns")
plt.show()


df_portfolio.plot.scatter(x="Risk", y="Returns", c="Sharpe", cmap="viridis", edgecolors="k", figsize=(11, 7), grid=True)
plt.scatter(x=max_sharpe["Risk"], y=max_sharpe["Returns"], c="r", marker="*", s=300)
plt.scatter(x=min_risk["Risk"], y=min_risk["Returns"], c="r", marker="X", s=200)
plt.title("Portfolio Optimization")
plt.xlabel("Risk")
plt.ylabel("Expected Returns")
plt.show()