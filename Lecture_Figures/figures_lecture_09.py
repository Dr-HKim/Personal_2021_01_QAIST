# 9강 자산배분

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny+dy, maxy+dy)


def get_yyyymm_add_months(n_yyyymm, n_months):
    n_yyyy, n_mm = divmod(n_yyyymm, 100)
    n_months_y, n_months_m = divmod(n_mm + n_months - 1, 12)
    output_yyyy = n_yyyy + n_months_y
    output_mm = n_months_m + 1
    output_yyyymm = output_yyyy * 100 + output_mm
    return output_yyyymm


########################################################################################################################
# 8.8.2.1 평균환율, 기말환율 > 주요국통화의 대원화 환율 통계자료 [036Y004][HY,MM,QQ,YY] (1964.05 부터)
BOK_036Y004 = pd.read_pickle('./Market_Watch_Data/BOK_036Y004.pkl')
BOK_036Y004_00 = BOK_036Y004[(BOK_036Y004["ITEM_CODE1"] == "0000001") & (BOK_036Y004["ITEM_CODE2"] == "0000200")].copy()  # 원달러환율 말일자료
BOK_036Y004_00["usdkrw"] = BOK_036Y004_00["DATA_VALUE"]

# 7.4.2 소비자물가지수(2015=100)(전국, 특수분류)  [021Y126][MM,QQ,YY] (1975.01 부터)
BOK_021Y126 = pd.read_pickle('./Market_Watch_Data/BOK_021Y126.pkl')
BOK_021Y126_00 = BOK_021Y126[BOK_021Y126["ITEM_CODE1"] == "00"].copy()  # 총지수
BOK_021Y126_00["cpi"] = BOK_021Y126_00["DATA_VALUE"]

# 7.7.1 주택매매가격지수(KB) [085Y021][MM,QQ,YY] (1986.01 부터)
BOK_085Y021 = pd.read_pickle('./Market_Watch_Data/BOK_085Y021.pkl')
BOK_085Y021_00 = BOK_085Y021[BOK_085Y021["ITEM_NAME1"] == "총지수"].copy()  # 총지수
BOK_085Y021_01 = BOK_085Y021[BOK_085Y021["ITEM_NAME1"] == "아파트"].copy()  # 총지수
BOK_085Y021_00["hpi"] = BOK_085Y021_00["DATA_VALUE"]
BOK_085Y021_01["apt_hpi"] = BOK_085Y021_01["DATA_VALUE"]

# 6.1.1 증권/재정 - 주식거래 및 주가지수 - 주식시장(일별) [064Y001] (1995.01.03 부터)
BOK_064Y001 = pd.read_pickle('./Market_Watch_Data/BOK_064Y001.pkl')
BOK_064Y001_01 = BOK_064Y001[BOK_064Y001["ITEM_CODE1"] == "0001000"].copy()  # KOSPI지수 / 코스피
BOK_064Y001_01["kospi"] = BOK_064Y001_01["DATA_VALUE"]
BOK_064Y001_01.index = BOK_064Y001_01["DATETIME"]

# 4.1.2 시장금리(월,분기,년) [028Y001] (1987.01, 1987Q1, 1987 부터)
BOK_028Y001 = pd.read_pickle('./Market_Watch_Data/BOK_028Y001.pkl')
BOK_028Y001_AA = BOK_028Y001[BOK_028Y001["ITEM_NAME1"] == "회사채(3년, AA-)"].copy()
BOK_028Y001_AA["cb_rate_aa"] = BOK_028Y001_AA["DATA_VALUE"]

# 미국 ETF 데이터 불러오기
yahoo_SPY = pd.read_csv('./Market_Watch_Data/yahoo_SPY.csv', header=0, encoding='utf-8', low_memory=False)
yahoo_IEF = pd.read_csv('./Market_Watch_Data/yahoo_IEF.csv', header=0, encoding='utf-8', low_memory=False)
yahoo_VNQ = pd.read_csv('./Market_Watch_Data/yahoo_VNQ.csv', header=0, encoding='utf-8', low_memory=False)
yahoo_HYG = pd.read_csv('./Market_Watch_Data/yahoo_HYG.csv', header=0, encoding='utf-8', low_memory=False)
yahoo_132030ks = pd.read_csv('./Market_Watch_Data/yahoo_132030.KS.csv', header=0, encoding='utf-8', low_memory=False)
yahoo_148070ks = pd.read_csv('./Market_Watch_Data/yahoo_148070.KS.csv', header=0, encoding='utf-8', low_memory=False)

