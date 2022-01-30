
import pandas as pd
from datetime import datetime

kb_data02 = pd.read_pickle('./KB_Land_processed/kb_data02.pkl')  # 02.매매APT
kb_data28 = pd.read_pickle('./KB_Land_processed/kb_data28.pkl')  # 28.아파트매매전세비


df_price = kb_data02[["날짜", "전국_전체", "서울_전체", "강북_전체", "강남_전체"]].copy()
lookback_period = 12
df_price["pct_change_전국"] = df_price["전국_전체"].pct_change(lookback_period)
df_price["pct_change_서울"] = df_price["서울_전체"].pct_change(lookback_period)
df_price["pct_change_강북"] = df_price["강북_전체"].pct_change(lookback_period)
df_price["pct_change_강남"] = df_price["강남_전체"].pct_change(lookback_period)

df_jeonse_to_purchase = kb_data28[["날짜", "전국", "서울", "강북", "강남"]].copy()
df_jeonse_to_purchase["전세가율_전국"] = df_jeonse_to_purchase["전국"] / 100
df_jeonse_to_purchase["전세가율_서울"] = df_jeonse_to_purchase["서울"] / 100
df_jeonse_to_purchase["전세가율_강북"] = df_jeonse_to_purchase["강북"] / 100
df_jeonse_to_purchase["전세가율_강남"] = df_jeonse_to_purchase["강남"] / 100

df_price = pd.merge(df_price, df_jeonse_to_purchase[["날짜", "전세가율_전국", "전세가율_서울", "전세가율_강북", "전세가율_강남"]], left_on='날짜', right_on='날짜', how='left')
df_price["갭_전국"] = 1 - df_price["전세가율_전국"]

# 갭투자수익률 연율화 및 퍼센트 단위로 표기
df_price["갭투자수익률_전국"] = (df_price["pct_change_전국"] / (1 - df_price["전세가율_전국"])) * 12 / lookback_period * 100
df_price["갭투자수익률_서울"] = (df_price["pct_change_서울"] / (1 - df_price["전세가율_서울"])) * 12 / lookback_period * 100
df_price["갭투자수익률_강북"] = (df_price["pct_change_강북"] / (1 - df_price["전세가율_강북"])) * 12 / lookback_period * 100
df_price["갭투자수익률_강남"] = (df_price["pct_change_강남"] / (1 - df_price["전세가율_강남"])) * 12 / lookback_period * 100

# Convention for import of the pyplot interface
import matplotlib.pyplot as plt

plt.rc('font', size=12)
fig, ax = plt.subplots(figsize=(10, 6))

# Specify how our lines should look
ax.plot(df_price["날짜"], df_price["갭투자수익률_전국"], color='tab:orange', label='Gap_Nationwide')
ax.plot(df_price["날짜"], df_price["갭투자수익률_서울"], color='tab:olive', linestyle='--', label='Gap_Seoul')
ax.plot(df_price["날짜"], df_price["갭투자수익률_강남"], color='tab:blue', linestyle='--', label='Gap_Seoul')

# Same as above
ax.set_xlabel('Time')
ax.set_ylabel('Annualized Return (%)')
ax.set_title('Gap Return')
ax.grid(True)
ax.legend(loc='upper left')



# 시각화
plt.plot(kb_data02["날짜"], kb_data02["전국_전체"], color='r', label="Nationwide")
plt.plot(kb_data02["날짜"], kb_data02["서울_전체"], color='g', label="Seoul")
plt.xlabel('Dates', fontsize=10)
plt.ylabel('Rates (%)', fontsize=10)
plt.legend(loc='upper left')
plt.show()