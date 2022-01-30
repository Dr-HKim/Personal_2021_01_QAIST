# Created by Kim Hyeongjun on 12/19/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.

import math
import pandas as pd
import numpy as np
from datetime import datetime


def get_yyyymm_add_months(n_yyyymm, n_months):
    n_yyyy, n_mm = divmod(n_yyyymm, 100)
    n_months_y, n_months_m = divmod(n_mm + n_months - 1, 12)
    output_yyyy = n_yyyy + n_months_y
    output_mm = n_months_m + 1
    output_yyyymm = output_yyyy*100 + output_mm
    return output_yyyymm


def get_kb_data(kb_data_value, kb_data_header, start_yyyymm=198601):
    # 헤더 다루기
    kb_data_header_tr = kb_data_header.transpose()
    kb_data_header_tr[0] = kb_data_header_tr[0].replace('\n', ' ', regex=True)  # 특수문자 제거
    kb_data_header_tr[0] = kb_data_header_tr[0].replace('/ ', '/', regex=True)  # "제주/ 서귀포" 를 "제주/서귀포"
    kb_data_header_tr[0] = kb_data_header_tr[0].fillna(method='ffill')  # 비어있는 지역 LOCF로 채우기
    kb_data_header_tr[1] = kb_data_header_tr[1].fillna("전체")
    kb_data_header_tr["name"] = kb_data_header_tr[0] + "_" + kb_data_header_tr[1]  # 헤더 생성

    # 데이터에 헤더를 Column Index 로 설정
    kb_data = kb_data_value.copy()
    kb_data = kb_data.apply(lambda col: pd.to_numeric(col, errors='coerce'))
    kb_data.columns = kb_data_header_tr["name"]  # Column Index 설정

    # 데이터가 없는 자료 제외 (마지막에 데이터가 아닌 텍스트 자료 있음)
    cond_no_data = ~kb_data['구분_전체'].isna()
    kb_data = kb_data[cond_no_data].copy()

    # 날짜 구조가 이상하게 되어있으므로 수정
    kb_data["YYYYMM0"] = start_yyyymm  # 시작시점
    kb_data["n_of_months"] = range(0, len(kb_data))  # 0 부터 1 씩 증가하는 숫자 입력
    kb_data["YYYYMM"] = get_yyyymm_add_months(kb_data["YYYYMM0"], kb_data["n_of_months"])
    kb_data.pop("YYYYMM0")
    kb_data.pop("n_of_months")
    kb_data["YYYYMMDD"] = kb_data["YYYYMM"] * 100 + 1

    # 첫번째 변수 이름을 날짜로 변경하고 날짜 입력
    kb_data.rename(columns={"구분_전체": "날짜"}, inplace=True)  # 변수명 변경
    kb_data["날짜"] = pd.to_datetime(kb_data['YYYYMMDD'].astype(str), errors='coerce', format='%Y%m%d')

    return kb_data


def get_kb_jeonse_to_purchase_data(kb_data_value, kb_data_header, start_yyyymm=198601):
    # 헤더 다루기
    kb_data_header_tr = kb_data_header.transpose()
    kb_data_header_tr[0] = kb_data_header_tr[0].replace('\n', ' ', regex=True)  # 특수문자 제거
    kb_data_header_tr[0] = kb_data_header_tr[0].replace('/ ', '/', regex=True)  # "제주/ 서귀포" 를 "제주/서귀포"
    kb_data_header_tr["name"] = kb_data_header_tr[0]  # 헤더 생성
    kb_data_header_tr["name"][0] = "날짜"

    # 데이터에 헤더를 Column Index 로 설정
    kb_data = kb_data_value.copy()
    kb_data.columns = kb_data_header_tr["name"]  # Column Index 설정

    # 데이터가 없는 자료 제외 (마지막에 데이터가 아닌 텍스트 자료 있음)
    cond_no_data = ~kb_data['날짜'].isna()
    kb_data = kb_data[cond_no_data].copy()
    kb_data = kb_data.apply(lambda col: pd.to_numeric(col, errors='coerce'))  # object 타입을 float64 로 변경

    # 날짜 구조가 이상하게 되어있으므로 수정
    kb_data["YYYYMM0"] = start_yyyymm  # 시작시점
    kb_data["n_of_months"] = range(0, len(kb_data))  # 0 부터 1 씩 증가하는 숫자 입력
    kb_data["YYYYMM"] = get_yyyymm_add_months(kb_data["YYYYMM0"], kb_data["n_of_months"])
    kb_data.pop("YYYYMM0")
    kb_data.pop("n_of_months")
    kb_data["YYYYMMDD"] = kb_data["YYYYMM"] * 100 + 1

    # 날짜를 datetime 형태로 입력
    kb_data["날짜"] = pd.to_datetime(kb_data['YYYYMMDD'].astype(str), errors='coerce', format='%Y%m%d')

    return kb_data


