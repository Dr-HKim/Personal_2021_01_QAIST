# 8강 환율

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
# 그림 8.1 코스피 지수와 환율
# 8.8.2.1 평균환율, 기말환율 > 주요국통화의 대원화 환율 통계자료 [036Y004][HY,MM,QQ,YY] (1964.05 부터)
BOK_036Y004 = pd.read_pickle('./Market_Watch_Data/BOK_036Y004.pkl')
BOK_036Y004_00 = BOK_036Y004[(BOK_036Y004["ITEM_CODE1"] == "0000001") & (BOK_036Y004["ITEM_CODE2"] == "0000200")].copy()  # 원달러환율 말일자료

# 6.1.1 증권/재정 - 주식거래 및 주가지수 - 주식시장(일별) [064Y001] (1995.01.03 부터)
BOK_064Y001 = pd.read_pickle('./Market_Watch_Data/BOK_064Y001.pkl')
BOK_064Y001_01 = BOK_064Y001[BOK_064Y001["ITEM_CODE1"] == "0001000"]  # KOSPI지수
BOK_064Y001_01.index = BOK_064Y001_01["DATETIME"]

df_kospi_monthly = BOK_064Y001_01.resample('M').last()

# 그림 8.1 코스피 지수와 환율
# 시각화: 월별 시계열 자료 2개를 서로 다른 y 축으로 표시하고 0 위치 통일
fig, ax1 = plt.subplots()
xlim_start = pd.to_datetime("2000-01-01", errors='coerce', format='%Y-%m-%d')

# 첫번째 시계열
color1 = "tab:blue"
ax1.set_xlabel("Dates")
ax1.set_ylabel("KOSPI", color=color1)  # 데이터 레이블
ax1.plot(df_kospi_monthly.index, df_kospi_monthly["DATA_VALUE"], color=color1)
# ax1.plot(BOK_064Y001_01["DATETIME"], BOK_064Y001_01["DATA_VALUE"], color=color1, linestyle='-')
ax1.tick_params(axis="y")

# 두번째 시계열
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color2 = "tab:red"
ax2.set_ylabel("USD/KRW", color=color2)  # 데이터 레이블
ax2.plot(BOK_036Y004_00["DATETIME"], BOK_036Y004_00["DATA_VALUE"], color=color2, linestyle='-')
ax2.tick_params(axis='y')

# 그래프 기타 설정
fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
# ax1.set_ylim([-50, 50])
ax2.set_ylim([800, 1800])
# align_yaxis(ax1, 0, ax2, 0)  # 두 축이 동일한 0 값을 가지도록 조정
# plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlim(xlim_start, )
plt.show()

# 그림 저장
plt.savefig("./Lecture_Figures_output/fig8.1_kospi_and_usd_krw.png")  # 그림 저장

########################################################################################################################
# 그림 8.2 코스피 지수와 코스피 기업이익
# 6.1.2 증권/재정 - 주식거래 및 주가지수 [028Y015][MM, YY] (200002, 1976 부터)
BOK_028Y015_MM = pd.read_pickle('./Market_Watch_Data/BOK_028Y015_MM.pkl')
kospi_n_shares = BOK_028Y015_MM[BOK_028Y015_MM["ITEM_NAME1"] == "KOSPI_상장주식수"].copy()
kospi_mkt_cap = BOK_028Y015_MM[BOK_028Y015_MM["ITEM_NAME1"] == "KOSPI_시가총액"].copy()
kospi_per = BOK_028Y015_MM[BOK_028Y015_MM["ITEM_NAME1"] == "KOSPI_주가이익비율 3)"].copy()
kospi_close = BOK_028Y015_MM[BOK_028Y015_MM["ITEM_NAME1"] == "KOSPI_종가"].copy()

kospi_n_shares.rename(columns={"DATA_VALUE": "n_shares"}, inplace=True)
kospi_mkt_cap.rename(columns={"DATA_VALUE": "mkt_cap"}, inplace=True)
kospi_per.rename(columns={"DATA_VALUE": "per"}, inplace=True)
kospi_close.rename(columns={"DATA_VALUE": "close"}, inplace=True)

kospi = pd.merge(kospi_n_shares[["DATETIME", "n_shares"]], kospi_mkt_cap[["DATETIME", "mkt_cap"]], left_on='DATETIME', right_on='DATETIME', how='left')
kospi = pd.merge(kospi, kospi_per[["DATETIME", "per"]], left_on='DATETIME', right_on='DATETIME', how='left')
kospi = pd.merge(kospi, kospi_close[["DATETIME", "close"]], left_on='DATETIME', right_on='DATETIME', how='left')

kospi["earnings"] = kospi["close"] / kospi["per"]
kospi["eps"] = kospi["earnings"] / kospi["n_shares"]

# 그림 8.2 코스피 지수와 코스피 기업이익
# 시각화: 월별 시계열 자료 2개를 서로 다른 y 축으로 표시하고 0 위치 통일
fig, ax1 = plt.subplots()
xlim_start = pd.to_datetime("2000-01-01", errors='coerce', format='%Y-%m-%d')

# 첫번째 시계열
color1 = "tab:blue"
ax1.set_xlabel("Dates")
ax1.set_ylabel("KOSPI", color=color1)  # 데이터 레이블
ax1.plot(df_kospi_monthly.index, df_kospi_monthly["DATA_VALUE"], color=color1)
# ax1.plot(BOK_064Y001_01["DATETIME"], BOK_064Y001_01["DATA_VALUE"], color=color1, linestyle='-')
ax1.tick_params(axis="y")

# 두번째 시계열
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color2 = "tab:red"
ax2.set_ylabel("KOSPI Earnings", color=color2)  # 데이터 레이블
ax2.plot(kospi["DATETIME"], kospi["earnings"], color=color2, linestyle='-')
ax2.tick_params(axis='y')

