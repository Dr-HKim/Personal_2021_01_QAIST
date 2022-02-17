# https://junyoru.tistory.com/122 참고
# FRED 에 가입하여 api key 를 받아야 한다
# https://fred.stlouisfed.org/ > My Account > API Keys > Request API Key
# fredapi 패키지 설치 (https://github.com/mortada/fredapi)
# 터미널/프롬프트: pip install fredapi
# 아나콘다: conda install fredapi
# colab: !pip install fredapi

from fredapi import Fred
from data_raw.def_authentication import *

# API Key 설정
fred_api_key = get_fred_auth_key()
fred = Fred(api_key=fred_api_key)

# 10년 만기 국고채
# Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity (DGS10)
# https://fred.stlouisfed.org/series/DGS10
fred_DGS10 = fred.get_series('DGS10')
fred_DGS10.to_pickle('./Market_Watch_Data/fred_DGS10.pkl')

# 2년 만기 국고채
# Market Yield on U.S. Treasury Securities at 2-Year Constant Maturity (DGS2)
# https://fred.stlouisfed.org/series/DGS2
fred_DGS2 = fred.get_series('DGS2')
fred_DGS2.to_pickle('./Market_Watch_Data/fred_DGS2.pkl')

# 3개월 만기 국고채
# Market Yield on U.S. Treasury Securities at 3-Month Constant Maturity (DGS3MO)
# https://fred.stlouisfed.org/series/DGS3MO
fred_DGS3MO = fred.get_series('DGS3MO')
fred_DGS3MO.to_pickle('./Market_Watch_Data/fred_DGS3MO.pkl')

# S&P 500 (SP500)
# https://fred.stlouisfed.org/series/SP500
fred_SP500 = fred.get_series('SP500')
fred_SP500.to_pickle('./Market_Watch_Data/fred_SP500.pkl')

# 미국 매출액 대비 재고비율 (Monthly, End of Period)
# Total Business: Inventories to Sales Ratio (ISRATIO)
fred_ISRATIO = fred.get_series('ISRATIO')
fred_ISRATIO.to_pickle('./Market_Watch_Data/fred_ISRATIO.pkl')

# 미국 실질 가계 소비 지출 (Monthly)
# Real Personal Consumption Expenditures (PCEC96)
# Units: Billions of Chained 2012 Dollars, Seasonally Adjusted Annual Rate
fred_PCEC96 = fred.get_series('PCEC96')
fred_PCEC96.to_pickle('./Market_Watch_Data/fred_PCEC96.pkl')

# 미국 실질 가계 소비 지출 (GDP, Quarterly)
# Real Personal Consumption Expenditures (DPCERO1Q156NBEA)
# Units: Percent Change from Quarter One Year Ago, Seasonally Adjusted
fred_DPCERO1Q156NBEA = fred.get_series('DPCERO1Q156NBEA')
fred_DPCERO1Q156NBEA.to_pickle('./Market_Watch_Data/fred_DPCERO1Q156NBEA.pkl')

# 미국 산업 생산
# Industrial Production: Total Index (INDPRO)
# Units: Index 2017=100, Seasonally Adjusted
fred_INDPRO = fred.get_series('INDPRO')
fred_INDPRO.to_pickle('./Market_Watch_Data/fred_INDPRO.pkl')

# 한국 수출 통계
# Exports: Value Goods for the Republic of Korea (XTEXVA01KRM667S)
# Units: US Dollars Monthly Level, Seasonally Adjusted
fred_XTEXVA01KRM667S = fred.get_series('XTEXVA01KRM667S')
fred_XTEXVA01KRM667S.to_pickle('./Market_Watch_Data/fred_XTEXVA01KRM667S.pkl')


# 유가 WTI (Monthly)
# Spot Crude Oil Price: West Texas Intermediate (WTI) (WTISPLC)
# Units: Dollars per Barrel, Not Seasonally Adjusted
fred_WTISPLC = fred.get_series('WTISPLC')
fred_WTISPLC.to_pickle('./Market_Watch_Data/fred_WTISPLC.pkl')



