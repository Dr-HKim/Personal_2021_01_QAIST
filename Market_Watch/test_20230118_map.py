import folium
import pandas as pd
import json

seoul_map = folium.Map(location=[37.55, 126.98], zoom_start=12)
seoul_map.save("./seoul.html")

seoul_map2 = folium.Map(location=[37.55, 126.98], tiles="Stamen Terrain", zoom_start=12)
seoul_map2.save("./seoul2.html")

seoul_map3 = folium.Map(location=[37.55, 126.98], tiles="Stamen Toner", zoom_start=12)
seoul_map3.save("./seoul3.html")

file_path = "경기도인구데이터.xlsx"
df = pd.read_excel(file_path, index_col="구분")
df.columns = df.columns.map(str)

geo_path = "경기도행정구역경계.json"
try:
    geo_data = json.load(open(geo_path, encoding="utf-8"))
except:
    geo_data = json.load(open(geo_path, encoding="utf-8-sig"))

g_map = folium.Map(location=[37.55, 126.98], tiles="Stamen Terrain", zoom_start=9)
year = 2017

folium.Choropleth(
    geo_data=geo_data, data=df[year], columns=[df.index, df[year]], fill_color="YlOrRd", fill_opacity=0.7,
    line_opacity=0.3, threshold_scale=[10000, 100000, 300000, 500000, 700000], key_on="feature.properties.name",
    legend_name="인구 수").add_to(g_map)

g_map.save("경기도인구"+str(year)+".html")