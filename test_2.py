import json
import pandas as pd
import glob
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from scikeras.wrappers import KerasRegressor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# JSON 파일 로드 함수
def load_weather_json_files(pattern):
    files = glob.glob(pattern)
    data_list = []
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            year = int(file.split('_')[1])
            month = int(file.split('_')[2].split('.')[0])
            for record in data['data']:
                record['year'] = year
                record['month'] = month
                data_list.append(record)
    return pd.DataFrame(data_list)

# 전력 사용량 데이터 로드 함수
def load_power_data(pattern):
    files = glob.glob(pattern)
    data_list = []
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for record in data['data']:
                year = int(record['year'])
                month = int(record['month'])
                record['year'] = year
                record['month'] = month
                data_list.append(record)
    return pd.DataFrame(data_list)

# City 전처리 함수
def preprocess_city_name(city):
    return city[:-1]

# 데이터 로드
weather_df = load_weather_json_files("weather/weather_*.json")
power_df = load_power_data("data_*.json")

# 전력 사용량 데이터에서 city 값 전처리
power_df['city'] = power_df['city'].apply(preprocess_city_name)

# 데이터 병합 조건
merge_condition = lambda row: power_df[(power_df['year'] == row['year']) & 
                                       (power_df['month'] == row['month']) & 
                                       (power_df['city'] == row['stnko'])]

# 병합된 데이터를 저장할 리스트
merged_data = []

# 데이터 병합
for _, row in weather_df.iterrows():
    matching_rows = merge_condition(row)
    for _, match in matching_rows.iterrows():
        merged_record = {**row, **match}
        merged_data.append(merged_record)

# 최종 데이터프레임 생성
final_df = pd.DataFrame(merged_data)

# 필요한 컬럼만 선택
final_df = final_df[['year', 'month', 'stnid', 'stnko', 'pa', 'avgtamax', 'avgtamin', 'taavg', 'avghm', 'biz', 'powerUsage']]

# "null" 값을 NaN으로 변환 후 채우기
final_df.replace("null", np.nan, inplace=True)
final_df.fillna(0, inplace=True)

# 'biz' 열을 라벨 인코딩
label_encoder = LabelEncoder()
final_df['biz'] = label_encoder.fit_transform(final_df['biz'])

# 특징과 레이블 분리
X = final_df[['year', 'month', 'stnid', 'pa', 'avgtamax', 'avgtamin', 'taavg', 'avghm', 'biz']]
y = final_df['powerUsage']

# 학습용 데이터와 테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 데이터 스케일링
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 모델 정의
def create_model():
    model = Sequential()
    model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
    return model

# KerasRegressor 래퍼를 사용하여 모델 생성
model = KerasRegressor(model=create_model, epochs=100, batch_size=32, verbose=1)

# 모델 학습
model.fit(X_train, y_train, validation_data=(X_test, y_test))

# 모델 평가
loss, mae = model.score(X_test, y_test)
print(f"Mean Absolute Error: {mae}")

# 예측
predictions = model.predict(X_test)