file_location = './KB_Land/KB부동산_월간_202111.xlsx'

########################################################################################################################
# StopWatch: 코드 시작
time_start = datetime.now()
print("Procedure started at: " + str(time_start))

########################################################################################################################
# 01.매매종합
kb_data01_value = pd.read_excel(file_location, sheet_name=4, header=None, skiprows=4, skipfooter=0)
kb_data01_header = pd.read_excel(file_location, sheet_name=4, header=None, skiprows=1, nrows=3)
kb_data01 = get_kb_data(kb_data01_value, kb_data01_header)
kb_data01["부산_강서구"] = np.nan  # 부산 강서구는 자료가 숨김처리 되어있고 모든 지수가 0 이므로 자료를 지운다
kb_data01.to_pickle('./KB_Land_processed/kb_data01.pkl')  # 자료 저장

# 02.매매APT
kb_data02_value = pd.read_excel(file_location, sheet_name=5, header=None, skiprows=4, skipfooter=0)
kb_data02_header = pd.read_excel(file_location, sheet_name=5, header=None, skiprows=1, nrows=3)
kb_data02 = get_kb_data(kb_data02_value, kb_data02_header)
kb_data02.to_pickle('./KB_Land_processed/kb_data02.pkl')  # 자료 저장

# 03.매매단독
kb_data03_value = pd.read_excel(file_location, sheet_name=6, header=None, skiprows=4, skipfooter=0)
kb_data03_header = pd.read_excel(file_location, sheet_name=6, header=None, skiprows=1, nrows=3)
kb_data03 = get_kb_data(kb_data03_value, kb_data03_header)
kb_data03.to_pickle('./KB_Land_processed/kb_data03.pkl')  # 자료 저장

# 04.매매연립
kb_data04_value = pd.read_excel(file_location, sheet_name=7, header=None, skiprows=4, skipfooter=0)
kb_data04_header = pd.read_excel(file_location, sheet_name=7, header=None, skiprows=1, nrows=3)
kb_data04 = get_kb_data(kb_data04_value, kb_data04_header)
kb_data04.to_pickle('./KB_Land_processed/kb_data04.pkl')  # 자료 저장

# 05.전세종합
kb_data05_value = pd.read_excel(file_location, sheet_name=8, header=None, skiprows=4, skipfooter=0)
kb_data05_header = pd.read_excel(file_location, sheet_name=8, header=None, skiprows=1, nrows=3)
kb_data05 = get_kb_data(kb_data05_value, kb_data05_header)
kb_data05.to_pickle('./KB_Land_processed/kb_data05.pkl')  # 자료 저장

# 06.전세APT
kb_data06_value = pd.read_excel(file_location, sheet_name=9, header=None, skiprows=4, skipfooter=0)
kb_data06_header = pd.read_excel(file_location, sheet_name=9, header=None, skiprows=1, nrows=3)
kb_data06 = get_kb_data(kb_data06_value, kb_data06_header)
kb_data06.to_pickle('./KB_Land_processed/kb_data06.pkl')  # 자료 저장

# 07.전세단독
kb_data07_value = pd.read_excel(file_location, sheet_name=10, header=None, skiprows=4, skipfooter=0)
kb_data07_header = pd.read_excel(file_location, sheet_name=10, header=None, skiprows=1, nrows=3)
kb_data07 = get_kb_data(kb_data07_value, kb_data07_header)
kb_data07.to_pickle('./KB_Land_processed/kb_data07.pkl')  # 자료 저장

# 08.전세연립
kb_data08_value = pd.read_excel(file_location, sheet_name=11, header=None, skiprows=4, skipfooter=0)
kb_data08_header = pd.read_excel(file_location, sheet_name=11, header=None, skiprows=1, nrows=3)
kb_data08 = get_kb_data(kb_data08_value, kb_data08_header)
kb_data08.to_pickle('./KB_Land_processed/kb_data08.pkl')  # 자료 저장

