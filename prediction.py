import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

elec_path = "datasets/Training/Elec/Seoul.xlsx"
population_path = "datasets/Training/Population/SeoulPop.xlsx"

elec_data = pd.read_excel(elec_path)
population_data = pd.read_excel(population_path)

population_data = population_data.iloc[1:].reset_index(drop=True)
columns = ['District'] + [f'2021-{i:02d}' for i in range(1, 13)] + [f'2022-{i:02d}' for i in range(1, 13)] + [f'2023-{i:02d}' for i in range(1, 13)]
population_data.columns = columns
population_data['District'] = population_data['District'].str.strip()
population_data['City'] = '서울특별시'
population_data = population_data.melt(id_vars=['City', 'District'], var_name='Month', value_name='Population')
population_data['Year'] = population_data['Month'].apply(lambda x: int(x.split('-')[0]))
population_data['Month'] = population_data['Month'].apply(lambda x: int(x.split('-')[1]))

elec_data.columns = ['City', 'District', 'Usage_Type'] + [f'2021-{i:02d}' for i in range(1, 13)] + [f'2022-{i:02d}' for i in range(1, 13)] + [f'2023-{i:02d}' for i in range(1, 13)]
elec_data = elec_data.melt(id_vars=['City', 'District', 'Usage_Type'], var_name='Month', value_name='Power_Usage')
elec_data['Year'] = elec_data['Month'].apply(lambda x: int(x.split('-')[0]))
elec_data['Month'] = elec_data['Month'].apply(lambda x: int(x.split('-')[1]))

# 데이터 결합
merged_data = pd.merge(elec_data, population_data, on=['City', 'District', 'Year', 'Month'])

# 특성 및 라벨 선택
X = merged_data[['Year', 'Month', 'District', 'Usage_Type', 'Population']]
y = merged_data['Power_Usage']

# 범주형 변수를 숫자로 변환 (예: 'District', 'Usage_Type')
X = pd.get_dummies(X, columns=['District', 'Usage_Type'])

# 데이터 스케일링 (정규화)
scaler_X = StandardScaler()
scaler_y = StandardScaler()
X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1))

# 모델 로드
model = load_model('trained_model.h5')

# 2024년 1월부터 12월까지의 데이터를 예측하기 위한 입력 데이터 생성
future_months = [(2024, i) for i in range(1, 13)]
usage_types = merged_data['Usage_Type'].unique()
districts = merged_data['District'].unique()

# 미래 데이터를 담을 리스트
future_data = []

for year, month in future_months:
    for district in districts:
        for usage_type in usage_types:
            population = population_data[(population_data['District'] == district) & (population_data['Year'] == 2023) & (population_data['Month'] == 12)]['Population'].values[0]
            future_data.append([year, month, district, usage_type, population])

# 데이터프레임으로 변환
future_df = pd.DataFrame(future_data, columns=['Year', 'Month', 'District', 'Usage_Type', 'Population'])

# 원래의 'District' 및 'Usage_Type' 열을 유지
original_columns = future_df[['Year', 'Month', 'District', 'Usage_Type']].copy()

# 범주형 변수를 숫자로 변환
future_df = pd.get_dummies(future_df, columns=['District', 'Usage_Type'])
future_df = future_df.reindex(columns=X.columns, fill_value=0)

# 데이터 스케일링
future_df_scaled = scaler_X.transform(future_df)

# 예측
batch_size = 64
future_predictions = model.predict(future_df_scaled, batch_size=batch_size)

# 예측 결과를 원래 데이터프레임에 추가
future_predictions_rescaled = scaler_y.inverse_transform(future_predictions)

original_columns['Predicted_Power_Usage'] = future_predictions_rescaled

# 결과를 구별 및 용도별로 정리하여 출력
pivot_table = original_columns.pivot_table(index=['District', 'Usage_Type'], columns='Month', values='Predicted_Power_Usage')

# 열 이름 변경
pivot_table.columns = [f'2024-{month:02d}' for month in pivot_table.columns]

print(pivot_table)

# 결과를 엑셀 파일로 저장 (선택 사항)
pivot_table.to_excel("predicted_final_2024.xlsx")