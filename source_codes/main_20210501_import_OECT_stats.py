# Created by Kim Hyeongjun on 05/01/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.
# 참고: https://stackoverflow.com/questions/40565871/read-data-from-oecd-api-into-python-and-pandas

import requests
import pandas as pd
import re


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

            data = obs[["time", "subject_id", "subject_name", "location_id", "location_name", "datavalue"]]

            # data = obs.pivot_table(index='time', columns=['names'], values='series')
            return data

        else:
            print('Error: No available records, please change parameters')
    else:
        print('Error: %s' % response.status_code)


# OECD 데이터 -> export -> Developer API -> Generate API queries

oecd_response = get_oecd_response(
    dataset="MEI_CLI",
    subjects=["LOLITOAA", "LOLITONO", "LOLITOTR_STSA", "LOLITOTR_GYSA", "BSCICP03", "CSCICP03",
              "LORSGPRT", "LORSGPNO", "LORSGPTD", "LORSGPOR_IXOBSA"],
    countries=["AUS", "AUT", "BEL", "CAN", "CHL", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN",
               "ISL", "IRL", "ISR", "ITA", "JPN", "KOR", "LUX", "MEX", "NLD", "NZL", "NOR", "POL", "PRT",
               "SVK", "SVN", "ESP", "SWE", "CHE", "TUR", "GBR", "USA", "EA19", "G4E", "G-7", "NAFTA",
               "OECDE", "OECD", "ONM", "A5M", "BRA", "CHN", "IND", "IDN", "RUS", "ZAF"],
    frequency="M", startDate="2019-04", endDate="2019-10"
)

df_tmp = get_oecd_data(oecd_response)

counts = df_tmp["subject_name"].value_counts()
counts = df_tmp["location_name"].value_counts()



df_tmp.columns



########################################################################################################################
OECD_ROOT_URL = "http://stats.oecd.org/SDMX-JSON/data"


def make_OECD_request(dsname, dimensions, params=None, root_dir=OECD_ROOT_URL):
    # Make URL for the OECD API and return a response
    # 4 dimensions: location, subject, measure, frequency
    # OECD API: https://data.oecd.org/api/sdmx-json-documentation/#d.en.330346

    if not params:
        params = {}

    dim_args = ['+'.join(d) for d in dimensions]
    dim_str = '.'.join(dim_args)

    url = root_dir + '/' + dsname + '/' + dim_str + '/all'

    print('Requesting URL ' + url)
    return rq.get(url=url, params=params)


def create_DataFrame_from_OECD(country='CZE', subject=[], measure=[], frequency='M', startDate=None, endDate=None):
    # Request data from OECD API and return pandas DataFrame

    # country: country code (max 1)
    # subject: list of subjects, empty list for all
    # measure: list of measures, empty list for all
    # frequency: 'M' for monthly and 'Q' for quarterly time series
    # startDate: date in YYYY-MM (2000-01) or YYYY-QQ (2000-Q1) format, None for all observations
    # endDate: date in YYYY-MM (2000-01) or YYYY-QQ (2000-Q1) format, None for all observations

    # Data download
    response = make_OECD_request('MEI'
                                 , [[country], subject, measure, [frequency]]
                                 , {'startTime': startDate, 'endTime': endDate,
                                    'dimensionAtObservation': 'AllDimensions'})

    # Data transformation
    if (response.status_code == 200):
        responseJson = response.json()
        obsList = responseJson.get('dataSets')[0].get('observations')

        if (len(obsList) > 0):
            print('Data downloaded from %s' % response.url)

            timeList = [item for item in responseJson.get('structure').get('dimensions').get('observation') if
                        item['id'] == 'TIME_PERIOD'][0]['values']
            subjectList = [item for item in responseJson.get('structure').get('dimensions').get('observation') if
                           item['id'] == 'SUBJECT'][0]['values']
            measureList = [item for item in responseJson.get('structure').get('dimensions').get('observation') if
                           item['id'] == 'MEASURE'][0]['values']

            obs = pd.DataFrame(obsList).transpose()
            obs.rename(columns={0: 'series'}, inplace=True)
            obs['id'] = obs.index
            obs = obs[['id', 'series']]
            obs['dimensions'] = obs.apply(lambda x: re.findall('\d+', x['id']), axis=1)
            obs['subject'] = obs.apply(lambda x: subjectList[int(x['dimensions'][1])]['id'], axis=1)
            obs['measure'] = obs.apply(lambda x: measureList[int(x['dimensions'][2])]['id'], axis=1)
            obs['time'] = obs.apply(lambda x: timeList[int(x['dimensions'][4])]['id'], axis=1)
            obs['names'] = obs['subject'] + '_' + obs['measure']

            data = obs.pivot_table(index='time', columns=['names'], values='series')
            return (data)

        else:
            print('Error: No available records, please change parameters')
    else:
        print('Error: %s' % response.status_code)


