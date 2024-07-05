import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
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
elec_data['Month'] =elec_data['Month'].apply(lambda x: int(x.split('-')[1]))

merged_data = pd.merge(elec_data, population_data, on=['City', 'District', 'Year', 'Month'])

print(merged_data)





