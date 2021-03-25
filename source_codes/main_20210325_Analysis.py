# Created by Kim Hyeongjun on 03/22/2021.
# Copyright © 2021 dr-hkim.github.io. All rights reserved.

import pandas as pd

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

df_dataset = sample_daily.copy()
list_symbol = df_dataset['Symbol'].drop_duplicates()
list_symbol = list_symbol.reset_index(drop=True)

df_firm_data = df_dataset[df_dataset['Symbol'] == list_symbol[34]]
list_date = df_firm_data['Date']
list_date = list_date.reset_index(drop=True)
list_date[2].year
list_date[2] + pd.Timedelta(days=15)

import datetime

datee = datetime.datetime.strptime(list_date[2], "%Y-%m-%d")

datetime.fromtimestamp(list_date[2])

list_date[2].datetime.year

pd.DatetimeIndex(list_date[2]).year
list_date[2]


df['year'] = df['ArrivalDate'].dt.year



for firm_symbol in list_symbol:
    df_firm_data = df_dataset[df_dataset['Symbol'] == firm_symbol]

class DataProcessing:
    """
    데이터를 입력하면 기계학습에 사용 가능한 형태로 변경
    """

    def __init__(self, df_dataset, list_variable_names, nmonths_lookback):

        output_total_lookback = []
        output_total_forecast = []

        list_CUSIP = df_dataset['CRSP_CUSIP'].drop_duplicates()

        for firm_CUSIP in list_CUSIP:
            df_firm_data = df_dataset[df_dataset['CRSP_CUSIP'] == firm_CUSIP]

            n_obs = len(df_firm_data.index) - nmonths_lookback + 1
            n_variables = len(list_variable_names)

            output_firm_lookback = []
            output_firm_forecast = []

            for i in range(0, n_obs):
                df_firm_data_12m = df_firm_data[0 + i:nmonths_lookback + i]
                df_lookback = df_firm_data_12m[list_variable_names].values
                df_forecast = df_firm_data_12m[-1:][['DEPVAR1Y']].values
                if i == 0:
                    output_firm_lookback = df_lookback
                    output_firm_forecast = df_forecast
                else:
                    output_firm_lookback = np.vstack([output_firm_lookback, df_lookback])
                    output_firm_forecast = np.vstack([output_firm_forecast, df_forecast])

            reshaped_output_firm_lookback = output_firm_lookback.reshape((n_obs, nmonths_lookback, n_variables))
            reshaped_output_firm_forecast = output_firm_forecast.reshape((n_obs, 1))

            if firm_CUSIP == list_CUSIP[0:1].values:
                output_total_lookback = reshaped_output_firm_lookback
                output_total_forecast = reshaped_output_firm_forecast
            else:
                output_total_lookback = np.vstack([output_total_lookback, reshaped_output_firm_lookback])
                output_total_forecast = np.vstack([output_total_forecast, reshaped_output_firm_forecast])

        output_total_forecast = output_total_forecast.reshape(len(output_total_forecast), )  # (n, 1) -> (n,) 차원 변경

        self.output_total_lookback = output_total_lookback
        self.output_total_forecast = output_total_forecast
        self.output_total_lookback_lastobs = output_total_lookback[:, -1, :]  # 일반적인 모형 적용을 위해


