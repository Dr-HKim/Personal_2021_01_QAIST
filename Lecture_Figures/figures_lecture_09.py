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
# 한국 주식
# KOSPI (1981.05.01 부터)
investpy_kospi = pd.read_pickle('./Market_Watch_Data/investpy_kospi.pkl')
investpy_kospi["KOSPI"] = investpy_kospi["Close"]
investpy_kospi_monthly = investpy_kospi.resample('M').last()  # 월말 자료만
investpy_kospi_monthly.index = investpy_kospi_monthly.index.map(lambda t: t.replace(day=1))  # 인덱스 날짜를 1일로
sr_KOSPI = investpy_kospi_monthly["KOSPI"]

# 1.5.1.1. 주식/채권/재정 - 주식거래/주가지수 - 주식시장(일) [802Y001][D] (1995.01.03 부터)
BOK_802Y001 = pd.read_pickle('./Market_Watch_Data/BOK_802Y001.pkl')
BOK_802Y001_01 = BOK_802Y001[BOK_802Y001["ITEM_CODE1"] == "0001000"].copy()  # KOSPI지수 / 코스피
BOK_802Y001_01["KOSPI"] = BOK_802Y001_01["DATA_VALUE"]
BOK_802Y001_01.index = BOK_802Y001_01["DATETIME"]

# 한국 국채
# 1.3.2.2. 시장금리(월,분기,년) [721Y001][A,M,Q] (1987.01, 1987Q1, 1987 부터)
BOK_721Y001 = pd.read_pickle('./Market_Watch_Data/BOK_721Y001.pkl')
BOK_721Y001_AA = BOK_721Y001[BOK_721Y001["ITEM_NAME1"] == "회사채(3년, AA-)"].copy()
BOK_721Y001_AA["CB(AA-)"] = BOK_721Y001_AA["DATA_VALUE"]
BOK_721Y001_KTB10Y = BOK_721Y001[BOK_721Y001["ITEM_NAME1"] == "국고채(10년)"].copy()
BOK_721Y001_KTB10Y["KTB10Y"] = BOK_721Y001_KTB10Y["DATA_VALUE"]
BOK_721Y001_KTB10Y.index = BOK_721Y001_KTB10Y["DATETIME"]
sr_KTB10Y_yield = BOK_721Y001_KTB10Y["KTB10Y"]

# KOSEF 국고채 10년 (2011.10.21 부터)
yahoo_148070ks = pd.read_csv('./Market_Watch_Data/yahoo_148070.KS.csv', header=0, encoding='utf-8', low_memory=False)
yahoo_148070ks["datetime"] = pd.to_datetime(yahoo_148070ks["Date"], errors='coerce', format='%Y-%m-%d')
yahoo_148070ks.index = yahoo_148070ks["datetime"]
yahoo_148070ks_monthly = yahoo_148070ks.resample('M').last()  # 월말 자료만
yahoo_148070ks_monthly.index = yahoo_148070ks_monthly.index.map(lambda t: t.replace(day=1))  # 인덱스 날짜를 1일로
sr_KTB10Y = yahoo_148070ks_monthly["Close"]

# 한국 부동산
# 4.4.1.1. 주택매매가격지수(KB) [901Y062][M] (1986.01 부터)
BOK_901Y062 = pd.read_pickle('./Market_Watch_Data/BOK_901Y062.pkl')
BOK_901Y062_00 = BOK_901Y062[BOK_901Y062["ITEM_NAME1"] == "총지수"].copy()  # 총지수
BOK_901Y062_01 = BOK_901Y062[BOK_901Y062["ITEM_NAME1"] == "아파트"].copy()  # 총지수
BOK_901Y062_00["HPI"] = BOK_901Y062_00["DATA_VALUE"]
BOK_901Y062_01["HPI(APT)"] = BOK_901Y062_01["DATA_VALUE"]
BOK_901Y062_01.index = BOK_901Y062_01["DATETIME"]
sr_HPI_APT = BOK_901Y062_01["HPI(APT)"]

# 한국 물가
# 4.2.1 소비자물가지수(2020=100)(전국, 특수분류) [901Y010][A,M,Q] (1975.01 부터)
BOK_901Y010 = pd.read_pickle('./Market_Watch_Data/BOK_901Y010.pkl')
BOK_901Y010_00 = BOK_901Y010[BOK_901Y010["ITEM_CODE1"] == "00"].copy()  # 총지수
BOK_901Y010_00["CPI"] = BOK_901Y010_00["DATA_VALUE"]
BOK_901Y010_00.index = BOK_901Y010_00["DATETIME"]
sr_CPI = BOK_901Y010_00["CPI"]

