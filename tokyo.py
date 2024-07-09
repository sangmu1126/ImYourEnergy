import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# 데이터 로드
electricity_data = pd.read_csv('datasets/Training/Elec/Tokyo_elec.csv')
weather_data = pd.read_csv('datasets/Training/Weather/Tokyo_weather.csv')


# 날짜 형식 변환
electricity_data['Date'] = pd.to_datetime(electricity_data['Date'])
weather_data['Date'] = pd.to_datetime(weather_data['Date'])

# 데이터 병합
data = pd.merge(electricity_data, weather_data, on='Date')

# NaN 및 Infinite 값 확인 및 처리
data.replace([np.inf, -np.inf], np.nan, inplace=True)
data.dropna(inplace=True)

# 특성과 타겟 설정
features = ['Avg_Temperature_C', 'Max_Temperature_C', 'Min_Temperature_C', 'Precipitation_mm', 'Humidity_%', 'Sunshine_Hours']
target = 'Electricity_Consumption_GWh'

# 특성 스케일링 (타겟과 분리해서 스케일링)
feature_scaler = MinMaxScaler()
data[features] = feature_scaler.fit_transform(data[features])

target_scaler = MinMaxScaler()
data[target] = target_scaler.fit_transform(data[[target]])

# 시계열 데이터셋 생성
def create_dataset(data, feature_cols, target_col, time_steps=1):
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[feature_cols].iloc[i:(i + time_steps)].values)
        y.append(data[target_col].iloc[i + time_steps])
    return np.array(X), np.array(y)

time_steps = 12
X, y = create_dataset(data, features, target, time_steps)

# 학습 및 검증 데이터 분리 (2021년 1월 ~ 2023년 12월 사용)
train_size = int(len(data[(data['Date'] >= '2021-01-01') & (data['Date'] <= '2023-12-31')]) - time_steps)
X_train, y_train = X[:train_size], y[:train_size]

# 모델 생성
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(time_steps, len(features))))
model.add(LSTM(50, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(25))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')

# 모델 학습
model.fit(X_train, y_train, batch_size=1, epochs=50)

# 2024년 데이터 예측
future_weather_data = pd.read_csv('datasets/Training/Weather/weather_tokyo_2024.csv')  # 예시 파일

# 날짜 형식 변환
future_weather_data['Date'] = pd.to_datetime(future_weather_data['Date'])

# NaN 및 Infinite 값 확인 및 처리
future_weather_data.replace([np.inf, -np.inf], np.nan, inplace=True)
future_weather_data.dropna(inplace=True)

# 스케일링
future_weather_data[features] = feature_scaler.transform(future_weather_data[features])

# 데이터셋 생성
future_X, _ = create_dataset(future_weather_data, features, target, time_steps)

# 예측
future_predict = model.predict(future_X)
future_predict = target_scaler.inverse_transform(future_predict)

# 예측 결과 시각화
plt.figure(figsize=(14, 5))
plt.plot(future_weather_data['Date'][time_steps:], future_predict, label='Future Predict')
plt.xlabel('Date')
plt.ylabel('Electricity Consumption (GWh)')
plt.title('Predicted Electricity Consumption for 2024')
plt.legend()
plt.show()
