# Created by Kim Hyeongjun on 01/19/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.
# https://ecos.bok.or.kr/jsp/openapi/OpenApiController.jsp
# ecos.bok.or.kr 접속 (E-mail: yuii7890@naver.com)
# 개발 가이드 > 통계코드검색

import datetime
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from data_raw.def_authentication import *
import statsmodels.api as sm  # HP Filtering


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



# 코스피 200 지수
df_kospi_200 = pd.read_pickle('./US_raw/df_kospi_200.pkl')
df_kospi_200_monthly = df_kospi_200.shift(-1).resample('M').last()

# 코덱스 200 (069500) 가격
df_069500 = pd.read_pickle('./US_raw/df_069500.pkl')
df_069500_monthly = df_069500.shift(-1).resample('M').last()

# 삼성전자 (005930) 가격
df_005930 = pd.read_pickle('./US_raw/df_005930.pkl')
df_005930_monthly = df_005930.shift(-1).resample('M').last()



# 시각화: 월별 시계열 자료 3개를 같은 y 축으로 표시
fig = plt.figure()
# fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
fig.set_size_inches(1800/300, 1200/300)  # 그래프 크기 지정, DPI=300

plt.plot(df_kospi_200_monthly.index, df_kospi_200_monthly.Close, color='g', label="KOSPI 200")

xlim_start = pd.to_datetime("2013-01-01", errors='coerce', format='%Y-%m-%d')
plt.xlim(xlim_start, )
plt.ylim(200, 500)
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('point', fontsize=10)
plt.legend(loc='upper left')
plt.show()

plt.savefig("./BOK_processed/fig1.1_KOSPI_200_Index.png")


# 시각화: 월별 시계열 자료 3개를 같은 y 축으로 표시
fig = plt.figure()
# fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
fig.set_size_inches(1800/300, 1200/300)  # 그래프 크기 지정, DPI=300

plt.plot(df_069500_monthly.index, df_069500_monthly.Close, color='g', label="KODEX 200 ETF")

xlim_start = pd.to_datetime("2013-01-01", errors='coerce', format='%Y-%m-%d')
plt.xlim(xlim_start, )
plt.ylim(20000, 50000)
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('KRW', fontsize=10)
plt.legend(loc='upper left')
plt.show()

plt.savefig("./BOK_processed/fig1.2_KODEX_200_ETF.png")





# 그림 1.1 코스피 200 지수와 코덱스 200 ETF 가격
# 시각화: 월별 시계열 자료 2개를 서로 다른 y 축으로 표시하고 0 위치 통일
fig, ax1 = plt.subplots()
xlim_start = pd.to_datetime("2000-01-01", errors='coerce', format='%Y-%m-%d')

# 첫번째 시계열
color1 = "tab:red"
ax1.set_xlabel("Dates")
ax1.set_ylabel("KODEX 200 ETF", color=color1)  # 데이터 레이블
ax1.plot(df_069500_monthly.index, df_069500_monthly.Close, color=color1)
ax1.tick_params(axis="y")

# 두번째 시계열
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color2 = "tab:blue"
ax2.set_ylabel("SAMSUNG ELECTRONICS", color=color2)  # 데이터 레이블
ax2.plot(df_005930_monthly.index, df_005930_monthly.Close, color=color2, linestyle='-')
ax2.tick_params(axis='y')

# 그래프 기타 설정
fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
ax1.set_ylim([20000, 50000])
ax2.set_ylim([30000, 100000])
# align_yaxis(ax1, 0, ax2, 0)  # 두 축이 동일한 0 값을 가지도록 조정
# plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlim(xlim_start, )
plt.show()

plt.savefig("./BOK_processed/fig4.8_current_account_and_kospi.png")  # 그림 저장