# 달러/원 환율
# 3.1.2.1. 평균환율/기말환율 > 주요국통화의 대원화 환율 [731Y004][A,M,Q,S] (1964.05 부터)
BOK_731Y004 = pd.read_pickle('./Market_Watch_Data/BOK_731Y004.pkl')
BOK_731Y004_00 = BOK_731Y004[(BOK_731Y004["ITEM_CODE1"] == "0000001") & (BOK_731Y004["ITEM_CODE2"] == "0000200")].copy()  # 원달러환율 말일자료
BOK_731Y004_00["USDKRW"] = BOK_731Y004_00["DATA_VALUE"]
BOK_731Y004_00.index = BOK_731Y004_00["DATETIME"]
sr_USDKRW = BOK_731Y004_00["USDKRW"]

# 미국 주식
# 미국 S&P 500 지수 (1979.12.26 부터)
investpy_snp500 = pd.read_pickle('./Market_Watch_Data/investpy_snp500.pkl')
investpy_snp500_monthly = investpy_snp500.resample('M').last()  # 월말 자료만
investpy_snp500_monthly.index = investpy_snp500_monthly.index.map(lambda t: t.replace(day=1))  # 인덱스 날짜를 1일로
sr_SNP500 = investpy_snp500_monthly["Close"]

# 미국 국채 인덱스 (10년 만기)
# 자료는 대략 1942.01 부터
wrds_index_treasury = pd.read_csv('./WRDS_raw/wrds_index_treasury.csv', header=0, encoding='utf-8', low_memory=False)
wrds_index_treasury["datetime"] = pd.to_datetime(wrds_index_treasury["caldt"], errors='coerce', format='%Y%m%d')
wrds_index_treasury.index = wrds_index_treasury["datetime"]
wrds_index_treasury_monthly = wrds_index_treasury.resample('M').last()  # 월말 자료만
wrds_index_treasury_monthly.index = wrds_index_treasury_monthly.index.map(lambda t: t.replace(day=1))  # 인덱스 날짜를 1일로
wrds_index_treasury_monthly = wrds_index_treasury_monthly[wrds_index_treasury_monthly["caldt"] > 19420000]
sr_TB10Y = wrds_index_treasury_monthly["b10ind"]

# # ICE BofA 7-10 Year US Corporate Index Total Return Index Value (BAMLCC4A0710YTRIV)
# fred_BAMLCC4A0710YTRIV = pd.read_pickle('./Market_Watch_Data/fred_BAMLCC4A0710YTRIV.pkl')
# sr_TB10Y = fred_BAMLCC4A0710YTRIV.resample('M').last()  # 월말 자료만
# sr_TB10Y.index = sr_TB10Y.index.map(lambda t: t.replace(day=1))  # 인덱스 날짜를 1일로

# Yahoo Finance
# Treasury Yield 10 Years (^TNX) : 국채 인덱스로 이걸 쓰는게 더 나을지도
# ICE Futures - ICE Futures Real Time Price. Currency in USD

# 미국 국채 수익률
# Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity (DGS10)
fred_DGS10 = pd.read_pickle('./Market_Watch_Data/fred_DGS10.pkl')
sr_TB10Y_yield = fred_DGS10.resample('M').last()  # 월말 자료만
sr_TB10Y_yield.index = sr_TB10Y_yield.index.map(lambda t: t.replace(day=1))  # 인덱스 날짜를 1일로

# IEF ETF
yahoo_IEF = pd.read_csv('./Market_Watch_Data/yahoo_IEF.csv', header=0, encoding='utf-8', low_memory=False)
yahoo_IEF["datetime"] = pd.to_datetime(yahoo_IEF["Date"], errors='coerce', format='%Y-%m-%d')
yahoo_IEF.index = yahoo_IEF["datetime"]
yahoo_IEF["IEF"] = yahoo_IEF["Close"]
yahoo_IEF_monthly = yahoo_IEF.resample('M').last()
yahoo_IEF_monthly.index = yahoo_IEF_monthly.index.map(lambda t: t.replace(day=1))  # 인덱스 날짜를 1일로
sr_IEF = yahoo_IEF_monthly["IEF"]

# 미국 부동산 (배당 재투자)
# Wilshire US Real Estate Investment Trust Total Market Index (Wilshire US REIT) (WILLREITIND)
fred_WILLREITIND = pd.read_pickle('./Market_Watch_Data/fred_WILLREITIND.pkl')
sr_REIT = fred_WILLREITIND.resample('M').last()  # 월말 자료만
sr_REIT.index = sr_REIT.index.map(lambda t: t.replace(day=1))  # 인덱스 날짜를 1일로

# 금 (달러)
# Gold Futures (ZGJ2)
investpy_Gold = pd.read_pickle('./Market_Watch_Data/investpy_Gold.pkl')
investpy_Gold_monthly = investpy_Gold.resample('M').last()  # 월말 자료만
investpy_Gold_monthly.index = investpy_Gold_monthly.index.map(lambda t: t.replace(day=1))  # 인덱스 날짜를 1일로
sr_GOLD = investpy_Gold_monthly["Close"]