data = create_DataFrame_from_OECD(frequency='M', subject=['MEI_CLI'])

data = create_DataFrame_from_OECD(country='CZE', subject=['LOCOPCNO'])
data = create_DataFrame_from_OECD(country='USA', frequency='Q', startDate='2009-Q1', endDate='2010-Q1')
data = create_DataFrame_from_OECD(country='USA', frequency='M', startDate='2009-01', endDate='2010-12')
data = create_DataFrame_from_OECD(country='USA', frequency='M', subject=['B6DBSI01'])
data = create_DataFrame_from_OECD(country='USA', frequency='Q', subject=['B6DBSI01'])

data = create_DataFrame_from_OECD(country='OECD', frequency='M', subject=['LOLITOAA'], startDate='2019-04',
                                  endDate='2021-03')

from bs4 import BeautifulSoup

oecd_url = "https://stats.oecd.org/SDMX-JSON/data/MEI_CLI/LOLITOAA+LOLITONO+LOLITOTR_STSA+LOLITOTR_GYSA+BSCICP03+CSCICP03+LORSGPRT+LORSGPNO+LORSGPTD+LORSGPOR_IXOBSA.AUS+AUT+BEL+CAN+CHL+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA+EA19+G4E+G-7+NAFTA+OECDE+OECD+ONM+A5M+BRA+CHN+IND+IDN+RUS+ZAF.M/all?startTime=2019-04&endTime=2021-03&dimensionAtObservation=allDimensions"
oecd_response = requests.get(oecd_url)  # Open API URL 호출
responseJson = oecd_response.json()
obsList = responseJson.get('dataSets')[0].get('observations')

# Data download
country = ["OECD", "KOR", "JPN"]
subject = ["LOLITOAA", "LOLITONO"]
measure = []
frequency = "M"
startDate = '2019-04'
endDate = '2021-03'
response = make_OECD_request('MEI', [country, subject, measure, frequency],
                             {'startTime': startDate, 'endTime': endDate, 'dimensionAtObservation': 'AllDimensions'})

oecd_url = "https://stats.oecd.org/restsdmx/sdmx.ashx/GetData/MEI_CLI/LOLITOAA+LOLITONO+LOLITOTR_STSA+LOLITOTR_GYSA+BSCICP03+CSCICP03+LORSGPRT+LORSGPNO+LORSGPTD+LORSGPOR_IXOBSA.AUS+AUT+BEL+CAN+CHL+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA+EA19+G4E+G-7+NAFTA+OECDE+OECD+ONM+A5M+BRA+CHN+IND+IDN+RUS+ZAF.M/all?startTime=2019-04&endTime=2021-03"
oecd_response = requests.get(oecd_url)  # Open API URL 호출
oecd_response.status_code

oecd_response.text

responseJson = oecd_response.json()
obsList = responseJson.get('dataSets')[0].get('observations')

oecd_xml = BeautifulSoup(oecd_response.text, "xml")
oecd_xml_row = oecd_xml.find_all("OBS")

oecd_xml_row[1]

oecd_response.text

data = oecd_response.json()
dfItem = pd.DataFrame.from_records(data)

oecd_url = "https://stats.oecd.org/SDMX-JSON/data/MEI_CLI/LOLITOAA+LOLITONO+LOLITOTR_STSA+LOLITOTR_GYSA+BSCICP03+CSCICP03+LORSGPRT+LORSGPNO+LORSGPTD+LORSGPOR_IXOBSA.AUS+AUT+BEL+CAN+CHL+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA+EA19+G4E+G-7+NAFTA+OECDE+OECD+ONM+A5M+BRA+CHN+IND+IDN+RUS+ZAF.M/all?startTime=2019-04&endTime=2021-03&dimensionAtObservation=allDimensions"

oecd_url = "https://stats.oecd.org/SDMX-JSON/data/MEI_CLI/LOLITOAA+LOLITONO+LOLITOTR_STSA+LOLITOTR_GYSA+BSCICP03+CSCICP03+LORSGPRT+LORSGPNO+LORSGPTD+LORSGPOR_IXOBSA.JPN+KOR+OECD.M/all?startTime=2019-04&endTime=2019-10&dimensionAtObservation=allDimensions"
response = requests.get(oecd_url)  # Open API URL 호출
responseJson = response.json()

responseJson

responseJson.get("structure").get('dimensions').get('observation')

obsList = responseJson.get('dataSets')[0].get('observations')

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

max(obs["dim0"].astype(int))
max(obs["dim1"].astype(int))
max(obs["dim2"].astype(int))
max(obs["dim3"].astype(int))

