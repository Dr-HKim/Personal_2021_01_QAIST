# 7강 미국 소비시장

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


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


# 데이터: https://databank.worldbank.org/source/world-development-indicators#
# Import XLSX File
df_worldbank = pd.read_excel(
    './Market_Watch_Data/Data_Extract_From_World_Development_Indicators.xlsx', sheet_name="Data", header=0, skiprows=0, skipfooter=5)

# 변수 이름 변경 ( 현재 "1960 [YR1960]" 으로 되어있는 것을 심플하게 "1960" 으로 변경
list_year = list(range(1960, 2021))
list_year = list(map(str, list_year))

new_names = ['Country Name', 'Country Code', 'Series Name', 'Series Code']
new_names.extend(list_year)  # 리스트 이어붙이기

df_worldbank.columns = new_names

# 문자열로 저장된 변수를 숫자로 변경하고 다시 저장
df_worldbank_data = df_worldbank[list_year].copy()
df_worldbank_data = df_worldbank_data.apply(lambda col: pd.to_numeric(col, errors='coerce'))
df_worldbank[list_year] = df_worldbank_data.copy()

# 항목별로 데이터 나누기
df_worldbank_household_consumption = df_worldbank[df_worldbank["Series Code"] == "NE.CON.PRVT.CD"].copy()
df_worldbank_final_consumption = df_worldbank[df_worldbank["Series Code"] == "NE.CON.TOTL.CD"].copy()
df_worldbank_household_consumption_p_gdp = df_worldbank[df_worldbank["Series Code"] == "NE.CON.PRVT.ZS"].copy()
df_worldbank_final_consumption_p_gdp = df_worldbank[df_worldbank["Series Code"] == "NE.CON.TOTL.ZS"].copy()


df_worldbank_household_consumption = df_worldbank_household_consumption.sort_values(by=['2020'], ascending=False)
df_worldbank_final_consumption = df_worldbank_final_consumption.sort_values(by=['2020'], ascending=False)


# 주요 변수 중 결측치가 없는 자료만 선택
cond_no_nan = (~np.isnan(df_worldbank_final_consumption["2020"]))
df_pie_chart_raw = df_worldbank_final_consumption[cond_no_nan].copy()
df_pie_chart_raw['rank_2020'] = df_pie_chart_raw['2020'].rank(method='min', ascending=False)  # 랭킹

# 랭킹 기준으로 10위 이내와 그 외 구분
df_pie_chart1 = df_pie_chart_raw[df_pie_chart_raw["rank_2020"] <= 11][["Country Name", "2010", "2020"]].copy()
df_pie_chart2 = df_pie_chart_raw[df_pie_chart_raw["rank_2020"] > 11][["Country Name", "2010", "2020"]].copy()

df_pie_chart = df_pie_chart1.append({'Country Name': 'Other Countries', '2010': df_pie_chart2["2010"].sum(), '2020': df_pie_chart2["2020"].sum()}, ignore_index=True)

g7_countries = ["United States", "Japan", "Germany", "United Kingdom", "France", "Italy", "Canada"]
df_pie_chart_g7 = df_pie_chart[df_pie_chart["Country Name"].isin(g7_countries)]
df_pie_chart_g7["2020"].sum() / df_pie_chart["2020"].sum()
df_pie_chart_g7["2010"].sum() / df_pie_chart["2010"].sum()



fig = plt.figure(figsize=(10, 10))  # 캔버스 생성
fig.set_facecolor('white')  # 캔버스 배경색을 하얀색으로 설정
ax = fig.add_subplot()  # 프레임 생성

colors = sns.color_palette('hls', len(df_pie_chart))  # observation 개수만큼 색상 사용

pie = ax.pie(df_pie_chart['2020'],  # 파이차트 출력
             startangle=90,  # 시작점을 90도(degree)로 지정
             counterclock=False,  # 시계 방향으로 그린다.
             autopct=lambda p: '{:.2f}%'.format(p),  # 퍼센티지 출력
             # wedgeprops=dict(width=0.5),  # 중간의 반지름 0.5만큼 구멍을 뚫어준다.
             colors=colors  # 색상 지정
             )

plt.legend(pie[0], df_pie_chart["Country Name"])  # 범례 표시
plt.show()

plt.savefig("./Lecture_Figures_output/fig7.1_global_consumption_market.png")