########################################################################################################################
# 27.종합매매전세비
kb_data27_value = pd.read_excel(file_location, sheet_name=25, header=None, skiprows=3, skipfooter=0)
kb_data27_header = pd.read_excel(file_location, sheet_name=25, header=None, skiprows=1, nrows=2)
kb_data27 = get_kb_jeonse_to_purchase_data(kb_data27_value, kb_data27_header, start_yyyymm=201106)
kb_data27.to_pickle('./KB_Land_processed/kb_data27.pkl')  # 자료 저장

# 28.아파트매매전세비
kb_data28_value = pd.read_excel(file_location, sheet_name=26, header=None, skiprows=3, skipfooter=0)
kb_data28_header = pd.read_excel(file_location, sheet_name=26, header=None, skiprows=1, nrows=2)
kb_data28 = get_kb_jeonse_to_purchase_data(kb_data28_value, kb_data28_header, start_yyyymm=199812)
kb_data28.to_pickle('./KB_Land_processed/kb_data28.pkl')  # 자료 저장

# 29.단독매매전세비
kb_data29_value = pd.read_excel(file_location, sheet_name=27, header=None, skiprows=3, skipfooter=0)
kb_data29_header = pd.read_excel(file_location, sheet_name=27, header=None, skiprows=1, nrows=2)
kb_data29 = get_kb_jeonse_to_purchase_data(kb_data29_value, kb_data29_header, start_yyyymm=201106)
kb_data29.to_pickle('./KB_Land_processed/kb_data29.pkl')  # 자료 저장

# 30.연립매매전세비
kb_data30_value = pd.read_excel(file_location, sheet_name=28, header=None, skiprows=3, skipfooter=0)
kb_data30_header = pd.read_excel(file_location, sheet_name=28, header=None, skiprows=1, nrows=2)
kb_data30 = get_kb_jeonse_to_purchase_data(kb_data30_value, kb_data30_header, start_yyyymm=201106)
kb_data30.to_pickle('./KB_Land_processed/kb_data30.pkl')  # 자료 저장

########################################################################################################################
# kb_data_header = kb_data27_header.copy()
# kb_data_value = kb_data27_value.copy()
# start_yyyymm = 201106
#
# # 헤더 다루기
# kb_data_header_tr = kb_data_header.transpose()
# kb_data_header_tr[0] = kb_data_header_tr[0].replace('\n', ' ', regex=True)  # 특수문자 제거
# kb_data_header_tr[0] = kb_data_header_tr[0].replace('/ ', '/', regex=True)  # "제주/ 서귀포" 를 "제주/서귀포"
# kb_data_header_tr["name"] = kb_data_header_tr[0] # 헤더 생성
# kb_data_header_tr["name"][0] = "날짜"
#
# # 데이터에 헤더를 Column Index 로 설정
# kb_data = kb_data_value.copy()
# kb_data.columns = kb_data_header_tr["name"]  # Column Index 설정
#
# # 데이터가 없는 자료 제외 (마지막에 데이터가 아닌 텍스트 자료 있음)
# cond_no_data = ~kb_data['날짜'].isna()
# kb_data = kb_data[cond_no_data].copy()
# kb_data = kb_data.apply(lambda col: pd.to_numeric(col, errors='coerce'))  # object 타입을 float64 로 변경
#
# # 날짜 구조가 이상하게 되어있으므로 수정
# kb_data["YYYYMM0"] = start_yyyymm  # 시작시점
# kb_data["n_of_months"] = range(0, len(kb_data))  # 0 부터 1 씩 증가하는 숫자 입력
# kb_data["YYYYMM"] = get_yyyymm_add_months(kb_data["YYYYMM0"], kb_data["n_of_months"])
# kb_data.pop("YYYYMM0")
# kb_data.pop("n_of_months")
# kb_data["YYYYMMDD"] = kb_data["YYYYMM"] * 100 + 1
#
# # 날짜를 datetime 형태로 입력
# kb_data["날짜"] = pd.to_datetime(kb_data['YYYYMMDD'].astype(str), errors='coerce', format='%Y%m%d')
#

