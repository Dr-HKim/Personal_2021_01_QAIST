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

dg_data = pd.read_excel(
    './data_raw/DG_DAILY_20210101_test.xlsx', sheet_name="DG_DAILY1", header=None, skiprows=14, skipfooter=0)

dg_header = pd.read_excel(
    './data_raw/DG_DAILY_20210101_test.xlsx', sheet_name="DG_DAILY1", header=None, skiprows=8, nrows=6)

