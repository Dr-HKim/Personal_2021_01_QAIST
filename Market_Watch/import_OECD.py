# Created by Kim Hyeongjun on 05/01/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.
# 참고: https://stackoverflow.com/questions/40565871/read-data-from-oecd-api-into-python-and-pandas
# 참고: https://pandas-datareader.readthedocs.io/en/latest/remote_data.html#remote-data-oecd (Fama-French)

import requests
import pandas as pd
import re


def get_yyyymm_add_months(n_yyyymm, n_months):
    n_yyyy, n_mm = divmod(n_yyyymm, 100)
    n_months_y, n_months_m = divmod(n_mm + n_months - 1, 12)
    output_yyyy = n_yyyy + n_months_y
    output_mm = n_months_m + 1
    output_yyyymm = output_yyyy * 100 + output_mm
    return output_yyyymm


def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny+dy, maxy+dy)


def get_oecd_response(dataset, subjects, countries, frequency, startDate, endDate,
                      root_dir="https://stats.oecd.org/SDMX-JSON/data"):
    # Make URL for the OECD API and return a response
    # 4 dimensions: SUBJECT, LOCATION, FREQUENCY, TIME_PERIOD
    # OECD API: https://data.oecd.org/api/sdmx-json-documentation/#d.en.330346

    dimension = [subjects, countries, frequency]
    dimension_args = ['+'.join(d) for d in dimension]
    dimension_str = ".".join(dimension_args)

    url = root_dir + '/' + dataset + '/' + dimension_str + "/all?startTime=" + startDate + "&endTime=" + endDate + \
          "&dimensionAtObservation=allDimensions"

    print('Requesting URL ' + url)
    return requests.get(url=url)


def get_oecd_data(response):
    # Request data from OECD API and return pandas DataFrame

    # country: country code (max 1)
    # subject: list of subjects, empty list for all
    # measure: list of measures, empty list for all
    # frequency: 'M' for monthly and 'Q' for quarterly time series
    # startDate: date in YYYY-MM (2000-01) or YYYY-QQ (2000-Q1) format, None for all observations
    # endDate: date in YYYY-MM (2000-01) or YYYY-QQ (2000-Q1) format, None for all observations

    # Data download
    # response = requests.get(url)  # Open API URL 호출

    # Data transformation
    if (response.status_code == 200):
        responseJson = response.json()
        obsList = responseJson.get('dataSets')[0].get('observations')

        if (len(obsList) > 0):
            print('Data downloaded from %s' % response.url)

            subjectList = [
                item for item in responseJson.get('structure').get('dimensions').get('observation') if
                item['id'] == 'SUBJECT'][0]['values']
            locationList = [
                item for item in responseJson.get('structure').get('dimensions').get('observation') if
                item['id'] == 'LOCATION'][0]['values']
            frequencyList = [
                item for item in responseJson.get('structure').get('dimensions').get('observation') if
                item['id'] == 'FREQUENCY'][0]['values']
            timeList = [
                item for item in responseJson.get('structure').get('dimensions').get('observation') if
                item['id'] == 'TIME_PERIOD'][0]['values']

            obs = pd.DataFrame(obsList).transpose()
            obs.rename(columns={0: 'series'}, inplace=True)
            obs['id'] = obs.index
            obs = obs[['id', 'series']]
            obs['dimensions'] = obs.apply(lambda x: re.findall('\d+', x['id']), axis=1)
            obs_dim_expanded = obs["dimensions"].apply(pd.Series)
            obs_dim_expanded.columns = ["dim0", "dim1", "dim2", "dim3"]
            obs = pd.merge(obs, obs_dim_expanded, left_index=True, right_index=True, how='outer')

            obs['subject_id'] = obs.apply(lambda x: subjectList[int(x["dim0"])]['id'], axis=1)
            obs['subject_name'] = obs.apply(lambda x: subjectList[int(x["dim0"])]['name'], axis=1)
            obs['location_id'] = obs.apply(lambda x: locationList[int(x["dim1"])]['id'], axis=1)
            obs['location_name'] = obs.apply(lambda x: locationList[int(x["dim1"])]['name'], axis=1)
            obs['time'] = obs.apply(lambda x: timeList[int(x["dim3"])]['id'], axis=1)
            obs['names'] = obs['subject_id'].copy()  # + '_' + obs['measure']
            obs.reset_index(level=0, inplace=True)
            obs.rename(columns={"series": "datavalue"}, inplace=True)

            obs["yyyy"] = obs["time"].str.slice(start=0, stop=4).astype(int)
            obs["mm"] = obs["time"].str.slice(start=5, stop=7).astype(int)
            obs["yyyymm"] = obs["yyyy"] * 100 + obs["mm"]

            data = obs[["yyyymm", "subject_id", "subject_name", "location_id", "location_name", "datavalue"]]

            # data = obs.pivot_table(index='time', columns=['names'], values='series')
            return data

        else:
            print('Error: No available records, please change parameters')
    else:
        print('Error: %s' % response.status_code)


MM_END_DATE = "2022-01"

########################################################################################################################
# OECD 데이터 -> export -> Developer API -> Generate API queries
oecd_response = get_oecd_response(
    dataset="MEI_CLI",
    subjects=["LOLITOAA", "LOLITONO", "LOLITOTR_STSA", "LOLITOTR_GYSA", "BSCICP03", "CSCICP03",
              "LORSGPRT", "LORSGPNO", "LORSGPTD", "LORSGPOR_IXOBSA"],
    countries=["AUS", "AUT", "BEL", "CAN", "CHL", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN",
               "ISL", "IRL", "ISR", "ITA", "JPN", "KOR", "LUX", "MEX", "NLD", "NZL", "NOR", "POL", "PRT",
               "SVK", "SVN", "ESP", "SWE", "CHE", "TUR", "GBR", "USA", "EA19", "G4E", "G-7", "NAFTA",
               "OECDE", "OECD", "ONM", "A5M", "BRA", "CHN", "IND", "IDN", "RUS", "ZAF"],
    frequency="M", startDate="1990-01", endDate=MM_END_DATE
)

df_oecd = get_oecd_data(oecd_response)
counts_subjects = df_oecd[["subject_id", "subject_name"]].value_counts()
counts_location = df_oecd["location_name"].value_counts()

# YYYYMM 을 기준으로 그 달의 가장 마지막 날짜 입력
df_oecd["datetime"] = pd.to_datetime(
    get_yyyymm_add_months(df_oecd["yyyymm"], 1) * 100 + 1, errors='coerce', format='%Y%m%d') + pd.Timedelta(days=-1)

# 데이터 저장
df_oecd.to_pickle('./Market_Watch_Data/oecd_monthly.pkl')

########################################################################################################################
# OECD 경기선행지수
# LOLITOTR_GYSA: 12-month rate of change of the trend restored CLI
# LOLITONO: Normalised (CLI)
# LOLITOAA: Amplitude adjusted (CLI)
# 장기 추세를 제거하고 최근 수치에 가중치를 두는 방식으로 진폭조정된(Amplitude adjusted) CLI
# 100이 넘으면 경기 상승, 100을 밑돌면 경기 하강
df_oecd_cli = df_oecd[(df_oecd["location_id"] == "OECD") & (df_oecd["subject_id"] == "LOLITOTR_GYSA")].copy()
df_oecd_cli2 = df_oecd[(df_oecd["location_id"] == "OECD") & (df_oecd["yyyymm"] > 202107)].copy()


