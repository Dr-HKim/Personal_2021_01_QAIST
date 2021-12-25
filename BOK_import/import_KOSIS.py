
# https://kosis.kr/openapi/index/index.jsp KOSIS 공유서비스 (id: yuii7890)
# 서비스이용 > 통계자료 > 자료등록

from data_raw.def_authentication import *
import requests
import pandas as pd


kosis_auth_key = get_kosis_auth_key()
kosis_user_id = get_kosis_user_id()


# KOSIS 제조업 평균가동률 (1980.01 시작)
end_YYYYMM = 202110
kosis_DT_1F31502 = "https://kosis.kr/openapi/statisticsData.do?method=getList&apiKey=" \
                   + kosis_auth_key + "&format=json&jsonVD=Y&userStatsId=" + kosis_user_id \
                   + "/101/DT_1F31502/2/1/20211225194325_2&prdSe=M&startPrdDe=" + "198001" + "&endPrdDe=" \
                   + str(end_YYYYMM)
kosis_response = requests.get(kosis_DT_1F31502)  # Open API URL 호출
data = kosis_response.json()
dfItem = pd.DataFrame.from_records(data)





kosis_url = get_kosis_url()
kosis_response = requests.get(kosis_url)  # Open API URL 호출
data = kosis_response.json()
dfItem = pd.DataFrame.from_records(data)



kosis_url = "https://kosis.kr/openapi/statisticsData.do?method=getList&apiKey="\
            "MDQzNmI2NWRhN2RiOGM3NTVhMDFmMGQ3MTgxZWQwZWE="\
            "&format=json&jsonVD=Y&userStatsId=yuii7890/101/DT_1F31502/2/1/20211225183549_2&prdSe=M&newEstPrdCnt=3"