# 비트코인
investpy_bitcoin = pd.read_pickle('./Market_Watch_Data/investpy_bitcoin.pkl')
investpy_bitcoin_monthly = investpy_bitcoin.resample('M').last()  # 월말 자료만
investpy_bitcoin_monthly.index = investpy_bitcoin_monthly.index.map(lambda t: t.replace(day=1))  # 인덱스 날짜를 1일로
sr_bitcoin = investpy_bitcoin_monthly["Close"]

########################################################################################################################
# 자산 데이터 합치기
df_assets = pd.DataFrame({'KOSPI': sr_KOSPI.values})
df_assets.index = sr_KOSPI.index
df_assets = df_assets.merge(sr_KTB10Y.rename('KTB10Y'), left_index=True, right_index=True, how='outer')
df_assets = df_assets.merge(sr_KTB10Y_yield.rename('KTB10Y_yield'), left_index=True, right_index=True, how='outer')
df_assets = df_assets.merge(sr_HPI_APT.rename('HPI_APT'), left_index=True, right_index=True, how='outer')
df_assets = df_assets.merge(sr_CPI.rename('CPI'), left_index=True, right_index=True, how='outer')
df_assets = df_assets.merge(sr_USDKRW.rename('USDKRW'), left_index=True, right_index=True, how='outer')
df_assets = df_assets.merge(sr_SNP500.rename('SNP500'), left_index=True, right_index=True, how='outer')
df_assets = df_assets.merge(sr_TB10Y.rename('TB10Y'), left_index=True, right_index=True, how='outer')
df_assets = df_assets.merge(sr_TB10Y_yield.rename('TB10Y_yield'), left_index=True, right_index=True, how='outer')
df_assets = df_assets.merge(sr_IEF.rename('IEF'), left_index=True, right_index=True, how='outer')
df_assets = df_assets.merge(sr_REIT.rename('REIT'), left_index=True, right_index=True, how='outer')
df_assets = df_assets.merge(sr_GOLD.rename('GOLD'), left_index=True, right_index=True, how='outer')
df_assets = df_assets.merge(sr_bitcoin.rename('Bitcoin'), left_index=True, right_index=True, how='outer')

# 달러 자산 환율 보정
df_assets["SNP500_KRW"] = df_assets["SNP500"] * df_assets["USDKRW"]  # 환율 보정
df_assets["TB10Y_KRW"] = df_assets["TB10Y"] * df_assets["USDKRW"]  # 환율 보정
df_assets["IEF_KRW"] = df_assets["IEF"] * df_assets["USDKRW"]  # 환율 보정
df_assets["REIT_KRW"] = df_assets["REIT"] * df_assets["USDKRW"]  # 환율 보정
df_assets["GOLD_KRW"] = df_assets["GOLD"] * df_assets["USDKRW"]  # 환율 보정

# 월별 수익률
df_assets_return = df_assets[["KOSPI"]].copy()
df_assets_return['KOSPI'] = df_assets['KOSPI'].pct_change(12, fill_method=None)
df_assets_return['KTB10Y'] = df_assets['KTB10Y'].pct_change(12, fill_method=None)
df_assets_return['KTB10Y_yield'] = df_assets['KTB10Y_yield'] / 100
df_assets_return['HPI_APT'] = df_assets['HPI_APT'].pct_change(12, fill_method=None)
# df_assets_return['CPI'] = df_assets['CPI'].pct_change(1, fill_method=None)
# df_assets_return['USDKRW'] = df_assets['USDKRW'].pct_change(1, fill_method=None)
df_assets_return['S&P500'] = df_assets['SNP500_KRW'].pct_change(12, fill_method=None)
df_assets_return['TB10Y'] = df_assets['TB10Y_KRW'].pct_change(12, fill_method=None)
df_assets_return['IEF'] = df_assets['IEF_KRW'].pct_change(12, fill_method=None)
df_assets_return['TB10Y_yield'] = df_assets['TB10Y_yield'] / 100
df_assets_return['REIT'] = df_assets['REIT_KRW'].pct_change(12, fill_method=None)
df_assets_return['GOLD'] = df_assets['GOLD_KRW'].pct_change(12, fill_method=None)

########################################################################################################################
# Dynamic Asset Correlation Heatmap
# 5년 / 10년 간 monthly rollover 하면서 heatmap 그리기
# KOSPI 1981.06 부터, HPI_APT 1986.01 부터, KTB10Y_yield 는 2000.11 부터
obs_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')
obs_end = pd.to_datetime("2021-12-01", errors='coerce', format='%Y-%m-%d')
df_assets_return_obs = df_assets_return[obs_start:obs_end]

list_assets = ["KOSPI", "KTB10Y", "HPI_APT", "S&P500", "TB10Y", "REIT", "GOLD"]
df_assets_return_obs = df_assets_return_obs[list_assets]

len(df_assets_return_obs) - 120

n_years = 10