########################################################################################################################
selected_countries = ["United States", "Japan", "Germany", "United Kingdom", "France", "Italy", "Canada", "China", "India", "Korea, Rep."]
df_selected = df_worldbank_household_consumption_p_gdp[df_worldbank_household_consumption_p_gdp["Country Name"].isin(selected_countries)]
df_selected = df_selected.sort_values(by=['2020'], ascending=False)

# 시각화: 국가별 소비를 GDP 퍼센트로 나타낸 값을 Bar Chart 로 표시
fig = plt.figure()
fig.set_size_inches(1800/300, 1200/300)  # 그래프 크기 지정, DPI=300

index = np.arange(len(selected_countries))
colors = sns.color_palette('hls', len(selected_countries))  # observation 개수만큼 색상 사용

plt.bar(index, df_selected["2020"], color=colors)
plt.xticks(index, df_selected["Country Name"], rotation='vertical')
plt.gcf().subplots_adjust(bottom=0.35)  # xlabel 이 잘리는 경우가 있어서 아래 마진 설정
plt.ylim(30, 70)
plt.ylabel('% of GDP', fontsize=10)

plt.show()
plt.savefig("./Lecture_Figures_output/fig7.2_consumption_as_percent_of_gdp.png")


########################################################################################################################
# 미국 실질 가계 소비 지출 (Monthly)
# Real Personal Consumption Expenditures (PCEC96)
# Units: Billions of Chained 2012 Dollars, Seasonally Adjusted Annual Rate
fred_PCEC96 = pd.read_pickle('./Market_Watch_Data/fred_PCEC96.pkl')
fred_PCEC96_pct_change = fred_PCEC96.pct_change(periods=12) * 100

# 미국 산업 생산
# Industrial Production: Total Index (INDPRO)
# Units: Index 2017=100, Seasonally Adjusted
fred_INDPRO = pd.read_pickle('./Market_Watch_Data/fred_INDPRO.pkl')
fred_INDPRO_pct_change = fred_INDPRO.pct_change(periods=12) * 100

# 한국 수출 통계
# Exports: Value Goods for the Republic of Korea (XTEXVA01KRM667S)
# Units: US Dollars Monthly Level, Seasonally Adjusted
fred_XTEXVA01KRM667S = pd.read_pickle('./Market_Watch_Data/fred_XTEXVA01KRM667S.pkl')
fred_XTEXVA01KRM667S_pct_change = fred_XTEXVA01KRM667S.pct_change(periods=12) * 100

# 그림 7.3 미국 가계의 소비지출과 산업생산 증가율 추이
# 시각화: 월별 시계열 자료 3개를 같은 y 축으로 표시
fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
# fig.set_size_inches(1800/300, 1200/300)  # 그래프 크기 지정, DPI=300

plt.plot(fred_PCEC96_pct_change.index, fred_PCEC96_pct_change, color='b', label="Real Personal Consumption Expenditures")
plt.plot(fred_INDPRO_pct_change.index, fred_INDPRO_pct_change, color='r', label="Industrial Production")

xlim_start = pd.to_datetime("2000-01-01", errors='coerce', format='%Y-%m-%d')
xlim_end = pd.to_datetime("2023-01-01", errors='coerce', format='%Y-%m-%d')

plt.xlim(xlim_start, )
plt.ylim(-20, 30)
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Percent Change from Year Ago (%)', fontsize=10)
plt.legend(loc='upper left')
plt.show()

plt.savefig("./Lecture_Figures_output/fig7.3_personal_consumption_expenditure_and_industrial_production.png")


# 그림 7.4 미국 산업생산과 한국 수출 증가율 추이
# 시각화: 월별 시계열 자료 3개를 같은 y 축으로 표시
fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
# fig.set_size_inches(1800/300, 1200/300)  # 그래프 크기 지정, DPI=300

plt.plot(fred_INDPRO_pct_change.index, fred_INDPRO_pct_change, color='r', label="Industrial Production")
plt.plot(fred_XTEXVA01KRM667S_pct_change.index, fred_XTEXVA01KRM667S_pct_change, color='g', label="Exports (Korea)")

xlim_start = pd.to_datetime("2000-01-01", errors='coerce', format='%Y-%m-%d')
xlim_end = pd.to_datetime("2023-01-01", errors='coerce', format='%Y-%m-%d')

plt.xlim(xlim_start, )
plt.ylim(-40, 50)
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Percent Change from Year Ago (%)', fontsize=10)
plt.legend(loc='lower right')
plt.show()

