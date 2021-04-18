# Python 샘플 코드 #
import pandas as pd
import requests
from data_raw.def_authentication import *
from bs4 import BeautifulSoup
from datetime import datetime


# 국토교통부_아파트매매 실거래 상세 자료
# 활용기간 2023.04.12 까지
# LAWD_CD = 11110  # 47290(경산) 지역코드 - 각 지역별 코드 행정표준코드관리시스템(www.code.go.kr)의 법정동코드 10자리 중 앞 5자리
# DEAL_YMD = 200601  # 계약월 - 실거래 자료의 계약년월 6자리
# numOfRows = 500  # 한 페이지 결과 수
# pageNo = 1  # 페이지번호
def get_apt_data(LAWD_CD, DEAL_YMD, numOfRows=10000, serviceKey=get_data_service_decoded_key()):
    # 호출하려는 OpenAPI URL 정의
    data_url = "".join(
        ["http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev?",
         "serviceKey=", serviceKey, "&LAWD_CD=", str(LAWD_CD), "&DEAL_YMD=", str(DEAL_YMD), "&numOfRows=",
         str(numOfRows)])

    # 정의된 OpenAPI URL을 호출
    data_response = requests.get(data_url)
    data_xml = BeautifulSoup(data_response.text, "xml")
    data_xml_row = data_xml.find_all("item")
    data_xml_row

    # XML에 포함된 항목들을 리스트로 저장
    list_items = ["거래금액", "건축년도", "년", "도로명", "도로명건물본번호코드", "도로명건물부번호코드",
                  "도로명시군구코드", "도로명일련번호코드", "도로명지상지하코드", "도로명코드",
                  "법정동", "법정동본번코드", "법정동부번코드", "법정동시군구코드", "법정동읍면동코드", "법정동지번코드",
                  "아파트", "월", "일", "일련번호", "전용면적", "지번", "지역코드", "층", "해제사유발생일", "해제여부"]

    # 리스트의 리스트 형태로 데이터프레임에 저장할 자료 만들기
    list_dataframe = []

    for n_obs in range(0, len(data_xml_row)):
        list_obs_values = []  # 동일한 관측치의 데이터는 모두 이 리스트에 저장된다
        for i in range(0, len(list_items)):
            # 특정 항목이 XML에 아예 존재하지 않는 경우가 있으므로 try 구문 사용
            try:
                list_obs_values.append(data_xml_row[n_obs].find(list_items[i]).text)
            except Exception as e:
                list_obs_values.append("")
                print("Error in " + str(n_obs) + "th obs, item: " + list_items[i] + ", " + str(e))
        list_dataframe.append(list_obs_values)  # 리스트의 리스트로 관측치 저장

    # 데이터프레임 형태로 변환
    df_apt = pd.DataFrame(list_dataframe, columns=list_items)
    return df_apt


########################################################################################################################

df_tmp1 = get_apt_data(LAWD_CD=11110, DEAL_YMD=202102)
df_tmp2 = get_apt_data(LAWD_CD=11320, DEAL_YMD=202102)
df_tmp3 = get_apt_data(LAWD_CD=11120, DEAL_YMD=202102)

########################################################################################################################
# Import TXT file 법정동코드 전체자료 불러오기
df_lawd_cd = pd.read_csv('./data_raw/법정동코드 전체자료.txt', sep="\t", engine='python', encoding="CP949")
df_lawd_cd["LAWD_CD"] = df_lawd_cd["법정동코드"].divmod(100000)[0]
df_lawd_cd_nodup = df_lawd_cd.drop_duplicates(subset=['LAWD_CD']).copy()  # 중복값 제외
df_lawd_cd_nodup_exist = df_lawd_cd_nodup[df_lawd_cd_nodup["폐지여부"] == "존재"].copy()

total_lawd_cd = df_lawd_cd_nodup_exist["LAWD_CD"]
tmp_lawd_cd = df_lawd_cd_nodup_exist["LAWD_CD"][3:10]

