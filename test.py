import json
import pandas as pd
import glob

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

# data 파일에서 city값에서 뒤의 한글자를 제거하는 함수
def preprocess_city_name(city_name):
    return city_name[:-1]

# 날씨 데이터 로드
weather_df = load_weather_json_files("weather/weather_*.json")

# 전력 사용량 데이터 로드
power_df = load_power_data("data_*.json")

# 전력 사용량 데이터에서 city 값 전처리
power_df['city'] = power_df['city'].apply(preprocess_city_name)

# 데이터 병합
matched_data = []

for _, weather_row in weather_df.iterrows():
    for _, power_row in power_df.iterrows():
        if (weather_row['year'] == power_row['year'] and 
            weather_row['month'] == power_row['month'] and 
            weather_row['stnko'] in power_row['city']):
            
            matched_record = {
                'year': weather_row['year'],
                'month': weather_row['month'],
                'stnid': weather_row['stnid'],
                'stnko': weather_row['stnko'],
                'pa': weather_row['pa'],
                'avgtamax': weather_row['avgtamax'],
                'avgtamin': weather_row['avgtamin'],
                'taavg': weather_row['taavg'],
                'avghm': weather_row['avghm'],
                'biz': power_row['biz'],
                'powerUsage': power_row['powerUsage']
            }
            matched_data.append(matched_record)

df = pd.DataFrame(matched_data)

# 2016년부터 2023년까지의 데이터 필터링
df = df[(df['year'] >= 2016) & (df['year'] <= 2023)]

# 필요한 컬럼만 선택
df = df[['year', 'month', 'stnid', 'stnko', 'pa', 'avgtamax', 'avgtamin', 'taavg', 'avghm', 'biz', 'powerUsage']]

# 데이터 확인
print(df.head())

# 데이터 저장 (선택적으로 사용)
df.to_csv('merged_data_2016_2023.csv', index=False, encoding='utf-8')

# 모델 학습
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# 범주형 데이터 인코딩 (업종)
label_encoder = LabelEncoder()
df['biz'] = label_encoder.fit_transform(df['biz'])

# 특징 및 레이블 설정
X = df[['year', 'month', 'stnid', 'pa', 'avgtamax', 'avgtamin', 'taavg', 'avghm', 'biz']]
y = df['powerUsage']

# 학습 및 테스트 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 데이터 스케일링
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 모델 정의
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(32, activation='relu'),
    Dense(1)  # 출력 레이어
])

# 모델 컴파일
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# 모델 학습
history = model.fit(X_train, y_train, epochs=100, validation_split=0.2, batch_size=32)

# 모델 평가
loss, mae = model.evaluate(X_test, y_test)
print(f'Mean Absolute Error: {mae}')

# 예측 수행
y_pred = model.predict(X_test)

# 예측 결과와 실제 값 비교
results = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred.flatten()})
print(results.head())

# 예측 결과와 실제 값 비교 그래프
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(y_test.values, label='Actual')
plt.plot(y_pred, label='Predicted')
plt.legend()
plt.show()

# 학습 과정 시각화
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend()
plt.show()
