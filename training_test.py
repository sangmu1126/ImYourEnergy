import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# 파일 로드 함수
def load_data(year):
    with open(f'weather_{year}.json', 'r') as weather_file:
        weather_data = json.load(weather_file)['data']
    with open(f'data_{year}.json', 'r') as power_file:
        power_data = json.load(power_file)['data']
    return weather_data, power_data

# 2015년부터 2023년까지 데이터 로드 및 병합
weather_data_all = []
power_data_all = []

for year in range(2015, 2024):
    weather_data, power_data = load_data(year)
    weather_data_all.extend(weather_data)
    power_data_all.extend(power_data)

# 데이터프레임으로 변환
weather_df = pd.DataFrame(weather_data_all)
power_df = pd.DataFrame(power_data_all)

# 공통 키(예: 날짜와 위치)로 데이터 병합
# 여기서는 가정된 키로 병합합니다. 실제 키로 변경해야 할 수 있습니다.
merged_df = pd.merge(weather_df, power_df, on=['date', 'location'])

# 필요한 특성 선택
features = ['pa', 'ps', 'avgtamax', 'avgtamin', 'taavg', 'tamax', 'tamin', 'avgtgmin', 'ta', 'tmmax', 'tmmin', 'maxcnt', 'mincnt', 'avghm', 'avgcatot', 'sumssday', 'avgte05', 'daydur']
target = 'powerUsage'

X = merged_df[features]
y = merged_df[target]

# 결측값 처리
X = X.fillna(X.mean())

# 데이터 정규화
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 학습 데이터와 테스트 데이터로 분리
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 모델 정의
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(32, activation='relu'),
    Dense(1)
])

# 모델 컴파일
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# 모델 학습
history = model.fit(X_train, y_train, epochs=50, validation_split=0.2, batch_size=32)

# 모델 평가
loss, mae = model.evaluate(X_test, y_test)
print(f'테스트 데이터에서의 평균 절대 오차(MAE): {mae}')

# 모델 저장
model.save('power_usage_prediction_model.h5')