class DataProcessingStep5:
    def __init__(self, df_training, df_validation, df_test, list_variable_names):
        # StopWatch: 코드 시작
        time_step5_start = datetime.now()
        print("Step5 started at: " + str(time_step5_start))

        # 빠른 기계학습 개발을 위하여 샘플 자료 작성
        # 참고: df_test 가운데 6910 개 기업 정상, 61개 기업 부도
        df_training_sample = get_dataset_sample(df_dataset=df_training, n_normal=80, n_bankrupt=80)
        df_validation_sample = get_dataset_sample(df_dataset=df_validation, n_normal=20, n_bankrupt=20)
        df_test_sample = get_dataset_sample(df_dataset=df_test, n_normal=2000, n_bankrupt=20)

        # Standardization: MinMaxScaler 사용, 훈련(training) 데이터셋에 맞추어 정규화 실시
        # todo: 음수 값이 있어도 MinMaxScaler 를 쓰는게 맞을까?
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaler.fit(df_training[list_variable_names])

        # 동일한 scaler 를 training, validation, test dataset 에 적용
        df_training[list_variable_names] = scaler.transform(df_training[list_variable_names])
        df_validation[list_variable_names] = scaler.transform(df_validation[list_variable_names])
        df_test[list_variable_names] = scaler.transform(df_test[list_variable_names])

        # 샘플자료에도 동일한 scaler 를 적용
        df_training_sample[list_variable_names] = scaler.transform(df_training_sample[list_variable_names])
        df_validation_sample[list_variable_names] = scaler.transform(df_validation_sample[list_variable_names])
        df_test_sample[list_variable_names] = scaler.transform(df_test_sample[list_variable_names])

        # 클래스를 사용하여 각 자료마다 X, X_lastobs, Y 생성
        step5_training = DataProcessing(
            df_dataset=df_training, list_variable_names=list_variable_names, nmonths_lookback=12)
        # StopWatch: Step5_training 종료
        time_step5_training = datetime.now()
        print("Step5_training finished at: " + str(time_step5_training))
        print("Elapsed (in step5): " + str(time_step5_training - time_step5_start))

        step5_validation = DataProcessing(
            df_dataset=df_validation, list_variable_names=list_variable_names, nmonths_lookback=12)
        # StopWatch: Step5_validation 종료
        time_step5_validation = datetime.now()
        print("Step5_validation finished at: " + str(time_step5_validation))
        print("Elapsed (in step5): " + str(time_step5_validation - time_step5_start))

        step5_test = DataProcessing(
            df_dataset=df_test, list_variable_names=list_variable_names, nmonths_lookback=12)
        # StopWatch: Step5_test 종료
        time_step5_test = datetime.now()
        print("Step5_test finished at: " + str(time_step5_test))
        print("Elapsed (in step5): " + str(time_step5_test - time_step5_start))

        # 샘플자료에도 클래스를 사용하여 각 자료마다 X, X_lastobs, Y 생성
        step5_training_sample = DataProcessing(
            df_dataset=df_training_sample, list_variable_names=list_variable_names, nmonths_lookback=12)
        step5_validation_sample = DataProcessing(
            df_dataset=df_validation_sample, list_variable_names=list_variable_names, nmonths_lookback=12)
        step5_test_sample = DataProcessing(
            df_dataset=df_test_sample, list_variable_names=list_variable_names, nmonths_lookback=12)
        # StopWatch: Step5_sample 종료
        time_step5_sample = datetime.now()
        print("Step5_sample finished at: " + str(time_step5_sample))
        print("Elapsed (in step5): " + str(time_step5_sample - time_step5_start))

        self.train_X = step5_training.output_total_lookback
        self.train_X_lastobs = step5_training.output_total_lookback_lastobs
        self.train_Y = step5_training.output_total_forecast

        self.validation_X = step5_validation.output_total_lookback
        self.validation_X_lastobs = step5_validation.output_total_lookback_lastobs
        self.validation_Y = step5_validation.output_total_forecast

        self.test_X = step5_test.output_total_lookback
        self.test_X_lastobs = step5_test.output_total_lookback_lastobs
        self.test_Y = step5_test.output_total_forecast

        self.sample_train_X = step5_training_sample.output_total_lookback
        self.sample_train_X_lastobs = step5_training_sample.output_total_lookback_lastobs
        self.sample_train_Y = step5_training_sample.output_total_forecast

        self.sample_validation_X = step5_validation_sample.output_total_lookback
        self.sample_validation_X_lastobs = step5_validation_sample.output_total_lookback_lastobs
        self.sample_validation_Y = step5_validation_sample.output_total_forecast

        self.sample_test_X = step5_test_sample.output_total_lookback
        self.sample_test_X_lastobs = step5_test_sample.output_total_lookback_lastobs
        self.sample_test_Y = step5_test_sample.output_total_forecast


