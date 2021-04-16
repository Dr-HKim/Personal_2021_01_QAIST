# Python 샘플 코드 #
import pandas as pd
import requests
from data_raw.def_authentication import *
from bs4 import BeautifulSoup


url = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev?LAWD_CD=11110&DEAL_YMD=201512&serviceKey="
service_key = get_data_service_decoded_key()
url2 = url + service_key
print(url2)

# 정의된 OpenAPI URL을 호출합니다.
data_response = requests.get(url2)
data_xml = BeautifulSoup(data_response.text, "xml")
data_xml_row = data_xml.find_all("item")
data_xml_row


print(data_xml_row[1])

list_ITEM01 = []
list_ITEM02 = []
list_ITEM03 = []
list_ITEM04 = []
list_ITEM05 = []
list_ITEM06 = []
list_ITEM07 = []
list_ITEM08 = []
list_ITEM09 = []
list_ITEM10 = []
list_ITEM11 = []
list_ITEM12 = []
list_ITEM13 = []
list_ITEM14 = []
list_ITEM15 = []
list_ITEM16 = []
list_ITEM17 = []
list_ITEM18 = []
list_ITEM19 = []
list_ITEM20 = []
list_ITEM21 = []
list_ITEM22 = []
list_ITEM23 = []
list_ITEM24 = []
list_ITEM25 = []


for item in data_xml_row:
    item_ITEM01 = item.find("거래금액").text
    item_ITEM02 = item.find("건축년도").text
    item_ITEM03 = item.find("년").text
    item_ITEM04 = item.find("도로명").text
    item_ITEM05 = item.find("도로명건물본번호코드").text
    item_ITEM06 = item.find("도로명건물부번호코드").text
    item_ITEM07 = item.find("도로명시군구코드").text
    item_ITEM08 = item.find("도로명일련번호코드").text
    item_ITEM09 = item.find("도로명지상지하코드").text
    item_ITEM09 = item.find("도로명코드").text
    item_ITEM10 = item.find("법정동").text
    item_ITEM11 = item.find("법정동본번코드").text
    item_ITEM12 = item.find("법정동부번코드").text
    item_ITEM13 = item.find("법정동시군구코드").text
    item_ITEM14 = item.find("법정동읍면동코드").text
    item_ITEM15 = item.find("법정동지번코드").text
    item_ITEM16 = item.find("아파트").text
    item_ITEM17 = item.find("월").text
    item_ITEM18 = item.find("일").text
    item_ITEM19 = item.find("일련번호").text
    item_ITEM20 = item.find("전용면적").text
    item_ITEM21 = item.find("지번").text
    item_ITEM22 = item.find("지역코드").text
    item_ITEM23 = item.find("층").text
    item_ITEM24 = item.find("해제사유발생일").text
    item_ITEM25 = item.find("해제여부").text

    list_ITEM01.append(item_ITEM01)
    list_ITEM02.append(item_ITEM02)
    list_ITEM03.append(item_ITEM03)
    list_ITEM04.append(item_ITEM04)
    list_ITEM05.append(item_ITEM05)
    list_ITEM06.append(item_ITEM06)
    list_ITEM07.append(item_ITEM07)
    list_ITEM08.append(item_ITEM08)
    list_ITEM09.append(item_ITEM09)
    list_ITEM10.append(item_ITEM10)
    list_ITEM11.append(item_ITEM11)
    list_ITEM12.append(item_ITEM12)
    list_ITEM13.append(item_ITEM13)
    list_ITEM14.append(item_ITEM14)
    list_ITEM15.append(item_ITEM15)
    list_ITEM16.append(item_ITEM16)
    list_ITEM17.append(item_ITEM17)
    list_ITEM18.append(item_ITEM18)
    list_ITEM19.append(item_ITEM19)
    list_ITEM20.append(item_ITEM20)
    list_ITEM21.append(item_ITEM21)
    list_ITEM22.append(item_ITEM22)
    list_ITEM23.append(item_ITEM23)
    list_ITEM24.append(item_ITEM24)
    list_ITEM25.append(item_ITEM25)



df_BOK = pd.DataFrame(list_ITEM01, columns=["item_ITEM01"])
df_BOK["item_ITEM02"] = list_ITEM02
df_BOK["item_ITEM03"] = list_ITEM03
df_BOK["item_ITEM04"] = list_ITEM04
df_BOK["item_ITEM05"] = list_ITEM05
df_BOK["item_ITEM06"] = list_ITEM06
df_BOK["item_ITEM07"] = list_ITEM07
df_BOK["item_ITEM08"] = list_ITEM08
df_BOK["item_ITEM09"] = list_ITEM09
df_BOK["item_ITEM10"] = list_ITEM10
df_BOK["item_ITEM11"] = list_ITEM11
df_BOK["item_ITEM12"] = list_ITEM12
df_BOK["item_ITEM13"] = list_ITEM13
df_BOK["item_ITEM14"] = list_ITEM14
df_BOK["item_ITEM15"] = list_ITEM15
df_BOK["item_ITEM16"] = list_ITEM16
df_BOK["item_ITEM17"] = list_ITEM17
df_BOK["item_ITEM18"] = list_ITEM18
df_BOK["item_ITEM19"] = list_ITEM19
df_BOK["item_ITEM20"] = list_ITEM20
df_BOK["item_ITEM21"] = list_ITEM21
df_BOK["item_ITEM22"] = list_ITEM22
df_BOK["item_ITEM23"] = list_ITEM23
df_BOK["item_ITEM24"] = list_ITEM24
df_BOK["item_ITEM25"] = list_ITEM25
