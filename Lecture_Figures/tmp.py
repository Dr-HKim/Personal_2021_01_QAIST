
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
