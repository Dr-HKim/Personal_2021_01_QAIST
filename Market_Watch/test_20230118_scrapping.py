import urllib.request
import re

# 웹에서 데이터 다운로드
url = "http://storage.googleapis.com/patents/grant_full_text/2014/ipg140107.zip"
print("Start Download")
frame, header = urllib.request.urlretrieve(url, "ipg140107.zip")
print("End Download")

# 파일 자동 다운로드
url = "http://www.google.com/googlebooks/uspto-patents-grants-text.html"
html = urllib.request.urlopen(url)
html_contents = str(html.read().decode("utf8"))
url_list = re.findall(r"(http)(.+)(zip)", html_contents)

for url in url_list:
    full_url = "".join(url)
    print(full_url)

file_name = "test.html"
fname, header = urllib.request.urlretrieve(full_url, file_name)

# 삼성전자 html 파싱
url_005930 = "https://finance.naver.com/item/main.nhn?code=005930"
html = urllib.request.urlopen(url_005930)
html_contents = str(html.read().decode("ms949"))

stock_results = re.findall("(\<dl class=\"blind\"\>)([\s\S]+?)(\<\/dl\>)", html_contents)
stock_results[0][1]

samsumg_stock = stock_results[0]
samsumg_index = samsumg_stock[1]

samsumg_stock
samsumg_index

index_list = re.findall("(\<dd\>)([\s\S]+?)(\<\/dd\>)", samsumg_index)
index_list

for index in index_list:
    print(index[1])