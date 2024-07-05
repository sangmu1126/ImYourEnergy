import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping
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

print(population_data.head())

elec_data.columns = ['City', 'District', 'Usage_Type'] + [f'2021-{i:02d}' for i in range(1, 13)] + [f'2022-{i:02d}' for i in range(1, 13)] + [f'2023-{i:02d}' for i in range(1, 13)]
elec_data = elec_data.melt(id_vars=['City', 'District', 'Usage_Type'], var_name='Month', value_name='Power_Usage')
elec_data['Year'] = elec_data['Month'].apply(lambda x: int(x.split('-')[0]))
elec_data['Month'] = elec_data['Month'].apply(lambda x: int(x.split('-')[1]))

print(elec_data.head())

merged_data = pd.merge(elec_data, population_data, on=['City', 'District', 'Year', 'Month'])

print(merged_data.head())

merged_data.replace([np.inf, -np.inf], np.nan, inplace=True)
merged_data.dropna(inplace=True)

print(merged_data.describe())

X = merged_data[['Year', 'Month', 'District', 'Usage_Type', 'Population']]
y = merged_data['Power_Usage']

X = pd.get_dummies(X, columns=['District', 'Usage_Type'])

scaler_X = StandardScaler()
scaler_y = StandardScaler()
X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1))

print("X_scaled:", X_scaled[:5])
print("y_scaled:", y_scaled[:5])

model = Sequential([
    Dense(64, activation='relu', input_shape=(X_scaled.shape[1],)),
    Dense(32, activation='relu'),
    Dense(1) 
])

optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)

model.compile(optimizer=optimizer, loss='mean_squared_error')

early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

batch_size = 64
model.fit(X_scaled, y_scaled, epochs=200, batch_size=batch_size, validation_split=0.2, callbacks=[early_stopping])

loss = model.evaluate(X_scaled, y_scaled, batch_size=batch_size)
print(f"Loss: {loss}")

future_months = [(2024, i) for i in range(1, 13)]
usage_types = merged_data['Usage_Type'].unique()
districts = merged_data['District'].unique()

future_data = []

for year, month in future_months:
    for district in districts:
        for usage_type in usage_types:
            population = population_data[(population_data['District'] == district) & (population_data['Year'] == 2023) & (population_data['Month'] == 12)]['Population'].values[0]
            future_data.append([year, month, district, usage_type, population])

future_df = pd.DataFrame(future_data, columns=['Year', 'Month', 'District', 'Usage_Type', 'Population'])

original_columns = future_df[['Year', 'Month', 'District', 'Usage_Type']].copy()

future_df = pd.get_dummies(future_df, columns=['District', 'Usage_Type'])
future_df = future_df.reindex(columns=X.columns, fill_value=0)

future_df_scaled = scaler_X.transform(future_df)

batch_size = 64
future_predictions = model.predict(future_df_scaled, batch_size=batch_size)

future_predictions_rescaled = scaler_y.inverse_transform(future_predictions)

original_columns['Predicted_Power_Usage'] = future_predictions_rescaled

pivot_table = original_columns.pivot_table(index=['District', 'Usage_Type'], columns='Month', values='Predicted_Power_Usage')

pivot_table.columns = [f'2024-{month:02d}' for month in pivot_table.columns]

print(pivot_table)

pivot_table.to_excel("predicted_2024.xlsx")
