# Python 샘플 코드 #

import requests
from data_raw.def_authentication import *
from bs4 import BeautifulSoup

# 호출하려는 OpenAPI URL 정의
BOK_url = "".join(
    ["http://ecos.bok.or.kr/api/StatisticSearch/", AUTH_KEY, "/", REQ_TYPE, "/", LANG, "/", START_COUNT, "/",
     END_COUNT, "/", STAT_CODE, "/", CYCLE_TYPE, "/", START_DATE, "/", END_DATE, "/", ITEM_1, "/", ITEM_2, "/",
     ITEM_3])
# 정의된 OpenAPI URL을 호출합니다.
BOK_response = requests.get(BOK_url)


url = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev?_wadl&type=xml"
url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'
url = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev?LAWD_CD=11110&DEAL_YMD=201512&serviceKey="
service_key = get_data_service_key()
url2 = url + service_key
print(url2)

# 정의된 OpenAPI URL을 호출합니다.
data_response = requests.get(url2)

data_xml = BeautifulSoup(data_response.text, "xml")
data_xml_row = data_xml.find_all("row")

print(data_response.text)
print(data_xml)




from urllib2 import Request, urlopen
from urllib import urlencode, quote_plus


service_key = get_data_service_key()

url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'
queryParams = '?' + urlencode({ quote_plus('ServiceKey') : '서비스키', quote_plus('pageNo') : '1', quote_plus('numOfRows') : '10', quote_plus('LAWD_CD') : '11110', quote_plus('DEAL_YMD') : '201512' })

request = Request(url + queryParams)
request.get_method = lambda: 'GET'
response_body = urlopen(request).read()
print response_body