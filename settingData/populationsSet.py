import pandas as pd

# 엑셀 파일 경로 설정
elec_2021 = "datasets/Training/Population/2021.xlsx"
elec_2022 = "datasets/Training/Population/2022.xlsx"
elec_2023 = "datasets/Training/Population/2023.xlsx"

# 데이터 로드
data_2021 = pd.read_excel(elec_2021)
data_2022 = pd.read_excel(elec_2022)
data_2023 = pd.read_excel(elec_2023)

# 데이터 확인
print("2021 Data")
print(data_2021.head())

print("\n2022 Data")
print(data_2022.head())

print("\n2023 Data")
print(data_2023.head())

# 데이터 결합
data_2021['Year'] = 2021
data_2022['Year'] = 2022
data_2023['Year'] = 2023

combined_data = pd.concat([data_2021, data_2022, data_2023])

# 시군구별 전력 사용량 분석
grouped_data = combined_data.groupby(['Year', '행정구역(시군구)별']).sum().reset_index()

# 결과 출력
print("\nCombined Data")
print(combined_data.head())

print("\nGrouped Data")
print(grouped_data.head())