# 그래프 기타 설정
fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
# ax1.set_ylim([-50, 50])
# ax2.set_ylim([800, 1800])
# align_yaxis(ax1, 0, ax2, 0)  # 두 축이 동일한 0 값을 가지도록 조정
# plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlim(xlim_start, )
plt.show()

# 그림 저장
plt.savefig("./Lecture_Figures_output/fig8.2_kospi_and_kospi_earnings.png")  # 그림 저장

########################################################################################################################
# 그림 8.4 달러/원 환율과 국제유가
# 8.8.2.1 평균환율, 기말환율 > 주요국통화의 대원화 환율 통계자료 [036Y004][HY,MM,QQ,YY] (1964.05 부터)
BOK_036Y004 = pd.read_pickle('./Market_Watch_Data/BOK_036Y004.pkl')
BOK_036Y004_00 = BOK_036Y004[(BOK_036Y004["ITEM_CODE1"] == "0000001") & (BOK_036Y004["ITEM_CODE2"] == "0000200")].copy()  # 원달러환율 말일자료

# 국제유가 WTI (Monthly)
# Spot Crude Oil Price: West Texas Intermediate (WTI) (WTISPLC)
# Units: Dollars per Barrel, Not Seasonally Adjusted
fred_WTISPLC = pd.read_pickle('./Market_Watch_Data/fred_WTISPLC.pkl')

# 그림 8.4 달러/원 환율과 국제유가
# 시각화: 월별 시계열 자료 2개를 서로 다른 y 축으로 표시하고 0 위치 통일
fig, ax1 = plt.subplots()
xlim_start = pd.to_datetime("2000-01-01", errors='coerce', format='%Y-%m-%d')

# 첫번째 시계열
color1 = "tab:blue"
ax1.set_xlabel("Dates")
ax1.set_ylabel("WTI (Dollars per Barrel)", color=color1)  # 데이터 레이블
ax1.plot(fred_WTISPLC.index, fred_WTISPLC, color=color1)
# ax1.plot(BOK_064Y001_01["DATETIME"], BOK_064Y001_01["DATA_VALUE"], color=color1, linestyle='-')
ax1.tick_params(axis="y")

# 두번째 시계열
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color2 = "tab:red"
ax2.set_ylabel("USD/KRW", color=color2)  # 데이터 레이블
ax2.plot(BOK_036Y004_00["DATETIME"], BOK_036Y004_00["DATA_VALUE"], color=color2, linestyle='-')
ax2.tick_params(axis='y')

# 그래프 기타 설정
fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
# ax1.set_ylim([-50, 50])
ax2.set_ylim([800, 1800])
# align_yaxis(ax1, 0, ax2, 0)  # 두 축이 동일한 0 값을 가지도록 조정
# plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlim(xlim_start, )
plt.show()

# 그림 저장
plt.savefig("./Lecture_Figures_output/fig8.4_wti_and_usd_krw.png")  # 그림 저장


########################################################################################################################
# 그림 8.5 OECD 경기선행지수와 국제유가

# OECD 경기선행지수 (OECD Composite Leading Indicator)
OECD_MONTHLY = pd.read_pickle('./Market_Watch_Data/oecd_monthly.pkl')

# LOLITOTR_GYSA: 12-month rate of change of the trend restored CLI
df_oecd_cli = OECD_MONTHLY[(OECD_MONTHLY["location_id"] == "OECD") & (OECD_MONTHLY["subject_id"] == "LOLITOTR_GYSA")].copy()
df_oecd_cli["datetime"] = df_oecd_cli["datetime"].apply(lambda dt: dt.replace(day=1))

# 국제유가 WTI (Monthly)
# Spot Crude Oil Price: West Texas Intermediate (WTI) (WTISPLC)
# Units: Dollars per Barrel, Not Seasonally Adjusted
fred_WTISPLC = pd.read_pickle('./Market_Watch_Data/fred_WTISPLC.pkl')
fred_WTISPLC_pct_change = fred_WTISPLC.pct_change(periods=12) * 100

# 그림 8.5 OECD 경기선행지수와 국제유가
# 시각화: 월별 시계열 자료 2개를 서로 다른 y 축으로 표시하고 0 위치 통일
fig, ax1 = plt.subplots()
xlim_start = pd.to_datetime("2000-01-01", errors='coerce', format='%Y-%m-%d')

# 첫번째 시계열
color1 = "tab:blue"
ax1.set_xlabel("Dates")
ax1.set_ylabel("WTI (%, YoY)", color=color1)  # 데이터 레이블
ax1.plot(fred_WTISPLC_pct_change.index, fred_WTISPLC_pct_change, color=color1)
# ax1.plot(BOK_064Y001_01["DATETIME"], BOK_064Y001_01["DATA_VALUE"], color=color1, linestyle='-')
ax1.tick_params(axis="y")

# 두번째 시계열
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color2 = "tab:red"
ax2.set_ylabel("OECD Composite Leading Indicator (%, YoY)", color=color2)  # 데이터 레이블
ax2.plot(df_oecd_cli["datetime"], df_oecd_cli["datavalue"], color=color2, linestyle='-')
ax2.tick_params(axis='y')

# 그래프 기타 설정
fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
ax1.set_ylim([-150, 300])
# ax2.set_ylim([800, 1800])
align_yaxis(ax1, 0, ax2, 0)  # 두 축이 동일한 0 값을 가지도록 조정
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlim(xlim_start, )
plt.show()

# 그림 저장
plt.savefig("./Lecture_Figures_output/fig8.5_oecd_cli_and_wti.png")  # 그림 저장