obs["dim0_int"] = obs["dim0"].astype(int)

counts = obs["dim1"].value_counts()

obs['subject_id'] = obs.apply(lambda x: subjectList[int(x["dim0"])]['id'], axis=1)
obs['subject_name'] = obs.apply(lambda x: subjectList[int(x["dim0"])]['name'], axis=1)
obs['time'] = obs.apply(lambda x: timeList[int(x["dim3"])]['id'], axis=1)
obs['location_id'] = obs.apply(lambda x: locationList[int(x["dim1"])]['id'], axis=1)
obs['location_name'] = obs.apply(lambda x: locationList[int(x["dim1"])]['name'], axis=1)

obs['dimensions'][1][1]

obs['subject'] = obs.apply(lambda x: subjectList[int(x['dimensions'][1])]['id'], axis=1)
obs['measure'] = obs.apply(lambda x: measureList[int(x['dimensions'][2])]['id'], axis=1)
obs['time'] = obs.apply(lambda x: timeList[int(x['dimensions'][4])]['id'], axis=1)
obs['names'] = obs['subject'] + '_' + obs['measure']

data = obs.pivot_table(index='time', columns=['names'], values='series')

tmp = get_oecd_url(dataset="MEI_CLI",
                   subjects=["LOLITOAA", "LOLITONO", "LOLITOTR_STSA", "LOLITOTR_GYSA", "BSCICP03", "CSCICP03",
                             "LORSGPRT", "LORSGPNO", "LORSGPTD", "LORSGPOR_IXOBSA"],
                   countries=["AUS", "AUT", "BEL", "CAN", "CHL", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN",
                              "ISL", "IRL", "ISR", "ITA", "JPN", "KOR", "LUX", "MEX", "NLD", "NZL", "NOR", "POL", "PRT",
                              "SVK", "SVN", "ESP", "SWE", "CHE", "TUR", "GBR", "USA", "EA19", "G4E", "G-7", "NAFTA",
                              "OECDE", "OECD", "ONM", "A5M", "BRA", "CHN", "IND", "IDN", "RUS", "ZAF"],
                   frequency="M", startDate="2019-04", endDate="2019-10"
                   )

frequency = "M"
startTime = "2019-04"
endTime = "2019-010"

dimension = [subjects, countries, frequency]
dimension_args = ['+'.join(d) for d in dimension]
dimension_str = ".".join(dimension_args)

dataset = "MEI_CLI"

OECD_ROOT_URL = "http://stats.oecd.org/SDMX-JSON/data"
{'startTime': startDate, 'endTime': endDate, 'dimensionAtObservation': 'allDimensions'}
url = root_dir + '/' + dataset + '/' + dimension_str + '/all'

oecd_url = "https://stats.oecd.org/SDMX-JSON/data/MEI_CLI/LOLITOAA+LOLITONO+LOLITOTR_STSA+LOLITOTR_GYSA+BSCICP03+CSCICP03+LORSGPRT+LORSGPNO+LORSGPTD+LORSGPOR_IXOBSA.JPN+KOR+OECD.M/all?startTime=2019-04&endTime=2019-10&dimensionAtObservation=allDimensions"

df_tmp0 = create_DataFrame_from_OECD(oecd_url)


def make_OECD_request(dsname, dimensions, params=None, root_dir=OECD_ROOT_URL):
    # Make URL for the OECD API and return a response
    # 4 dimensions: location, subject, measure, frequency
    # OECD API: https://data.oecd.org/api/sdmx-json-documentation/#d.en.330346

    if not params:
        params = {}

    dim_args = ['+'.join(d) for d in dimensions]
    dim_str = '.'.join(dim_args)

    url = root_dir + '/' + dsname + '/' + dim_str + '/all'

    print('Requesting URL ' + url)
    return rq.get(url=url, params=params)


subjects = ["LOLITOAA", "LOLITONO", "LOLITOTR_STSA", "LOLITOTR_GYSA", "BSCICP03", "CSCICP03",
            "LORSGPRT", "LORSGPNO", "LORSGPTD", "LORSGPOR_IXOBSA"]

countries = ["AUS", "AUT", "BEL", "CAN", "CHL", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN",
             "ISL", "IRL", "ISR", "ITA", "JPN", "KOR", "LUX", "MEX", "NLD", "NZL", "NOR", "POL", "PRT",
             "SVK", "SVN", "ESP", "SWE", "CHE", "TUR", "GBR", "USA", "EA19", "G4E", "G-7", "NAFTA",
             "OECDE", "OECD", "ONM", "A5M", "BRA", "CHN", "IND", "IDN", "RUS", "ZAF"]
