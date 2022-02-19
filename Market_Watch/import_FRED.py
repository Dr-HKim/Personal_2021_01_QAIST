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

########################################################################################################################
# 기준금리
# Federal Funds Target Range - Upper Limit (DFEDTARU)
fred_DFEDTARU = fred.get_series('DFEDTARU')
fred_DFEDTARU.to_pickle('./Market_Watch_Data/fred_DFEDTARU.pkl')

# Federal Funds Target Range - Lower Limit (DFEDTARL)
fred_DFEDTARL = fred.get_series('DFEDTARL')
fred_DFEDTARL.to_pickle('./Market_Watch_Data/fred_DFEDTARL.pkl')

# Federal Funds Effective Rate Monthly (FEDFUNDS)
fred_FEDFUNDS = fred.get_series('FEDFUNDS')
fred_FEDFUNDS.to_pickle('./Market_Watch_Data/fred_FEDFUNDS.pkl')

# Federal Funds Effective Rate Daily (DFF)
fred_DFF = fred.get_series('DFF')
fred_DFF.to_pickle('./Market_Watch_Data/fred_DFF.pkl')

# 달러 인덱스
# Nominal Broad U.S. Dollar Index (DTWEXBGS)
# Units: Index Jan 2006=100, Not Seasonally Adjusted
fred_DTWEXBGS = fred.get_series('DTWEXBGS')
fred_DTWEXBGS.to_pickle('./Market_Watch_Data/fred_DTWEXBGS.pkl')

# 채권 인덱스
# ICE BofA 7-10 Year US Corporate Index Total Return Index Value (BAMLCC4A0710YTRIV)
# Units: Index, Not Seasonally Adjusted
fred_BAMLCC4A0710YTRIV = fred.get_series('BAMLCC4A0710YTRIV')
fred_BAMLCC4A0710YTRIV.to_pickle('./Market_Watch_Data/fred_BAMLCC4A0710YTRIV.pkl')

# 부동산 인덱스 (배당 재투자)
# Wilshire US Real Estate Investment Trust Total Market Index (Wilshire US REIT) (WILLREITIND)
# Units: Index, Not Seasonally Adjusted
fred_WILLREITIND = fred.get_series('WILLREITIND')
fred_WILLREITIND.to_pickle('./Market_Watch_Data/fred_WILLREITIND.pkl')

# 부동산 인덱스 (배당 재투자 안함)
# Wilshire US Real Estate Investment Trust Price Index (Wilshire US REIT) (WILLREITPR)
# Units: Index, Not Seasonally Adjusted
fred_WILLREITPR = fred.get_series('WILLREITPR')
fred_WILLREITPR.to_pickle('./Market_Watch_Data/fred_WILLREITPR.pkl')


########################################################################################################################
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

# BB 등급 회사채 가산금리
# ICE BofA BB US High Yield Index Option-Adjusted Spread (BAMLH0A1HYBB)
# Units: Percent, Not Seasonally Adjusted
fred_BAMLH0A1HYBB = fred.get_series('BAMLH0A1HYBB')
fred_BAMLH0A1HYBB.to_pickle('./Market_Watch_Data/fred_BAMLH0A1HYBB.pkl')


########################################################################################################################
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



