# Created by Kim Hyeongjun on 03/22/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.

import pandas as pd

########################################################################################################################
# 데이터가이드 일간 데이터 불러오기
# 파일: DG_DAILY_20000101_20201231.xlsx
# 날짜: 2000-01-01 ~ 2020-12-31
# Sheet DG_DAILY1: 기준가(원), 시가(원), 고가(원), 저가(원), 종가(원)
# Sheet DG_DAILY2: 수정시가(원), 수정고가(원), 수정저가(원), 수정주가(원), 수정계수
# Sheet DG_DAILY3: 거래량(주), 거래대금(원), 상장주식수(주), 상장예정주식수(주), 외국인보유주식수(티커)(주)
# 자료: B:WOM
# A9: Symbol (A000010)
# A10: Symbol Name (조흥은행)
# A11: Kind (SSC)
# A12: Item (S410000200)
# A13: Item Name (기준가(원))
# A14: Frequency (DAILY)
# A15: 날짜 시작 (2000-01-04)
# A5198: 날짜 종료 (2020-12-30)

DG_DAILY_20000101_20201231 = pd.read_excel('./data_raw/DG_DAILY_20000101_20201231.xlsx', sheet_name=1, header=3,
                                  skipfooter=0, usecols="B:GE")






# 각 월별 ID 만들기
df_KB_sales_index['MONTH_ID'] = df_KB_sales_index.index

# datetime 형식으로 날짜 붙이기
df_KB_sales_index["Date0"] = pd.to_datetime("19860101", errors='coerce', format='%Y%m%d')
df_KB_sales_index["Date_y"] = df_KB_sales_index["Date0"].dt.year + divmod(df_KB_sales_index['MONTH_ID'], 12)[0]
df_KB_sales_index["Date_m"] = df_KB_sales_index["Date0"].dt.month + divmod(df_KB_sales_index['MONTH_ID'], 12)[1]
df_KB_sales_index["Date_d"] = df_KB_sales_index["Date0"].dt.day
df_KB_sales_index["Date"] = pd.to_datetime(
    df_KB_sales_index["Date_y"] * 10000 + df_KB_sales_index["Date_m"] * 100 + df_KB_sales_index["Date_d"],
    format='%Y%m%d')
df_KB_sales_index = df_KB_sales_index.drop(["Date0", "Date_y", "Date_m", "Date_d"], axis=1)

# 주택매매가격 종합지수 시계열 그래프 그리기
plt.plot(df_KB_sales_index["Date"], df_KB_sales_index["Total"], color='g')
plt.plot(df_KB_sales_index["Date"], df_KB_sales_index["Seoul"], color='orange')
plt.xlabel('Month')
plt.ylabel('Housing Index')
plt.show()
