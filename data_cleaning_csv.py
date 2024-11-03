import pandas as pd

# Cargar los datasets originales
df_completed_requests = pd.read_csv('C:/Users/natal/OneDrive/Escritorio/Canadian Pr/datasets/completed_access_to_information_requests.csv')
df_contracts = pd.read_csv('C:/Users/natal/OneDrive/Escritorio/Canadian Pr/datasets/contracts_with_dates_corrected.csv')

# Paso 1: Extraer 'year' y 'month' del campo 'contract_date' en df_contracts
# Asegúrate de que 'contract_date' esté en formato datetime
df_contracts['contract_date'] = pd.to_datetime(df_contracts['contract_date'], errors='coerce')

# Crear nuevas columnas 'year' y 'month' basadas en 'contract_date'
df_contracts['year'] = df_contracts['contract_date'].dt.year
df_contracts['month'] = df_contracts['contract_date'].dt.month

# Verificar las nuevas columnas de fecha
print("Primeros registros de contratos con fechas extraídas:")
print(df_contracts[['contract_date', 'year', 'month']].head())

# Paso 2: Realizar el merge completo
df_all = pd.merge(df_completed_requests, df_contracts, on=['owner_org'], how='outer', indicator=True)

# Realizar el merge para obtener solo aquellos que coinciden (both)
df_both = df_all[df_all['_merge'] == 'both']

# Reviso los registros de cada tipo después del merge
print(f"Registros 'left_only': {df_all[df_all['_merge'] == 'left_only'].shape[0]}")
print(f"Registros 'right_only': {df_all[df_all['_merge'] == 'right_only'].shape[0]}")
print(f"Registros 'both': {df_both.shape[0]}")

# Guardar los nuevos merges corregidos
df_all.to_csv('C:/Users/natal/OneDrive/Escritorio/Canadian Pr/datasets/combined_data_all_corrected.csv', index=False)
df_both.to_csv('C:/Users/natal/OneDrive/Escritorio/Canadian Pr/datasets/combined_data_both_corrected.csv', index=False)