# for i in range(0, len(df_assets_return_obs) - 12*n_years + 1):
#     df_tmp = df_assets_return_obs.iloc[i:n_years*12 + i]
#
#     fig = plt.figure()
#     fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
#     sns.heatmap(
#         data=df_tmp.corr(), annot=True, fmt='.2f', linewidths=.5, center=0,
#         cmap=sns.diverging_palette(220, 20, as_cmap=True), vmin=-1, vmax=1)
#
#     yyyymm0 = df_tmp.first_valid_index().year*100 + df_tmp.first_valid_index().month
#     yyyymm1 = df_tmp.last_valid_index().year*100 + df_tmp.last_valid_index().month
#
#     filename = "heatmap_" + str(n_years) + "Y_" + str(yyyymm0) + "_" + str(yyyymm1) + ".png"
#     plt.title('Correlation Heatmap ' + str(yyyymm0) + " - " + str(yyyymm1))
#     plt.savefig("./Lecture_Figures_output/heatmap_" + str(n_years) + "Y/" + filename)  # 그림 저장
#     plt.close()


########################################################################################################################
# Asset Correlation Heatmap (1990년 이후 전체 기간)
# KOSPI 1981.06 부터, HPI_APT 1986.01 부터, KTB10Y_yield 는 2000.11 부터, KTB10Y 는 2012.10 부터
obs_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')
obs_end = pd.to_datetime("2021-12-01", errors='coerce', format='%Y-%m-%d')
df_assets_return_obs = df_assets_return[obs_start:obs_end]

list_assets = ["KOSPI", "KTB10Y", "HPI_APT", "S&P500", "TB10Y", "REIT", "GOLD"]
df_assets_return_obs = df_assets_return_obs[list_assets]
df_assets_return_obs["KTB10Y"] = np.nan

fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
sns.heatmap(
    data=df_assets_return_obs.corr(), annot=True, fmt='.2f', linewidths=.5, center=0,
    cmap=sns.diverging_palette(220, 20, as_cmap=True), vmin=-1, vmax=1)

plt.savefig("./Lecture_Figures_output/fig9.1_assets_correlation_heatmap_1990.png")  # 그림 저장

# 2000년 이후
obs_start1 = pd.to_datetime("2000-01-01", errors='coerce', format='%Y-%m-%d')

fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
sns.heatmap(
    data=df_assets_return_obs[obs_start1:].corr(), annot=True, fmt='.2f', linewidths=.5, center=0,
    cmap=sns.diverging_palette(220, 20, as_cmap=True), vmin=-1, vmax=1)

plt.savefig("./Lecture_Figures_output/fig9.1_assets_correlation_heatmap_2000.png")  # 그림 저장


# KTB10Y 는 2012.10 부터 사용 가능하므로 여기서 다시 반영
obs_start = pd.to_datetime("1990-01-01", errors='coerce', format='%Y-%m-%d')
obs_end = pd.to_datetime("2021-12-01", errors='coerce', format='%Y-%m-%d')
df_assets_return_obs = df_assets_return[obs_start:obs_end]

list_assets = ["KOSPI", "KTB10Y", "HPI_APT", "S&P500", "TB10Y", "REIT", "GOLD"]
df_assets_return_obs = df_assets_return_obs[list_assets]

# 최근 10년
obs_start1 = pd.to_datetime("2011-01-01", errors='coerce', format='%Y-%m-%d')

fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
sns.heatmap(
    data=df_assets_return_obs[obs_start1:].corr(), annot=True, fmt='.2f', linewidths=.5, center=0,
    cmap=sns.diverging_palette(220, 20, as_cmap=True), vmin=-1, vmax=1)

plt.savefig("./Lecture_Figures_output/fig9.1_assets_correlation_heatmap_2011.png")  # 그림 저장

# 최근 5년
obs_start1 = pd.to_datetime("2016-01-01", errors='coerce', format='%Y-%m-%d')

fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
sns.heatmap(
    data=df_assets_return_obs[obs_start1:].corr(), annot=True, fmt='.2f', linewidths=.5, center=0,
    cmap=sns.diverging_palette(220, 20, as_cmap=True), vmin=-1, vmax=1)

plt.savefig("./Lecture_Figures_output/fig9.1_assets_correlation_heatmap_2016.png")  # 그림 저장

########################################################################################################################
df_portfolio = df_assets[["KOSPI", "TB10Y_KRW", "SNP500_KRW"]]
df_portfolio = df_assets[["KOSPI", "TB10Y_KRW", "SNP500_KRW", "Bitcoin", "GOLD"]]

dt_end = pd.to_datetime("2021-12-01", errors='coerce', format='%Y-%m-%d')

dt_base1 = pd.to_datetime("2000-01-01", errors='coerce', format='%Y-%m-%d')
dt_base2 = pd.to_datetime("2010-01-01", errors='coerce', format='%Y-%m-%d')
dt_base3 = pd.to_datetime("2015-01-01", errors='coerce', format='%Y-%m-%d')

dt_end = pd.to_datetime("2021-12-01", errors='coerce', format='%Y-%m-%d')
dt_base4 = pd.to_datetime("2010-07-01", errors='coerce', format='%Y-%m-%d')

