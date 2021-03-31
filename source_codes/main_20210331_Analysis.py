# Created by Kim Hyeongjun on 03/22/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.

# Import Packages
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

########################################################################################################################
# # Import Pickle Dataset
# processed_daily_20000101_Current = pd.read_pickle('./data_processed/processed_daily_20000101_Current.pkl')
# processed_fs_1981_2020 = pd.read_pickle('./data_processed/processed_fs_1981_2020.pkl')
#
# # 재무제표 자료는 2011년 이후부터 분기별 자료 사용 가능
# sample_fs = processed_fs_1981_2020.loc[processed_fs_1981_2020["회계년"] > 2015]
#
# date_start = pd.to_datetime("20150101", errors='coerce', format='%Y%m%d')
# sample_daily = processed_daily_20000101_Current.loc[processed_daily_20000101_Current["Date"] > date_start]
#
# # 데이터 저장하기
# sample_fs.to_pickle('./data_processed/sample_fs.pkl')
# sample_daily.to_pickle('./data_processed/sample_daily.pkl')

########################################################################################################################
# Import Pickle Dataset
sample_fs = pd.read_pickle('./data_processed/sample_fs.pkl')
sample_daily = pd.read_pickle('./data_processed/sample_daily.pkl')

# YYYYQQ = 회계년 + 주기 (1Q -> Q1)
df_fs_data = sample_fs.copy()
df_fs_data["YYYYQQ"] = df_fs_data["회계년"].astype(str) + "Q" + df_fs_data["주기"].str.slice(start=0, stop=1)

col_names1 = df_fs_data.columns[0:5].to_series()
col_names2 = pd.Series(df_fs_data.columns[-1])
col_names3 = df_fs_data.columns[5:-1].to_series()
col_names = col_names1.append([col_names2])
col_names = col_names.append(col_names3)

df_fs_data = df_fs_data[col_names]
df_fs_data["SEQ"] = df_fs_data["총자본(천원)"]  # Stockholders' Equity - Total


df_daily_data = sample_daily.copy()

date_start = pd.to_datetime("20150101", errors='coerce', format='%Y%m%d')
date_start.year
date_start.month


# 사업보고서: 결산 후 90일 이내 (12월 결산법인 03/31)
# 분기보고서: 분기 경과 후 45일 이내 (12월 결산법인 05/17)
# 반기보고서: 반기 경과 후 45일 이내 (12월 결산법인 08/16)
# 분기보고서: 분기 경과 후 45일 이내 (12월 결산법인 11/15)


df_daily_data["Date"] > date_start

# COMPUSTAT
# Identifying Information (8/8)
# GVKEY -- Global Company Key
# CONM -- Company Name
# TIC -- Ticker Symbol
# CUSIP -- CUSIP
# CIK -- CIK Number
# EXCHG -- Stock Exchange Code
# FYR -- Fiscal Year-End
# FIC -- Foreign Incorporation Code

# Identifying Information, cont (2/34)
# DLDTE -- Research Company Deletion Date
# DLRSN -- Research Co Reason for Deletion (02: Bankruptcy, 03: Liquidation)

# Company Descriptor (25/25)
# ACCTCHG -- Adoption of Accounting Changes
# ACCTSTD -- Accounting Standard
# ACQMETH -- Acquisition Method
# ADRR -- ADR Ratio
# AJEX -- Adjustment Factor (Company) - Cumulative by Ex-Date
# AJP -- Adjustment Factor (Company) - Cumulative byPay-Date
# APDEDATE -- Actual Period End date
# BSPR -- Balance Sheet Presentation
# COMPST -- Comparability Status (다른 기관과 비교시 주의점, 인수합병 / 회계변경 등)
# CURNCD -- Native Currency Code
# CURRTR -- Currency Translation Rate
# CURUSCN -- US Canadian Translation Rate
# FDATE -- Final Date
# FINAL -- Final Indicator Flag
# FYEAR -- Data Year - Fiscal
# ISMOD -- Income Statement Model Number (operating expense 표기 방법)
# LTCM -- Long Term Contract Method
# OGM -- OIL & GAS METHOD (Oil / Gas 기업의 수익 인식 방법)
# PDATE -- Preliminary Date (예비 업데이트 날짜)
# PDDUR -- Period Duration (income statement 에서 다루는 개월 수)
# SCF -- Cash Flow Format
# SRC -- Source Document
# STALT -- Status Alert
# UDPL -- Utility - Liberalized Depreciation Code
# UPD -- Update Code

# Balance Sheet Items (10/382)
# ACT -- Current Assets - Total
# AT -- Assets - Total
# CEQ -- Common/Ordinary Equity - Total
# CEQL -- Common Equity Liquidation Value
# CH -- Cash
# CHE -- Cash and Short-Term Investments
# LCT -- Current Liabilities - Total
# LT -- Liabilities - Total
# RE -- Retained Earnings
# SEQ -- Stockholders' Equity - Total
# WCAP -- Working Capital (Balance Sheet)

# Income Statement Items (3/328)
# EBIT -- Earnings Before Interest and Taxes
# NI -- Net Income (Loss)
# SALE -- Sales/Turnover (Net)

# Miscellaneous Items (1/114)
# CSHO -- Common Shares Outstanding

# Supplemental Data Items (1/17)
# MKVALT -- Market Value - Total - Fiscal
# Market value for single issue companies is common shares outstanding multiplied by the month-end price that corresponds to the period end date.
