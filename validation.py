# validation.py

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

# 엑셀 파일 로드
pop_file_path = "datasets/Training/Population/pop_seoul_2024.xlsx"
elec_file_path = "datasets/Training/Elec/elec_seoul_2024.xlsx"

# 인구 데이터 로드
population_data = pd.read_excel(pop_file_path)
elec_data = pd.read_excel(elec_file_path)

# 인구 데이터 전처리
# pop_data.columns = ['District', '2024-01', '2024-02', '2024-03']
# pop_data = pop_data.melt(id_vars=['District'], var_name='Month', value_name='Population')
# pop_data['Year'] = pop_data['Month'].apply(lambda x: int(x.split('-')[0]))
# pop_data['Month'] = pop_data['Month'].apply(lambda x: int(x.split('-')[1]))

population_data = population_data.iloc[1:].reset_index(drop=True)
columns = ['District', '2024-01', '2024-02', '2024-03']
population_data.columns = columns
population_data['District'] = population_data['District'].str.strip()
population_data['City'] = '서울특별시'
population_data = population_data.melt(id_vars=['City', 'District'], var_name='Month', value_name='Population')
population_data['Year'] = population_data['Month'].apply(lambda x: int(x.split('-')[0]))
population_data['Month'] = population_data['Month'].apply(lambda x: int(x.split('-')[1]))

# 전력 사용량 데이터 전처리
elec_data.columns = ['City', 'District', 'Usage_Type', '2024-01', '2024-02', '2024-03']
elec_data = elec_data.melt(id_vars=['City', 'District', 'Usage_Type'], var_name='Month', value_name='Power_Usage')
elec_data['Year'] = elec_data['Month'].apply(lambda x: int(x.split('-')[0]))
elec_data['Month'] = elec_data['Month'].apply(lambda x: int(x.split('-')[1]))

# 데이터 결합
validation_data = pd.merge(elec_data, population_data, on=['City', 'District', 'Year', 'Month'])

# 특성 및 라벨 선택
X_val = validation_data[['Year', 'Month', 'District', 'Usage_Type', 'Population']]
y_val = validation_data['Power_Usage']

# 범주형 변수를 숫자로 변환 (예: 'District', 'Usage_Type')
X_val = pd.get_dummies(X_val, columns=['District', 'Usage_Type'])

# 데이터 스케일링 (훈련 시 사용한 스케일러 사용)
scaler_X = StandardScaler()
scaler_y = StandardScaler()
X_val_scaled = scaler_X.fit_transform(X_val)
y_val_scaled = scaler_y.fit_transform(y_val.values.reshape(-1, 1))

# 모델 로드
model = load_model('trained_model.h5')

# 예측 수행
y_pred_scaled = model.predict(X_val_scaled)

# 예측 결과를 원래 스케일로 변환
y_pred = scaler_y.inverse_transform(y_pred_scaled)

# 결과 데이터프레임 생성
validation_data['Predicted_Power_Usage'] = y_pred

# 비교 결과 출력
print(validation_data[['City', 'District', 'Year', 'Month', 'Usage_Type', 'Power_Usage', 'Predicted_Power_Usage']])

# 예측 결과를 엑셀 파일로 저장 (선택 사항)
validation_data.to_excel("validation_results.xlsx", index=False)
