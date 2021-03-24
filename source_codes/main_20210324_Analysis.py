# Created by Kim Hyeongjun on 03/22/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.

import pandas as pd

########################################################################################################################
# Import Pickle Dataset
processed_daily_20000101_Current = pd.read_pickle('./data_processed/processed_daily_20000101_Current.pkl')
processed_fs_1981_2020 = pd.read_pickle('./data_processed/processed_fs_1981_2020.pkl')

# 재무제표 자료는 2011년 이후부터 분기별 자료 사용 가능
sample_fs = processed_fs_1981_2020.loc[processed_fs_1981_2020["회계년"] > 2010]

date_start = pd.to_datetime("20200404", errors='coerce', format='%Y%m%d')
sample_daily = processed_daily_20000101_Current.loc[processed_daily_20000101_Current["Date"] > date_start]
