
import pandas as pd
from datetime import datetime

fs_IFRSN = \
    pd.read_pickle('./DataGuide_processed/dg_fs_IFRSN.pkl')

processed_daily_20000101_Current = \
    pd.read_pickle('./DataGuide_processed/dg_daily_20000101_Current.pkl')


df_fs_tmp = fs_IFRSN.copy()
df_fs_tmp = df_fs_tmp.sort_values(by=['Symbol'])
df_fs_list = df_fs_tmp.drop_duplicates(subset=['Symbol'], keep='last')  # 3303개 기업

df_daily_tmp = processed_daily_20000101_Current.copy()
df_daily_tmp = df_daily_tmp.sort_values(by=['Symbol'])
df_daily_list = df_daily_tmp.drop_duplicates(subset=['Symbol'], keep='last')  # 2975개 기업