plt.savefig("./Lecture_Figures_output/fig7.4_industrial_production_and_Korea_exports.png")
########################################################################################################################
# 그림 7.5 OECD 경기선행지수와 미국 실질가계소비

# OECD 경기선행지수 (OECD Composite Leading Indicator)
OECD_MONTHLY = pd.read_pickle('./Market_Watch_Data/oecd_monthly.pkl')

# LOLITOTR_GYSA: 12-month rate of change of the trend restored CLI
df_oecd_cli = OECD_MONTHLY[(OECD_MONTHLY["location_id"] == "OECD") & (OECD_MONTHLY["subject_id"] == "LOLITOTR_GYSA")].copy()
df_oecd_cli["datetime"] = df_oecd_cli["datetime"].apply(lambda dt: dt.replace(day=1))

# df_oecd_cli["L12_MXEF_Close"] = df_oecd_cli["MXEF_Close"].shift(3)  # lag 3 months

# 미국 실질 가계 소비 지출 (Monthly)
# Real Personal Consumption Expenditures (PCEC96)
# Units: Billions of Chained 2012 Dollars, Seasonally Adjusted Annual Rate
fred_PCEC96 = pd.read_pickle('./Market_Watch_Data/fred_PCEC96.pkl')
fred_PCEC96_pct_change = fred_PCEC96.pct_change(periods=12) * 100


# 그림 7.5 OECD 경기선행지수와 미국 실질가계소비
# 시각화: 월별 시계열 자료 3개를 같은 y 축으로 표시
fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
# fig.set_size_inches(1800/300, 1200/300)  # 그래프 크기 지정, DPI=300

plt.plot(df_oecd_cli.datetime, df_oecd_cli.datavalue, color='r', label="OECD Composite Leading Indicator")
plt.plot(fred_PCEC96_pct_change.index, fred_PCEC96_pct_change, color='g', label="Real Personal Consumption Expenditures")

xlim_start = pd.to_datetime("2000-01-01", errors='coerce', format='%Y-%m-%d')
xlim_end = pd.to_datetime("2023-01-01", errors='coerce', format='%Y-%m-%d')

plt.xlim(xlim_start, )
plt.ylim(-20, 30)
plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Percent Change from Year Ago (%)', fontsize=10)
plt.legend(loc='lower right')
plt.show()

plt.savefig("./Lecture_Figures_output/fig7.5_oecd_cli_and_personal_consumption_expenditures.png")

########################################################################################################################
# 그림 7.6 ISM 신규주문지수와 미국 실질가계소비

# ISM 신규주문지수
investpy_economic_calendar = pd.read_pickle('./Market_Watch_Data/investpy_economic_calendar_us_20000101_20220215.pkl')

investpy_new_orders = investpy_economic_calendar[investpy_economic_calendar['event'].str.contains("ISM Manufacturing New Orders")].copy()
investpy_new_orders["datetime_announced"] = pd.to_datetime(investpy_new_orders["date"], errors='coerce', format="%d/%m/%Y")
investpy_new_orders["datetime"] = investpy_new_orders["datetime_announced"] + pd.DateOffset(months=-1)
investpy_new_orders["datetime"] = investpy_new_orders["datetime"].apply(lambda dt: dt.replace(day=1))
investpy_new_orders["index"] = pd.to_numeric(investpy_new_orders["actual"])
investpy_new_orders["pct_change"] = investpy_new_orders["index"].pct_change(periods=12) * 100
investpy_new_orders["index_ma_3m"] = investpy_new_orders["index"].rolling(window=3).mean()


# 미국 실질 가계 소비 지출 (Monthly)
# Real Personal Consumption Expenditures (PCEC96)
# Units: Billions of Chained 2012 Dollars, Seasonally Adjusted Annual Rate
fred_PCEC96 = pd.read_pickle('./Market_Watch_Data/fred_PCEC96.pkl')
fred_PCEC96_pct_change = fred_PCEC96.pct_change(periods=12) * 100


# 그림 7.6 ISM 신규주문지수와 미국 실질가계소비
# 시각화: 월별 시계열 자료 2개를 서로 다른 y 축으로 표시하고 0 위치 통일
fig, ax1 = plt.subplots()
xlim_start = pd.to_datetime("2000-01-01", errors='coerce', format='%Y-%m-%d')

