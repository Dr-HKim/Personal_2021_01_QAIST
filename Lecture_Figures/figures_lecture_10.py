
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
# 비트코인
investpy_bitcoin = pd.read_pickle('./Market_Watch_Data/investpy_bitcoin.pkl')
sr_bitcoin = investpy_bitcoin["Close"]

# 이더리움
investpy_Ethereum = pd.read_pickle('./Market_Watch_Data/investpy_Ethereum.pkl')
sr_Ethereum = investpy_Ethereum["Close"]

# 리플
investpy_Ripple = pd.read_pickle('./Market_Watch_Data/investpy_Ripple.pkl')
sr_Ripple = investpy_Ripple["Close"]

# 금 (달러)
# Gold Futures (ZGJ2)
investpy_Gold = pd.read_pickle('./Market_Watch_Data/investpy_Gold.pkl')
sr_GOLD = investpy_Gold["Close"]

# 달러 인덱스
fred_DTWEXBGS = pd.read_pickle('./Market_Watch_Data/fred_DTWEXBGS.pkl')
sr_Dollar = fred_DTWEXBGS.copy()

# 미국 10년만기 국고채
fred_DGS10 = pd.read_pickle('./Market_Watch_Data/fred_DGS10.pkl')
sr_TB10Y = fred_DGS10.copy()

# 미국 2년만기 국고채
fred_DGS2 = pd.read_pickle('./Market_Watch_Data/fred_DGS2.pkl')
sr_TB2Y = fred_DGS2.copy()

# 미국 주식
# 미국 S&P 500 지수 (1979.12.26 부터)
investpy_snp500 = pd.read_pickle('./Market_Watch_Data/investpy_snp500.pkl')
sr_SNP500 = investpy_snp500["Close"]

# 한국 주식
# KOSPI (1981.05.01 부터)
investpy_kospi = pd.read_pickle('./Market_Watch_Data/investpy_kospi.pkl')
sr_KOSPI = investpy_kospi["Close"]

########################################################################################################################
# 자산 데이터 합치기
df_assets = pd.DataFrame({'Bitcoin': sr_bitcoin.values})
df_assets.index = sr_bitcoin.index
df_assets = df_assets.merge(sr_Ethereum.rename('Ethereum'), left_index=True, right_index=True, how='outer')
df_assets = df_assets.merge(sr_Ripple.rename('Ripple'), left_index=True, right_index=True, how='outer')
df_assets = df_assets.merge(sr_GOLD.rename('GOLD'), left_index=True, right_index=True, how='outer')
df_assets = df_assets.merge(sr_Dollar.rename('Dollar'), left_index=True, right_index=True, how='outer')
df_assets = df_assets.merge(sr_TB10Y.rename('TB10Y'), left_index=True, right_index=True, how='outer')
df_assets = df_assets.merge(sr_TB2Y.rename('TB2Y'), left_index=True, right_index=True, how='outer')
df_assets = df_assets.merge(sr_SNP500.rename('SNP500'), left_index=True, right_index=True, how='outer')
df_assets = df_assets.merge(sr_KOSPI.rename('KOSPI'), left_index=True, right_index=True, how='outer')

df_assets = df_assets.fillna(method='ffill')


# 월별 수익률
n_return = 252
df_assets_return = df_assets[["Bitcoin"]].copy()
df_assets_return['Bitcoin'] = df_assets['Bitcoin'].pct_change(n_return, fill_method=None)
df_assets_return['Ethereum'] = df_assets['Ethereum'].pct_change(n_return, fill_method=None)
df_assets_return['Ripple'] = df_assets['Ripple'].pct_change(n_return, fill_method=None)
df_assets_return['GOLD'] = df_assets['GOLD'].pct_change(n_return, fill_method=None)
df_assets_return['Dollar'] = df_assets['Dollar'].pct_change(n_return, fill_method=None)
df_assets_return['TB10Y'] = df_assets['TB10Y'] / 100
df_assets_return['TB2Y'] = df_assets['TB2Y'] / 100
df_assets_return['SNP500'] = df_assets['SNP500'].pct_change(n_return, fill_method=None)
df_assets_return['KOSPI'] = df_assets['KOSPI'].pct_change(n_return, fill_method=None)



########################################################################################################################
# Asset Correlation Heatmap (1990년 이후 전체 기간)
# KOSPI 1981.06 부터, HPI_APT 1986.01 부터, KTB10Y_yield 는 2000.11 부터, KTB10Y 는 2012.10 부터
obs_start = pd.to_datetime("2017-03-11", errors='coerce', format='%Y-%m-%d')
obs_end = pd.to_datetime("2021-12-31", errors='coerce', format='%Y-%m-%d')

obs_start = pd.to_datetime("2020-10-01", errors='coerce', format='%Y-%m-%d')
obs_end = pd.to_datetime("2021-10-30", errors='coerce', format='%Y-%m-%d')
df_assets_return_obs = df_assets_return[obs_start:obs_end]

# list_assets = ["KOSPI", "KTB10Y", "HPI_APT", "S&P500", "TB10Y", "REIT", "GOLD"]
# df_assets_return_obs = df_assets_return_obs[list_assets]
# df_assets_return_obs["KTB10Y"] = np.nan

fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
sns.heatmap(
    data=df_assets_return_obs.corr(), annot=True, fmt='.2f', linewidths=.5, center=0,
    cmap=sns.diverging_palette(220, 20, as_cmap=True), vmin=-1, vmax=1)

plt.savefig("./Lecture_Figures_output/tmp3.png")  # 그림 저장