yahoo_SPY["spy"] = yahoo_SPY["Close"]
yahoo_IEF["ief"] = yahoo_IEF["Close"]
yahoo_VNQ["vnq"] = yahoo_VNQ["Close"]
yahoo_HYG["hyg"] = yahoo_HYG["Close"]
yahoo_132030ks["gold"] = yahoo_132030ks["Close"]
yahoo_148070ks["ktb10y"] = yahoo_148070ks["Close"]

yahoo_SPY["datetime"] = pd.to_datetime(yahoo_SPY["Date"], errors='coerce', format='%Y-%m-%d')
yahoo_IEF["datetime"] = pd.to_datetime(yahoo_IEF["Date"], errors='coerce', format='%Y-%m-%d')
yahoo_VNQ["datetime"] = pd.to_datetime(yahoo_VNQ["Date"], errors='coerce', format='%Y-%m-%d')
yahoo_HYG["datetime"] = pd.to_datetime(yahoo_HYG["Date"], errors='coerce', format='%Y-%m-%d')
yahoo_132030ks["datetime"] = pd.to_datetime(yahoo_132030ks["Date"], errors='coerce', format='%Y-%m-%d')
yahoo_148070ks["datetime"] = pd.to_datetime(yahoo_148070ks["Date"], errors='coerce', format='%Y-%m-%d')

yahoo_SPY.index = yahoo_SPY["datetime"]
yahoo_IEF.index = yahoo_IEF["datetime"]
yahoo_VNQ.index = yahoo_VNQ["datetime"]
yahoo_HYG.index = yahoo_HYG["datetime"]
yahoo_132030ks.index = yahoo_132030ks["datetime"]
yahoo_148070ks.index = yahoo_148070ks["datetime"]

df_kospi_monthly = BOK_064Y001_01.resample('M').last()
df_spy_monthly = yahoo_SPY.resample('M').last()
df_ief_monthly = yahoo_IEF.resample('M').last()
df_vnq_monthly = yahoo_VNQ.resample('M').last()
df_hyg_monthly = yahoo_HYG.resample('M').last()
df_gold_monthly = yahoo_132030ks.resample('M').last()
df_ktb10y_monthly = yahoo_148070ks.resample('M').last()

df_kospi_monthly["DATETIME"] = df_kospi_monthly["DATETIME"].apply(lambda dt: dt.replace(day=1))
df_spy_monthly["datetime"] = df_spy_monthly["datetime"].apply(lambda dt: dt.replace(day=1))
df_ief_monthly["datetime"] = df_ief_monthly["datetime"].apply(lambda dt: dt.replace(day=1))
df_vnq_monthly["datetime"] = df_vnq_monthly["datetime"].apply(lambda dt: dt.replace(day=1))
df_hyg_monthly["datetime"] = df_hyg_monthly["datetime"].apply(lambda dt: dt.replace(day=1))
df_gold_monthly["datetime"] = df_gold_monthly["datetime"].apply(lambda dt: dt.replace(day=1))
df_ktb10y_monthly["datetime"] = df_ktb10y_monthly["datetime"].apply(lambda dt: dt.replace(day=1))

df_kospi_monthly.index = df_kospi_monthly["DATETIME"]
df_spy_monthly.index = df_spy_monthly["datetime"]
df_ief_monthly.index = df_ief_monthly["datetime"]
df_vnq_monthly.index = df_vnq_monthly["datetime"]
df_hyg_monthly.index = df_hyg_monthly["datetime"]
df_gold_monthly.index = df_gold_monthly["datetime"]
df_ktb10y_monthly.index = df_ktb10y_monthly["datetime"]