dt_base = dt_base4
df_portfolio = df_portfolio[dt_base:dt_end]
df_portfolio["index_KOSPI"] = df_portfolio["KOSPI"] / (df_portfolio.loc[dt_base]["KOSPI"]) * 100
df_portfolio["index_TB10Y"] = df_portfolio["TB10Y_KRW"] / (df_portfolio.loc[dt_base]["TB10Y_KRW"]) * 100
df_portfolio["portfolio73"] = df_portfolio["index_KOSPI"] * 0.7 + df_portfolio["index_TB10Y"] * 0.3
df_portfolio["portfolio55"] = df_portfolio["index_KOSPI"] * 0.5 + df_portfolio["index_TB10Y"] * 0.5
df_portfolio["portfolio46"] = df_portfolio["index_KOSPI"] * 0.4 + df_portfolio["index_TB10Y"] * 0.6
df_portfolio["portfolio37"] = df_portfolio["index_KOSPI"] * 0.3 + df_portfolio["index_TB10Y"] * 0.7
df_portfolio["index_SNP500"] = df_portfolio["SNP500_KRW"] / (df_portfolio.loc[dt_base]["SNP500_KRW"]) * 100

df_portfolio["index_Bitcoin"] = df_portfolio["Bitcoin"] / (df_portfolio.loc[dt_base]["Bitcoin"]) * 100
df_portfolio["index_GOLD"] = df_portfolio["GOLD"] / (df_portfolio.loc[dt_base]["GOLD"]) * 100

# 그림 9.2 자산배분 포트폴리오 수익률 비교
# 시각화: 월별 시계열 자료 1개를 표시
fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300

colors = sns.color_palette('hls', 6)  # observation 개수만큼 색상 사용
plt.plot(df_portfolio.index, df_portfolio["index_KOSPI"], color=colors[0], label="KOSPI")
plt.plot(df_portfolio.index, df_portfolio["portfolio73"], color=colors[1], label="Portfolio 73")
plt.plot(df_portfolio.index, df_portfolio["portfolio55"], color=colors[2], label="Portfolio 55")
# plt.plot(df_portfolio.index, df_portfolio["portfolio46"], color=colors[5], label="Portfolio 46")
plt.plot(df_portfolio.index, df_portfolio["portfolio37"], color=colors[3], label="Portfolio 37")
plt.plot(df_portfolio.index, df_portfolio["index_TB10Y"], color=colors[4], label="TB10Y")
# plt.plot(df_portfolio.index, df_portfolio["index_SNP500"], color=colors[5], label="SNP500")

plt.plot(df_portfolio.index, df_portfolio["index_Bitcoin"], color=colors[0], label="GOLD")
plt.plot(df_portfolio.index, df_portfolio["index_GOLD"], color=colors[0], label="KOSPI")


xlim_start = dt_base
plt.xlim(xlim_start, )
# plt.ylim(80, 180)
#plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Index (2015.01 = 100)', fontsize=10)
plt.legend(loc='upper left')
plt.show()

plt.savefig("./Lecture_Figures_output/fig9.2_asset_allocation_returns_2015.png")  # 그림 저장


########################################################################################################################
# Markowiz 포트폴리오

# selected_assets = ["KOSPI", "TB10Y"]
selected_assets = ["KOSPI", "IEF"]

df_portfolio = df_assets_return[selected_assets].copy()
dt_start = pd.to_datetime("2004-12-01", errors='coerce', format='%Y-%m-%d')
dt_end = pd.to_datetime("2021-12-01", errors='coerce', format='%Y-%m-%d')
df_portfolio = df_portfolio[dt_start:dt_end]

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

    # Expected return (YoY 수익률 사용했으므로 252일 보정 필요없음)
    ret_arr[x] = np.sum((df_portfolio.mean() * weights * 252 / 252))

    # Expected volatility (YoY 수익률 사용했으므로 252일 보정 필요없음)
    vol_arr[x] = np.sqrt(np.dot(weights.T, np.dot(df_portfolio.cov() * 252 / 252, weights)))

    # Sharpe Ratio
    sharpe_arr[x] = ret_arr[x] / vol_arr[x]

sharpe_arr.max()
all_weights[sharpe_arr.argmax(), :]
max_sr_vol = vol_arr[sharpe_arr.argmax()]
max_sr_ret = ret_arr[sharpe_arr.argmax()]

all_weights[vol_arr.argmin(), :]
min_vol_vol = vol_arr[vol_arr.argmin()]
min_vol_ret = ret_arr[vol_arr.argmin()]
min_vol_vol
min_vol_ret

fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
plt.scatter(vol_arr, ret_arr, c=sharpe_arr, cmap='viridis')
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('Volatility')
plt.ylabel('Return')
plt.xlim(0, )
plt.ylim(0, )
plt.scatter(max_sr_vol, max_sr_ret, c='tab:red', s=50)  # red dot
plt.scatter(min_vol_vol, min_vol_ret, c='tab:blue', s=50)  # red dot
plt.show()