# 국토교통부_아파트매매 실거래 상세 자료는 2008년 1월부터 자료가 존재한다.
list_yyyymm = []
for n_year in range(2016, 2021):
    if n_year + 1 == 2021:
        for n_month in range(0, 3):
            list_yyyymm.append((n_year + 1) * 100 + n_month + 1)
    else:
        for n_month in range(0, 12):
            list_yyyymm.append((n_year + 1) * 100 + n_month + 1)
list_yyyymm.reverse()
list_yyyymm


# StopWatch: 코드 시작
time_this_code_start = datetime.now()
print("This code started at: " + str(time_this_code_start))

df_dataset_null = get_apt_data(LAWD_CD=11120, DEAL_YMD=202102)  # DataFrame 구성을 위해 공백 자료를 하나 만든다.

# 전국의 한달 자료 받는데 9분 소요
for yyyymm in list_yyyymm:
    df_dataset = df_dataset_null.copy()
    for lawd_cd in total_lawd_cd:
        df_apt = get_apt_data(LAWD_CD=lawd_cd, DEAL_YMD=yyyymm)
        df_apt.to_pickle("./data_raw/df_apt_" + str(yyyymm) + "_" + str(lawd_cd) + ".pkl")
        df_dataset = pd.concat([df_dataset, df_apt])
    df_dataset.to_pickle("./data_raw/df_dataset_" + str(yyyymm) + ".pkl")

# StopWatch: 코드 종료
time_this_code_end = datetime.now()
print("This code finished at: " + str(time_this_code_end))
print("Elapsed (in this code): " + str(time_this_code_end - time_this_code_start))

########################################################################################################################
# 국토교통부_아파트매매 실거래 상세 자료
# 활용기간 2023.04.12 까지
serviceKey = get_data_service_decoded_key()  # 인증키
LAWD_CD = 11110  # 47290(경산) 지역코드 - 각 지역별 코드 행정표준코드관리시스템(www.code.go.kr)의 법정동코드 10자리 중 앞 5자리
DEAL_YMD = 200601  # 계약월 - 실거래 자료의 계약년월 6자리
pageNo = 1  # 페이지번호
numOfRows = 500  # 한 페이지 결과 수

# 호출하려는 OpenAPI URL 정의
data_url = "".join(
    ["http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev?",
     "serviceKey=", serviceKey, "&LAWD_CD=", str(LAWD_CD), "&DEAL_YMD=", str(DEAL_YMD), "&numOfRows=", str(numOfRows)])

# 정의된 OpenAPI URL을 호출
data_response = requests.get(data_url)
data_xml = BeautifulSoup(data_response.text, "xml")
data_xml_row = data_xml.find_all("item")
print(data_xml)
data_xml_row

# XML에 포함된 항목들을 리스트로 저장
list_items = ["거래금액", "건축년도", "년", "도로명", "도로명건물본번호코드", "도로명건물부번호코드",
              "도로명시군구코드", "도로명일련번호코드", "도로명지상지하코드", "도로명코드",
              "법정동", "법정동본번코드", "법정동부번코드", "법정동시군구코드", "법정동읍면동코드", "법정동지번코드",
              "아파트", "월", "일", "일련번호", "전용면적", "지번", "지역코드", "층", "해제사유발생일", "해제여부"]

# 리스트의 리스트 형태로 데이터프레임에 저장할 자료 만들기
list_dataframe = []

for n_obs in range(0, len(data_xml_row)):
    list_obs_values = []  # 동일한 관측치의 데이터는 모두 이 리스트에 저장된다
    for i in range(0, len(list_items)):
        # 특정 항목이 XML에 아예 존재하지 않는 경우가 있으므로 try 구문 사용
        try:
            list_obs_values.append(data_xml_row[n_obs].find(list_items[i]).text)
        except Exception as e:
            list_obs_values.append("")
            print("Error in " + str(n_obs) + "th obs, item: " + list_items[i] + ", " + str(e))
    list_dataframe.append(list_obs_values)  # 리스트의 리스트로 관측치 저장

# 데이터프레임 형태로 변환
df = pd.DataFrame(list_dataframe, columns=list_items)

df_tmp = df[df['아파트'].str.contains("한신")]