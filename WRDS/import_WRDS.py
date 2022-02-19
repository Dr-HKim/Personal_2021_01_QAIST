import pandas as pd

# B30, B20, B10: 30, 20, 10년 만기 국채
# T90, T30: 90일, 30일 만기 국채
# CPI: 소비자물가지수
# 자료는 대략 1942.01 부터
wrds_index_treasury = pd.read_csv('./WRDS_raw/wrds_index_treasury.csv', header=0, encoding='utf-8', low_memory=False)
wrds_index_treasury["datetime"] = pd.to_datetime(wrds_index_treasury["caldt"], errors='coerce', format='%Y%m%d')
wrds_index_treasury.index = wrds_index_treasury["datetime"]
wrds_index_treasury_monthly = wrds_index_treasury.resample('M').last()  # 월말 자료만
wrds_index_treasury_monthly.index = wrds_index_treasury_monthly.index.map(lambda t: t.replace(day=1))  # 인덱스 날짜를 1일로
wrds_index_treasury_monthly = wrds_index_treasury_monthly[wrds_index_treasury_monthly["caldt"] > 19420000]
sr_TB10Y = wrds_index_treasury_monthly["b10ind"]