# 하나로 합친 데이터프레임 만들기
df_data = BOK_021Y126_00[["DATETIME", "cpi"]]
df_data = pd.merge(df_data, BOK_085Y021_00[["DATETIME", "hpi"]], left_on='DATETIME', right_on='DATETIME', how='left')
df_data = pd.merge(df_data, BOK_085Y021_01[["DATETIME", "apt_hpi"]], left_on='DATETIME', right_on='DATETIME', how='left')
df_data = pd.merge(df_data, BOK_028Y001_AA[["DATETIME", "cb_rate_aa"]], left_on='DATETIME', right_on='DATETIME', how='left')
df_data = pd.merge(df_data, BOK_036Y004_00[["DATETIME", "usdkrw"]], left_on='DATETIME', right_on='DATETIME', how='left')
df_data = pd.merge(df_data, df_kospi_monthly[["kospi"]], left_on='DATETIME', right_index=True, how='left')
df_data = pd.merge(df_data, df_spy_monthly[["spy"]], left_on='DATETIME', right_index=True, how='left')
df_data = pd.merge(df_data, df_ief_monthly[["ief"]], left_on='DATETIME', right_index=True, how='left')
df_data = pd.merge(df_data, df_vnq_monthly[["vnq"]], left_on='DATETIME', right_index=True, how='left')
df_data = pd.merge(df_data, df_hyg_monthly[["hyg"]], left_on='DATETIME', right_index=True, how='left')
df_data = pd.merge(df_data, df_gold_monthly[["gold"]], left_on='DATETIME', right_index=True, how='left')
df_data = pd.merge(df_data, df_ktb10y_monthly[["ktb10y"]], left_on='DATETIME', right_index=True, how='left')

df_data["spy_krw"] = df_data["spy"] * df_data["usdkrw"]  # 환율 보정
df_data["ief_krw"] = df_data["ief"] * df_data["usdkrw"]  # 환율 보정
df_data["vnq_krw"] = df_data["vnq"] * df_data["usdkrw"]  # 환율 보정
df_data["hyg_krw"] = df_data["hyg"] * df_data["usdkrw"]  # 환율 보정

n_available = 321  # 2011-11-01
df_data["index_cpi"] = df_data["cpi"] / (df_data.iloc[n_available, ]["cpi"]) * 100
df_data["index_apt_hpi"] = df_data["apt_hpi"] / (df_data.iloc[n_available, ]["apt_hpi"]) * 100
df_data["index_kospi"] = df_data["kospi"] / (df_data.iloc[n_available, ]["kospi"]) * 100
df_data["index_spy"] = df_data["spy_krw"] / (df_data.iloc[n_available, ]["spy_krw"]) * 100
df_data["index_ief"] = df_data["ief_krw"] / (df_data.iloc[n_available, ]["ief_krw"]) * 100
df_data["index_vnq"] = df_data["vnq_krw"] / (df_data.iloc[n_available, ]["vnq_krw"]) * 100
df_data["index_hyg"] = df_data["hyg_krw"] / (df_data.iloc[n_available, ]["hyg_krw"]) * 100
df_data["index_gold"] = df_data["gold"] / (df_data.iloc[n_available, ]["gold"]) * 100
df_data["index_ktb10y"] = df_data["ktb10y"] / (df_data.iloc[n_available, ]["ktb10y"]) * 100

n_available2 = 321  # 211 부터 적용 가능 (2002-08-01)
df_data["index_kospi2"] = df_data["kospi"] / (df_data.iloc[n_available2, ]["kospi"]) * 100
df_data["index_ief2"] = df_data["ief_krw"] / (df_data.iloc[n_available2, ]["ief_krw"]) * 100

df_data["index_portfolio73"] = df_data["index_kospi2"] * 0.7 + df_data["index_ief2"] * 0.3
df_data["index_portfolio55"] = df_data["index_kospi2"] * 0.5 + df_data["index_ief2"] * 0.5
df_data["index_portfolio37"] = df_data["index_kospi2"] * 0.3 + df_data["index_ief2"] * 0.7

df_data['KOSPI'] = df_data['index_kospi'].pct_change(1)
df_data['KTB10Y'] = df_data['index_ktb10y'].pct_change(1)
df_data['APT'] = df_data['index_apt_hpi'].pct_change(1)
df_data['SPY'] = df_data['index_spy'].pct_change(1)
df_data['IEF'] = df_data['index_ief'].pct_change(1)
df_data['HYG'] = df_data['index_hyg'].pct_change(1)
df_data['VNQ'] = df_data['index_vnq'].pct_change(1)
df_data['GOLD'] = df_data['index_gold'].pct_change(1)

