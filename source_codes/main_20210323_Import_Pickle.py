# Created by Kim Hyeongjun on 03/22/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.

import pandas as pd
from datetime import datetime


dg_test_data = pd.read_pickle('./data_processed/dg_test_data.pkl')
dg_test_header = pd.read_pickle('./data_processed/dg_test_header.pkl')


dg_header0 = dg_test_header.transpose()
new_header = dg_header0.iloc[0] #grab the first row for the header
dg_header0 = dg_header0[1:] #take the data less the header row
dg_header0.columns = new_header #set the header row as the df header

dg_header1 = dg_header0.loc[dg_header0["Item Name"] == "기준가(원)"]
dg_header1 = dg_header1.reset_index()

symbol_names = dg_header1["Symbol Name"]
item_names = dg_header0["Item Name"]
item_names = item_names[0:5]

index = pd.MultiIndex.from_product([symbol_names, item_names], names=["symbol", "item"])
dg_data0 = dg_test_data.copy()
dg_data0 = dg_data0.iloc[:, 1:]
dg_data0.columns = index
