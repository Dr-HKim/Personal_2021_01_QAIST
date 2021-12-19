# Created by Kim Hyeongjun on 03/22/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.
# 데이터가이드 일간 데이터 엑셀을 불러와서 Pickle 형태로 저장
# 전체 약 5시간 소요

import pandas as pd
from datetime import datetime

########################################################################################################################
# 데이터가이드 분기별 재무제표 불러오기
# 파일: DG_FS_2020_2021.xlsx
# Sheet: GeneralInfo, IFRSN, GAAPC, GAAPN
# A8: 빈칸, F8: NFS-IFRS(C)
# A9: 빈칸, F9: 6000901001
# A10: 빈칸, F10: 총자산(천원)
# A11: Symbol, B11: Name, C11: 결산월, D11: 회계년, E11: 주기, F11 부터 빈칸
# A12 부터 데이터 시작
# A114851: 데이터 끝 (WG114851)

# StopWatch: 코드 시작
time_start = datetime.now()
print("Procedure started at: " + str(time_start))

dg_GeneralHistoric_Annual_2000_2021_data = pd.read_excel(
    './DataGuide/DG_GeneralHistoric_Annual_2000_2021.xlsx', header=None, skiprows=11, skipfooter=0)
dg_GeneralHistoric_Annual_2000_2021_data.to_pickle('./DataGuide_processed/dg_GeneralHistoric_Annual_2000_2021_data.pkl')

dg_GeneralHistoric_Annual_2000_2021_header = pd.read_excel(
    './DataGuide/DG_GeneralHistoric_Annual_2000_2021.xlsx', header=None, skiprows=7, nrows=4)
dg_GeneralHistoric_Annual_2000_2021_header.to_pickle('./DataGuide_processed/dg_GeneralHistoric_Annual_2000_2021_header.pkl')

# StopWatch
time_end_GeneralInfo_2000_2021 = datetime.now()
print("Load GeneralInfo Annual 2000_2021 finished at: " + str(time_end_GeneralInfo_2000_2021))
print("Elapsed (in GeneralInfo Annual 2000_2021): " + str(time_end_GeneralInfo_2000_2021 - time_start))

dg_GeneralHistoric_2020_2021_data = pd.read_excel(
    './DataGuide/DG_GeneralHistoric_2020_2021.xlsx', header=None, skiprows=11, skipfooter=0)
dg_GeneralHistoric_2020_2021_data.to_pickle('./DataGuide_processed/dg_GeneralHistoric_Quarterly_2020_2021_data.pkl')

dg_GeneralHistoric_2020_2021_header = pd.read_excel(
    './DataGuide/DG_GeneralHistoric_2020_2021.xlsx', header=None, skiprows=7, nrows=4)
dg_GeneralHistoric_2020_2021_header.to_pickle('./DataGuide_processed/dg_GeneralHistoric_Quarterly_2020_2021_header.pkl')

# StopWatch
time_end_GeneralInfo_2020_2021 = datetime.now()
print("Load GeneralInfo_2013_2019 finished at: " + str(time_end_GeneralInfo_2020_2021))
print("Elapsed (in GeneralInfo_2013_2019): " + str(time_end_GeneralInfo_2020_2021 - time_start))

dg_GeneralHistoric_2013_2019_data = pd.read_excel(
    './DataGuide/DG_GeneralHistoric_2013_2019.xlsx', header=None, skiprows=11, skipfooter=0)
dg_GeneralHistoric_2013_2019_data.to_pickle('./DataGuide_processed/dg_GeneralHistoric_Quarterly_2013_2019_data.pkl')

dg_GeneralHistoric_2013_2019_header = pd.read_excel(
    './DataGuide/DG_GeneralHistoric_2013_2019.xlsx', header=None, skiprows=7, nrows=4)
dg_GeneralHistoric_2013_2019_header.to_pickle('./DataGuide_processed/dg_GeneralHistoric_Quarterly_2013_2019_header.pkl')

# StopWatch
time_end_GeneralInfo_2013_2019 = datetime.now()
print("Load GeneralInfo_2013_2019 finished at: " + str(time_end_GeneralInfo_2013_2019))
print("Elapsed (in GeneralInfo_2013_2019): " + str(time_end_GeneralInfo_2013_2019 - time_start))

