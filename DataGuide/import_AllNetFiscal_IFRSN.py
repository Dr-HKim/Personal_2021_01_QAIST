# Created by Kim Hyeongjun on 03/22/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.
# 데이터가이드 재무제표 엑셀을 불러와서 Pickle 형태로 저장
# IFRSN_2020_2021 약 12분 소요
# 전체 약 1시간 소요

import pandas as pd
from datetime import datetime

########################################################################################################################
# 데이터가이드 분기별 재무제표 불러오기
# 파일: DG_AllNetFiscal_2020_2021.xlsx
# Sheet: IFRSC, IFRSN, GAAPC, GAAPN
# A8: 빈칸, F8: NFS-IFRS(C)
# A9: 빈칸, F9: 6000901001
# A10: 빈칸, F10: 총자산(천원)
# A11: Symbol, B11: Name, C11: 결산월, D11: 회계년, E11: 주기, F11 부터 빈칸
# A12 부터 데이터 시작
# A114851: 데이터 끝 (WG114851)

########################################################################################################################
# StopWatch: 코드 시작
time_start = datetime.now()
print("Procedure started at: " + str(time_start))

dg_fs_IFRSN_2020_2021_data = pd.read_excel(
    './DataGuide/DG_AllNetFiscal_2020_2021.xlsx', sheet_name="IFRSN", header=None, skiprows=11, skipfooter=0)
dg_fs_IFRSN_2020_2021_data.to_pickle('./DataGuide_processed/dg_fs_IFRSN_2020_2021_data.pkl')

dg_fs_IFRSN_2020_2021_header = pd.read_excel(
    './DataGuide/DG_AllNetFiscal_2020_2021.xlsx', sheet_name="IFRSN", header=None, skiprows=7, nrows=4)
dg_fs_IFRSN_2020_2021_header.to_pickle('./DataGuide_processed/dg_fs_IFRSN_2020_2021_header.pkl')

# StopWatch
time_end_IFRSN_2020_2021 = datetime.now()
print("Load IFRSN_2020_2021 finished at: " + str(time_end_IFRSN_2020_2021))
print("Elapsed (in IFRSN_2020_2021): " + str(time_end_IFRSN_2020_2021 - time_start))


dg_fs_IFRSN_2010_2019_data = pd.read_excel(
    './DataGuide/DG_AllNetFiscal_2010_2019.xlsx', sheet_name="IFRSN", header=None, skiprows=11, skipfooter=0)
dg_fs_IFRSN_2010_2019_data.to_pickle('./DataGuide_processed/dg_fs_IFRSN_2010_2019_data.pkl')

dg_fs_IFRSN_2010_2019_header = pd.read_excel(
    './DataGuide/DG_AllNetFiscal_2010_2019.xlsx', sheet_name="IFRSN", header=None, skiprows=7, nrows=4)
dg_fs_IFRSN_2010_2019_header.to_pickle('./DataGuide_processed/dg_fs_IFRSN_2010_2019_header.pkl')

# StopWatch
time_end_IFRSN_2010_2019 = datetime.now()
print("Load IFRSN_2010_2019 finished at: " + str(time_end_IFRSN_2010_2019))
print("Elapsed (in IFRSN_2010_2019): " + str(time_end_IFRSN_2010_2019 - time_end_IFRSN_2020_2021))

dg_fs_IFRSN_2000_2009_data = pd.read_excel(
    './DataGuide/DG_AllNetFiscal_2000_2009.xlsx', sheet_name="IFRSN", header=None, skiprows=11, skipfooter=0)
dg_fs_IFRSN_2000_2009_data.to_pickle('./DataGuide_processed/dg_fs_IFRSN_2000_2009_data.pkl')

dg_fs_IFRSN_2000_2009_header = pd.read_excel(
    './DataGuide/DG_AllNetFiscal_2000_2009.xlsx', sheet_name="IFRSN", header=None, skiprows=7, nrows=4)
dg_fs_IFRSN_2000_2009_header.to_pickle('./DataGuide_processed/dg_fs_IFRSN_2000_2009_header.pkl')

# StopWatch
time_end_IFRSN_2000_2009 = datetime.now()
print("Load IFRSN_2000_2009 finished at: " + str(time_end_IFRSN_2000_2009))
print("Elapsed (in IFRSN_2000_2009): " + str(time_end_IFRSN_2000_2009 - time_end_IFRSN_2010_2019))