plt.savefig("./Lecture_Figures_output/fig9.5_markowitz_portfolio.png")  # 그림 저장

########################################################################################################################
# df_portfolio = df_assets_return.copy()
# dt_start = pd.to_datetime("2010-01-01", errors='coerce', format='%Y-%m-%d')
# dt_end = pd.to_datetime("2021-12-01", errors='coerce', format='%Y-%m-%d')
# df_portfolio = df_portfolio[dt_start:dt_end]
#
# df_portfolio["portfolio46"] = (df_portfolio["KOSPI"] * 0.4 + df_portfolio["TB10Y"] * 0.6) * 100


selected_assets = ["KOSPI", "IEF"]

df_portfolio = df_assets_return[selected_assets].copy()
dt_start = pd.to_datetime("2004-12-01", errors='coerce', format='%Y-%m-%d')
dt_end = pd.to_datetime("2021-12-01", errors='coerce', format='%Y-%m-%d')
df_portfolio = df_portfolio[dt_start:dt_end]
df_portfolio["portfolio46"] = (df_portfolio["KOSPI"] * 0.4 + df_portfolio["IEF"] * 0.6) * 100


# plt.hist(df_portfolio['portfolio46'], color='tab:blue', edgecolor='black', normed=True, bins=20)

# Density Plot and Histogram of all arrival delays
fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
sns.distplot(df_portfolio['portfolio46'], hist=True, kde=True,
             bins=20, color='darkblue',
             hist_kws={'edgecolor': 'black'},
             kde_kws={'linewidth': 2})

plt.savefig("./Lecture_Figures_output/fig9.6_portfolio46_return_histogram.png")  # 그림 저장



fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
sns.histplot(data=df_portfolio, x="portfolio46", stat="probability",
             # bins=20,
             binwidth=1,
             discrete=False)

plt.savefig("./Lecture_Figures_output/fig9.6_portfolio46_return_histogram.png")  # 그림 저장


tips = sns.load_dataset("tips")
fig, axes = plt.subplots(nrows=2, ncols=1,figsize=(12,6))
axes = axes.flatten()
sns.histplot(data=tips, x="size", stat="probability", discrete=False,ax=axes[0])
sns.histplot(data=tips, x="size", stat="probability", discrete=True,ax=axes[1])


########################################################################################################################















