# Created by Kim Hyeongjun on 03/22/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.
# 데이터가이드 일간 데이터 엑셀을 불러와서 Pickle 형태로 저장
# 전체 약 5시간 소요

import pandas as pd
from datetime import datetime

########################################################################################################################
# 데이터가이드 분기별 재무제표 불러오기
# 파일: DG_FS_20200519_1981_1989.xlsx
# Sheet1
# A8: 빈칸, F8: NFS-IFRS(C)
# A9: 빈칸, F9: 6000901001
# A10: 빈칸, F10: 총자산(천원)
# A11: Symbol, B11: Name, C11: 결산월, D11: 회계년, E11: 주기, F11 부터 빈칸
# A12 부터 데이터 시작
# A114851: 데이터 끝 (WG114851)

# StopWatch: 코드 시작
time_start = datetime.now()
print("Procedure started at: " + str(time_start))

# 각 1시간 41분씩 총 5시간 소요
dg_fs_20200519_1981_1989_data = pd.read_excel(
    './data_raw/DG_FS_20200519_1981_1989.xlsx', header=None, skiprows=11, skipfooter=0)
dg_fs_20200519_1981_1989_data.to_pickle('./data_processed/dg_fs_20200519_1981_1989_data.pkl')

dg_fs_20200519_1981_1989_header = pd.read_excel(
    './data_raw/DG_FS_20200519_1981_1989.xlsx', header=None, skiprows=7, nrows=4)
dg_fs_20200519_1981_1989_header.to_pickle('./data_processed/dg_fs_20200519_1981_1989_header.pkl')

# StopWatch
time_end_1981_1989 = datetime.now()
print("Load 1981_1989 finished at: " + str(time_end_1981_1989))
print("Elapsed (in 1981_1989): " + str(time_end_1981_1989 - time_start))

dg_fs_20200519_1990_1999_data = pd.read_excel(
    './data_raw/DG_FS_20200519_1990_1999.xlsx', header=None, skiprows=11, skipfooter=0)
dg_fs_20200519_1990_1999_data.to_pickle('./data_processed/dg_fs_20200519_1990_1999_data.pkl')

dg_fs_20200519_1990_1999_header = pd.read_excel(
    './data_raw/DG_FS_20200519_1990_1999.xlsx', header=None, skiprows=7, nrows=4)
dg_fs_20200519_1990_1999_header.to_pickle('./data_processed/dg_fs_20200519_1990_1999_header.pkl')

# StopWatch
time_end_1990_1999 = datetime.now()
print("Load 1990_1999 finished at: " + str(time_end_1990_1999))
print("Elapsed (in 1990_1999): " + str(time_end_1990_1999 - time_end_1981_1989))

dg_fs_20200519_2000_2015_data = pd.read_excel(
    './data_raw/DG_FS_20200519_2000_2015.xlsx', header=None, skiprows=11, skipfooter=0)
dg_fs_20200519_2000_2015_data.to_pickle('./data_processed/dg_fs_20200519_2000_2015_data.pkl')

dg_fs_20200519_2000_2015_header = pd.read_excel(
    './data_raw/DG_FS_20200519_2000_2015.xlsx', header=None, skiprows=7, nrows=4)
dg_fs_20200519_2000_2015_header.to_pickle('./data_processed/dg_fs_20200519_2000_2015_header.pkl')

# StopWatch
time_end_2000_2015 = datetime.now()
print("Load 2000_2015 finished at: " + str(time_end_2000_2015))
print("Elapsed (in 2000_2015): " + str(time_end_2000_2015 - time_end_1990_1999))

dg_fs_20200519_2016_2020_data = pd.read_excel(
    './data_raw/DG_FS_20200519_2016_2020.xlsx', header=None, skiprows=11, skipfooter=0)
dg_fs_20200519_2016_2020_data.to_pickle('./data_processed/dg_fs_20200519_2016_2020_data.pkl')

dg_fs_20200519_2016_2020_header = pd.read_excel(
    './data_raw/DG_FS_20200519_2016_2020.xlsx', header=None, skiprows=7, nrows=4)
dg_fs_20200519_2016_2020_header.to_pickle('./data_processed/dg_fs_20200519_2016_2020_header.pkl')

# StopWatch
time_end_2016_2020 = datetime.now()
print("Load 2016_2020 finished at: " + str(time_end_2016_2020))
print("Elapsed (in 2016_2020): " + str(time_end_2016_2020 - time_end_2000_2015))
print("Elapsed (in total): " + str(time_end_2016_2020 - time_start))