list_assets = ["KOSPI", "KTB10Y", "APT", "SPY", "IEF", "HYG", "VNQ", "GOLD", ]
dt_start = pd.to_datetime("2011-11-01", errors='coerce', format='%Y-%m-%d')
dt_end = pd.to_datetime("2022-02-01", errors='coerce', format='%Y-%m-%d')

df_graph = df_data[(df_data["DATETIME"] >= dt_start) & (df_data["DATETIME"] <= dt_end)]

df_graph[list_assets].corr()

########################################################################################################################
# 그림 9.1 주요 자산 간 상관관계
fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
sns.heatmap(
    data=df_graph[list_assets].corr(), annot=True, fmt='.2f', linewidths=.5, center=0,
    cmap=sns.diverging_palette(220, 20, as_cmap=True))

plt.savefig("./Lecture_Figures_output/fig9.1_assets_correlation_heatmap.png")  # 그림 저장

########################################################################################################################
# 그림 9.2 자산배분 포트폴리오 수익률 비교
# 시각화: 월별 시계열 자료 1개를 표시
fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300

colors = sns.color_palette('hls', 6)  # observation 개수만큼 색상 사용
plt.plot(df_data["DATETIME"], df_data["index_kospi2"], color=colors[0], label="KOSPI")
plt.plot(df_data["DATETIME"], df_data["index_portfolio73"], color=colors[1], label="Portfolio 73")
plt.plot(df_data["DATETIME"], df_data["index_portfolio55"], color=colors[2], label="Portfolio 55")
plt.plot(df_data["DATETIME"], df_data["index_portfolio37"], color=colors[3], label="Portfolio 37")
plt.plot(df_data["DATETIME"], df_data["index_ief2"], color=colors[4], label="IEF")

xlim_start = pd.to_datetime("2011-10-01", errors='coerce', format='%Y-%m-%d')
plt.xlim(xlim_start, )
plt.ylim(80, 180)
#plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Index (2011.11 = 100)', fontsize=10)
plt.legend(loc='upper left')
plt.show()

plt.savefig("./Lecture_Figures_output/fig9.2_asset_allocation_returns.png")  # 그림 저장

########################################################################################################################
# Markowiz 포트폴리오

selected_assets = ["KOSPI", "IEF"]
df_assets = df_graph[selected_assets].copy()

np.random.seed(42)
num_ports = 6000
all_weights = np.zeros((num_ports, len(selected_assets)))
ret_arr = np.zeros(num_ports)
vol_arr = np.zeros(num_ports)
sharpe_arr = np.zeros(num_ports)

for x in range(num_ports):
    # Weights
    weights = np.array(np.random.random(len(selected_assets)))
    weights = weights / np.sum(weights)

    # Save weights
    all_weights[x, :] = weights

    # Expected return
    ret_arr[x] = np.sum((df_assets.mean() * weights * 252))

    # Expected volatility
    vol_arr[x] = np.sqrt(np.dot(weights.T, np.dot(df_assets.cov() * 252, weights)))

    # Sharpe Ratio
    sharpe_arr[x] = ret_arr[x] / vol_arr[x]

sharpe_arr.max()
all_weights[sharpe_arr.argmax(), :]
max_sr_vol = vol_arr[sharpe_arr.argmax()]
max_sr_ret = ret_arr[sharpe_arr.argmax()]

plt.figure(figsize=(12, 8))
plt.scatter(vol_arr, ret_arr, c=sharpe_arr, cmap='viridis')
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('Volatility')
plt.ylabel('Return')
plt.scatter(max_sr_vol, max_sr_ret, c='red', s=50)  # red dot
plt.scatter(np.sqrt(df_assets.iloc[:, 0].var() * 252), df_assets.iloc[:, 0].mean() * 252, c='red', s=50)  # red dot
plt.scatter(np.sqrt(df_assets.iloc[:, 1].var() * 252), df_assets.iloc[:, 1].mean() * 252, c='red', s=50)  # red dot
plt.show()