dg_GeneralHistoric_2009_2012_data = pd.read_excel(
    './DataGuide/DG_GeneralHistoric_1997_2012.xlsx', sheet_name="Sheet1", header=None, skiprows=11, skipfooter=0)
dg_GeneralHistoric_2009_2012_data.to_pickle('./DataGuide_processed/dg_GeneralHistoric_Quarterly_2009_2012_data.pkl')

dg_GeneralHistoric_2009_2012_header = pd.read_excel(
    './DataGuide/DG_GeneralHistoric_1997_2012.xlsx', sheet_name="Sheet1", header=None, skiprows=7, nrows=4)
dg_GeneralHistoric_2009_2012_header.to_pickle('./DataGuide_processed/dg_GeneralHistoric_Quarterly_2009_2012_header.pkl')

# StopWatch
time_end_GeneralInfo_2009_2012 = datetime.now()
print("Load GeneralInfo_2009_2012 finished at: " + str(time_end_GeneralInfo_2009_2012))
print("Elapsed (in GeneralInfo_2009_2012): " + str(time_end_GeneralInfo_2009_2012 - time_start))

dg_GeneralHistoric_2005_2008_data = pd.read_excel(
    './DataGuide/DG_GeneralHistoric_1997_2012.xlsx', sheet_name="Sheet2", header=None, skiprows=11, skipfooter=0)
dg_GeneralHistoric_2005_2008_data.to_pickle('./DataGuide_processed/dg_GeneralHistoric_Quarterly_2005_2008_data.pkl')

dg_GeneralHistoric_2005_2008_header = pd.read_excel(
    './DataGuide/DG_GeneralHistoric_1997_2012.xlsx', sheet_name="Sheet2", header=None, skiprows=7, nrows=4)
dg_GeneralHistoric_2005_2008_header.to_pickle('./DataGuide_processed/dg_GeneralHistoric_Quarterly_2005_2008_header.pkl')

# StopWatch
time_end_GeneralInfo_2005_2008 = datetime.now()
print("Load GeneralInfo_2005_2008 finished at: " + str(time_end_GeneralInfo_2005_2008))
print("Elapsed (in GeneralInfo_2005_2008): " + str(time_end_GeneralInfo_2005_2008 - time_start))

dg_GeneralHistoric_2001_2004_data = pd.read_excel(
    './DataGuide/DG_GeneralHistoric_1997_2012.xlsx', sheet_name="Sheet3", header=None, skiprows=11, skipfooter=0)
dg_GeneralHistoric_2001_2004_data.to_pickle('./DataGuide_processed/dg_GeneralHistoric_Quarterly_2001_2004_data.pkl')

dg_GeneralHistoric_2001_2004_header = pd.read_excel(
    './DataGuide/DG_GeneralHistoric_1997_2012.xlsx', sheet_name="Sheet3", header=None, skiprows=7, nrows=4)
dg_GeneralHistoric_2001_2004_header.to_pickle('./DataGuide_processed/dg_GeneralHistoric_Quarterly_2001_2004_header.pkl')

# StopWatch
time_end_GeneralInfo_2001_2004 = datetime.now()
print("Load GeneralInfo_2001_2004 finished at: " + str(time_end_GeneralInfo_2001_2004))
print("Elapsed (in GeneralInfo_2001_2004): " + str(time_end_GeneralInfo_2001_2004 - time_start))

dg_GeneralHistoric_1997_2000_data = pd.read_excel(
    './DataGuide/DG_GeneralHistoric_1997_2012.xlsx', sheet_name="Sheet4", header=None, skiprows=11, skipfooter=0)
dg_GeneralHistoric_1997_2000_data.to_pickle('./DataGuide_processed/dg_GeneralHistoric_Quarterly_1997_2000_data.pkl')

dg_GeneralHistoric_1997_2000_header = pd.read_excel(
    './DataGuide/DG_GeneralHistoric_1997_2012.xlsx', sheet_name="Sheet4", header=None, skiprows=7, nrows=4)
dg_GeneralHistoric_1997_2000_header.to_pickle('./DataGuide_processed/dg_GeneralHistoric_Quarterly_1997_2000_header.pkl')

# StopWatch
time_end_GeneralInfo_1997_2000 = datetime.now()
print("Load GeneralInfo_1997_2000 finished at: " + str(time_end_GeneralInfo_1997_2000))
print("Elapsed (in GeneralInfo_1997_2000): " + str(time_end_GeneralInfo_1997_2000 - time_start))