# 첫번째 시계열
color1 = "tab:blue"
ax1.set_xlabel("Dates")
ax1.set_ylabel("Real Personal Consumption Expenditures", color=color1)  # 데이터 레이블
ax1.plot(fred_PCEC96_pct_change.index, fred_PCEC96_pct_change, color=color1)
ax1.tick_params(axis="y")

# 두번째 시계열
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color2 = "tab:red"
ax2.set_ylabel("ISM Manufacturing New Orders Index (3 months moving average)", color=color2)  # 데이터 레이블
ax2.plot(investpy_new_orders.datetime, investpy_new_orders["index_ma_3m"], color=color2, linestyle='-')
ax2.tick_params(axis='y')

# 그래프 기타 설정
fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
ax1.set_ylim([-5, 10])
#ax2.set_ylim([0, 80])
# align_yaxis(ax1, 0, ax2, 0)  # 두 축이 동일한 0 값을 가지도록 조정
# plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlim(xlim_start, )
plt.show()

# 그림 저장
plt.savefig("./Lecture_Figures_output/fig7.6_ism_new_orders_and_personal_consumption_expenditures.png")  # 그림 저장


########################################################################################################################
# 그림 7.7 ISM 신규주문지수와 한국 수출

# ISM 신규주문지수
investpy_economic_calendar = pd.read_pickle('./Market_Watch_Data/investpy_economic_calendar_us_20000101_20220215.pkl')

investpy_new_orders = investpy_economic_calendar[investpy_economic_calendar['event'].str.contains("ISM Manufacturing New Orders")].copy()
investpy_new_orders["datetime_announced"] = pd.to_datetime(investpy_new_orders["date"], errors='coerce', format="%d/%m/%Y")
investpy_new_orders["datetime"] = investpy_new_orders["datetime_announced"] + pd.DateOffset(months=-1)
investpy_new_orders["datetime"] = investpy_new_orders["datetime"].apply(lambda dt: dt.replace(day=1))
investpy_new_orders["index"] = pd.to_numeric(investpy_new_orders["actual"])
investpy_new_orders["pct_change"] = investpy_new_orders["index"].pct_change(periods=12) * 100
investpy_new_orders["index_ma_3m"] = investpy_new_orders["index"].rolling(window=3).mean()

# 한국 수출 통계
# Exports: Value Goods for the Republic of Korea (XTEXVA01KRM667S)
# Units: US Dollars Monthly Level, Seasonally Adjusted
fred_XTEXVA01KRM667S = pd.read_pickle('./Market_Watch_Data/fred_XTEXVA01KRM667S.pkl')
fred_XTEXVA01KRM667S_pct_change = fred_XTEXVA01KRM667S.pct_change(periods=12) * 100
fred_XTEXVA01KRM667S_3m_ma = fred_XTEXVA01KRM667S.rolling(window=3).mean()
fred_XTEXVA01KRM667S_3m_ma_pct_change = fred_XTEXVA01KRM667S_3m_ma.pct_change(periods=12) * 100

# 그림 7.7 ISM 신규주문지수와 한국 수출
# 시각화: 월별 시계열 자료 2개를 서로 다른 y 축으로 표시하고 0 위치 통일
fig, ax1 = plt.subplots()
xlim_start = pd.to_datetime("2000-01-01", errors='coerce', format='%Y-%m-%d')

# 첫번째 시계열
color1 = "tab:blue"
ax1.set_xlabel("Dates")
ax1.set_ylabel("Korea Exports 3 Months Moving Average (%, YoY)", color=color1)  # 데이터 레이블
ax1.plot(fred_XTEXVA01KRM667S_3m_ma_pct_change.index, fred_XTEXVA01KRM667S_3m_ma_pct_change, color=color1)
ax1.tick_params(axis="y")

# 두번째 시계열
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color2 = "tab:red"
ax2.set_ylabel("ISM Manufacturing New Orders Index (3 months moving average)", color=color2)  # 데이터 레이블
ax2.plot(investpy_new_orders.datetime, investpy_new_orders["index_ma_3m"], color=color2, linestyle='-')
ax2.tick_params(axis='y')

# 그래프 기타 설정
fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
ax1.set_ylim([-50, 50])
#ax2.set_ylim([0, 80])
# align_yaxis(ax1, 0, ax2, 0)  # 두 축이 동일한 0 값을 가지도록 조정
# plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlim(xlim_start, )
plt.show()

# 그림 저장
plt.savefig("./Lecture_Figures_output/fig7.7_ism_new_orders_and_korea_exports.png")  # 그림 저장

