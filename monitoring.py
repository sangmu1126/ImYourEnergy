import requests
import urllib.parse
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout


url = "https://openapi.kpx.or.kr/openapi/sukub5mMaxDatetime/getSukub5mMaxDatetime"
params = {
    "ServiceKey": "NpWQYBWBernbIhRAeWWRQx+Amef+hy8m+HDpfVbjbQzjZga2mjyJXKpn7C86fmyy4AaS0UlbG4BE8CPZnp+AvA=="
}

response = requests.get(url, params=params)

# 응답 상태 코드 확인
if response.status_code == 200:
    try:
        data = response.json()
    except ValueError:
        print("응답이 JSON 형식이 아닙니다. 원시 응답 내용:")
        print(response.text)
else:
    print(f"응답 상태 코드: {response.status_code}")
    print("원시 응답 내용:")
    print(response.text)
    data = None

# 데이터가 유효한 경우에만 처리
if data:
    df = pd.DataFrame(data['response']['body']['items']['item'])

    # 데이터프레임 변환 및 전처리
    df['baseDatetime'] = pd.to_datetime(df['baseDatetime'], format='%Y%m%d%H%M%S')
    df.set_index('baseDatetime', inplace=True)
    df = df[['currPwrTot', 'forecastLoad', 'suppAbility', 'suppReservePwr', 'suppReserveRate', 'operReservePwr', 'operReserveRate']]

    # 시각화
    df.plot(subplots=True, figsize=(10, 12))
    plt.show()

    # 데이터 준비
    sequence_length = 60  # 예측에 사용할 타임 스텝 수
    X = []
    y = []

    for i in range(len(df) - sequence_length):
        X.append(df.iloc[i:i+sequence_length].values)
        y.append(df.iloc[i+sequence_length]['currPwrTot'])

    X = np.array(X)
    y = np.array(y)

    # 데이터 스케일링
    scaler_X = MinMaxScaler()
    scaler_y = MinMaxScaler()

    X_scaled = scaler_X.fit_transform(X.reshape(-1, X.shape[-1])).reshape(X.shape)
    y_scaled = scaler_y.fit_transform(y.reshape(-1, 1))

    # 데이터 셔플 및 분할
    shuffle_index = np.random.permutation(len(X_scaled))
    X_scaled = X_scaled[shuffle_index]
    y_scaled = y_scaled[shuffle_index]

    split = int(0.8 * len(X_scaled))
    X_train, X_test = X_scaled[:split], X_scaled[split:]
    y_train, y_test = y_scaled[:split], y_scaled[split:]

    # LSTM 모델 구축
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(sequence_length, X.shape[2])),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')

    # 모델 학습
    model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.2)

    # 예측
    predictions = model.predict(X_test)
    predictions = scaler_y.inverse_transform(predictions)  # 스케일링 복원
    y_test = scaler_y.inverse_transform(y_test)  # 스케일링 복원

    # 예측 결과 시각화
    plt.figure(figsize=(14, 5))
    plt.plot(y_test, color='blue', label='Actual Power Demand')
    plt.plot(predictions, color='red', label='Predicted Power Demand')
    plt.title('Power Demand Prediction')
    plt.xlabel('Time')
    plt.ylabel('Power Demand (MW)')
    plt.legend()
    plt.show()