# ########################################################################################################################
# # 미국 ETF 데이터 불러오기
# yahoo_SPY = pd.read_csv('./Market_Watch_Data/yahoo_SPY.csv', header=0, encoding='utf-8', low_memory=False)
# yahoo_IEF = pd.read_csv('./Market_Watch_Data/yahoo_IEF.csv', header=0, encoding='utf-8', low_memory=False)
# yahoo_VNQ = pd.read_csv('./Market_Watch_Data/yahoo_VNQ.csv', header=0, encoding='utf-8', low_memory=False)
# yahoo_HYG = pd.read_csv('./Market_Watch_Data/yahoo_HYG.csv', header=0, encoding='utf-8', low_memory=False)
# yahoo_132030ks = pd.read_csv('./Market_Watch_Data/yahoo_132030.KS.csv', header=0, encoding='utf-8', low_memory=False)
# yahoo_148070ks = pd.read_csv('./Market_Watch_Data/yahoo_148070.KS.csv', header=0, encoding='utf-8', low_memory=False)
#
# yahoo_SPY["spy"] = yahoo_SPY["Close"]
# yahoo_IEF["ief"] = yahoo_IEF["Close"]
# yahoo_VNQ["vnq"] = yahoo_VNQ["Close"]
# yahoo_HYG["hyg"] = yahoo_HYG["Close"]
# yahoo_132030ks["gold"] = yahoo_132030ks["Close"]
# yahoo_148070ks["ktb10y"] = yahoo_148070ks["Close"]
#
# yahoo_SPY["datetime"] = pd.to_datetime(yahoo_SPY["Date"], errors='coerce', format='%Y-%m-%d')
# yahoo_IEF["datetime"] = pd.to_datetime(yahoo_IEF["Date"], errors='coerce', format='%Y-%m-%d')
# yahoo_VNQ["datetime"] = pd.to_datetime(yahoo_VNQ["Date"], errors='coerce', format='%Y-%m-%d')
# yahoo_HYG["datetime"] = pd.to_datetime(yahoo_HYG["Date"], errors='coerce', format='%Y-%m-%d')
# yahoo_132030ks["datetime"] = pd.to_datetime(yahoo_132030ks["Date"], errors='coerce', format='%Y-%m-%d')
# yahoo_148070ks["datetime"] = pd.to_datetime(yahoo_148070ks["Date"], errors='coerce', format='%Y-%m-%d')  # KOSEF 국고채 10년
#
# yahoo_SPY.index = yahoo_SPY["datetime"]
# yahoo_IEF.index = yahoo_IEF["datetime"]
# yahoo_VNQ.index = yahoo_VNQ["datetime"]
# yahoo_HYG.index = yahoo_HYG["datetime"]
# yahoo_132030ks.index = yahoo_132030ks["datetime"]
# yahoo_148070ks.index = yahoo_148070ks["datetime"]
#
# df_kospi_monthly = BOK_802Y001_01.resample('M').last()
# df_spy_monthly = yahoo_SPY.resample('M').last()
# df_ief_monthly = yahoo_IEF.resample('M').last()
# df_vnq_monthly = yahoo_VNQ.resample('M').last()
# df_hyg_monthly = yahoo_HYG.resample('M').last()
# df_gold_monthly = yahoo_132030ks.resample('M').last()
# df_ktb10y_monthly = yahoo_148070ks.resample('M').last()
#
# df_kospi_monthly["DATETIME"] = df_kospi_monthly["DATETIME"].apply(lambda dt: dt.replace(day=1))
# df_spy_monthly["datetime"] = df_spy_monthly["datetime"].apply(lambda dt: dt.replace(day=1))
# df_ief_monthly["datetime"] = df_ief_monthly["datetime"].apply(lambda dt: dt.replace(day=1))
# df_vnq_monthly["datetime"] = df_vnq_monthly["datetime"].apply(lambda dt: dt.replace(day=1))
# df_hyg_monthly["datetime"] = df_hyg_monthly["datetime"].apply(lambda dt: dt.replace(day=1))
# df_gold_monthly["datetime"] = df_gold_monthly["datetime"].apply(lambda dt: dt.replace(day=1))
# df_ktb10y_monthly["datetime"] = df_ktb10y_monthly["datetime"].apply(lambda dt: dt.replace(day=1))
#
# df_kospi_monthly.index = df_kospi_monthly["DATETIME"]
# df_spy_monthly.index = df_spy_monthly["datetime"]
# df_ief_monthly.index = df_ief_monthly["datetime"]
# df_vnq_monthly.index = df_vnq_monthly["datetime"]
# df_hyg_monthly.index = df_hyg_monthly["datetime"]
# df_gold_monthly.index = df_gold_monthly["datetime"]
# df_ktb10y_monthly.index = df_ktb10y_monthly["datetime"]
#
# # 하나로 합친 데이터프레임 만들기
# df_data = BOK_901Y010_00[["DATETIME", "CPI"]]
# df_data = pd.merge(df_data, BOK_901Y062_00[["DATETIME", "HPI"]], left_on='DATETIME', right_on='DATETIME', how='left')
# df_data = pd.merge(df_data, BOK_901Y062_01[["DATETIME", "HPI(APT)"]], left_on='DATETIME', right_on='DATETIME', how='left')
# df_data = pd.merge(df_data, BOK_721Y001_AA[["DATETIME", "CB(AA-)"]], left_on='DATETIME', right_on='DATETIME', how='left')
# df_data = pd.merge(df_data, BOK_731Y004_00[["DATETIME", "USDKRW"]], left_on='DATETIME', right_on='DATETIME', how='left')
# df_data = pd.merge(df_data, df_kospi_monthly[["kospi"]], left_on='DATETIME', right_index=True, how='left')
# df_data = pd.merge(df_data, investpy_snp500_monthly[["snp500"]], left_on='DATETIME', right_index=True, how='left')
# df_data = pd.merge(df_data, df_spy_monthly[["spy"]], left_on='DATETIME', right_index=True, how='left')
# df_data = pd.merge(df_data, df_ief_monthly[["ief"]], left_on='DATETIME', right_index=True, how='left')
# df_data = pd.merge(df_data, df_vnq_monthly[["vnq"]], left_on='DATETIME', right_index=True, how='left')
# df_data = pd.merge(df_data, df_hyg_monthly[["hyg"]], left_on='DATETIME', right_index=True, how='left')
# df_data = pd.merge(df_data, df_gold_monthly[["gold"]], left_on='DATETIME', right_index=True, how='left')
# df_data = pd.merge(df_data, df_ktb10y_monthly[["ktb10y"]], left_on='DATETIME', right_index=True, how='left')
#
# df_data["snp500_krw"] = df_data["snp500"] * df_data["usdkrw"]  # 환율 보정
# df_data["spy_krw"] = df_data["spy"] * df_data["usdkrw"]  # 환율 보정
# df_data["ief_krw"] = df_data["ief"] * df_data["usdkrw"]  # 환율 보정
# df_data["vnq_krw"] = df_data["vnq"] * df_data["usdkrw"]  # 환율 보정
# df_data["hyg_krw"] = df_data["hyg"] * df_data["usdkrw"]  # 환율 보정
#
# n_available = 321  # 2011-11-01
# df_data["index_cpi"] = df_data["cpi"] / (df_data.iloc[n_available, ]["cpi"]) * 100
# df_data["index_apt_hpi"] = df_data["apt_hpi"] / (df_data.iloc[n_available, ]["apt_hpi"]) * 100
# df_data["index_kospi"] = df_data["kospi"] / (df_data.iloc[n_available, ]["kospi"]) * 100
# df_data["index_snp500"] = df_data["snp500_krw"] / (df_data.iloc[n_available, ]["snp500_krw"]) * 100
# df_data["index_spy"] = df_data["spy_krw"] / (df_data.iloc[n_available, ]["spy_krw"]) * 100
# df_data["index_ief"] = df_data["ief_krw"] / (df_data.iloc[n_available, ]["ief_krw"]) * 100
# df_data["index_vnq"] = df_data["vnq_krw"] / (df_data.iloc[n_available, ]["vnq_krw"]) * 100
# df_data["index_hyg"] = df_data["hyg_krw"] / (df_data.iloc[n_available, ]["hyg_krw"]) * 100
# df_data["index_gold"] = df_data["gold"] / (df_data.iloc[n_available, ]["gold"]) * 100
# df_data["index_ktb10y"] = df_data["ktb10y"] / (df_data.iloc[n_available, ]["ktb10y"]) * 100
#
# n_available2 = 321  # 211 부터 적용 가능 (2002-08-01)
# df_data["index_kospi2"] = df_data["kospi"] / (df_data.iloc[n_available2, ]["kospi"]) * 100
# df_data["index_snp5002"] = df_data["snp500_krw"] / (df_data.iloc[n_available2, ]["snp500_krw"]) * 100
#
# df_data["index_portfolio73"] = df_data["index_kospi2"] * 0.7 + df_data["index_snp5002"] * 0.3
# df_data["index_portfolio55"] = df_data["index_kospi2"] * 0.5 + df_data["index_snp5002"] * 0.5
# df_data["index_portfolio37"] = df_data["index_kospi2"] * 0.3 + df_data["index_snp5002"] * 0.7
#
# df_data['KOSPI'] = df_data['index_kospi'].pct_change(1)
# df_data['KTB10Y'] = df_data['index_ktb10y'].pct_change(1)
# df_data['APT'] = df_data['index_apt_hpi'].pct_change(1)
# df_data['S&P500'] = df_data['index_snp500'].pct_change(1)
# df_data['SPY'] = df_data['index_spy'].pct_change(1)
# df_data['IEF'] = df_data['index_ief'].pct_change(1)
# df_data['HYG'] = df_data['index_hyg'].pct_change(1)
# df_data['VNQ'] = df_data['index_vnq'].pct_change(1)
# df_data['GOLD'] = df_data['index_gold'].pct_change(1)
#
# list_assets = ["KOSPI", "KTB10Y", "APT", "SPY", "IEF", "HYG", "VNQ", "GOLD", ]
# dt_start = pd.to_datetime("2011-11-01", errors='coerce', format='%Y-%m-%d')
# dt_end = pd.to_datetime("2022-02-01", errors='coerce', format='%Y-%m-%d')
#
# df_graph = df_data[(df_data["DATETIME"] >= dt_start) & (df_data["DATETIME"] <= dt_end)]
#
# df_graph[list_assets].corr()
#
# ########################################################################################################################
# # 그림 9.1 주요 자산 간 상관관계
# fig = plt.figure()
# fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
# sns.heatmap(
#     data=df_graph[list_assets].corr(), annot=True, fmt='.2f', linewidths=.5, center=0,
#     cmap=sns.diverging_palette(220, 20, as_cmap=True))
#
# plt.savefig("./Lecture_Figures_output/fig9.1_assets_correlation_heatmap.png")  # 그림 저장
#
# ########################################################################################################################
# # 그림 9.2 자산배분 포트폴리오 수익률 비교
# # 시각화: 월별 시계열 자료 1개를 표시
# fig = plt.figure()
# fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
#
# colors = sns.color_palette('hls', 6)  # observation 개수만큼 색상 사용
# plt.plot(df_data["DATETIME"], df_data["index_kospi2"], color=colors[0], label="KOSPI")
# plt.plot(df_data["DATETIME"], df_data["index_portfolio73"], color=colors[1], label="Portfolio 73")
# plt.plot(df_data["DATETIME"], df_data["index_portfolio55"], color=colors[2], label="Portfolio 55")
# plt.plot(df_data["DATETIME"], df_data["index_portfolio37"], color=colors[3], label="Portfolio 37")
# plt.plot(df_data["DATETIME"], df_data["index_ief2"], color=colors[4], label="IEF")
#
# xlim_start = pd.to_datetime("2011-10-01", errors='coerce', format='%Y-%m-%d')
# plt.xlim(xlim_start, )
# plt.ylim(80, 180)
# #plt.axhline(y=0, color='green', linestyle='dotted')
# plt.xlabel('Dates', fontsize=10)
# plt.ylabel('Index (2011.11 = 100)', fontsize=10)
# plt.legend(loc='upper left')
# plt.show()
#
# plt.savefig("./Lecture_Figures_output/fig9.2_asset_allocation_returns.png")  # 그림 저장
