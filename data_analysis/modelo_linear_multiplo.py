import os
import pandas as pd
import statsmodels.api as sm

# Carregar variáveis
vars_df = pd.read_csv('vars_sep.csv')
variables = vars_df['Variaveis'].tolist()
# remove as variaveis com a palavra dist
variables = [var for var in variables if 'dist' not in var]
# remove a Sem_Interferência
# variables.remove('Sem_Interferência')

# Caminho para a pasta com os dados
data_dir = './filtered_data'

# Carregar e processar dados
sel_type = 'MeanTime'
all_data = []
for file in os.listdir(data_dir):
    if file.endswith('.csv'):
        file_path = os.path.join(data_dir, file)
        df = pd.read_csv(file_path)
        df_filtered = df[df['Tempo_ms'] <= 9088]  # Filtrar Tempo_mss

        df_type_data = {
            "MinTime": df_filtered['Tempo_ms'].min(),
            "MaxTime": df_filtered['Tempo_ms'].max(),
            "MeanTime": df_filtered['Tempo_ms'].mean()
        }

        df_mean = df_filtered['Tempo_ms'].mean()  # Calcular média do Tempo_ms
        df_max = df_filtered['Tempo_ms'].max()
        df_min = df_filtered['Tempo_ms'].min()
        colunas = df.columns.tolist()
        #pega os valores das colunas com os nomes das variaveis para fazer a analise
        data_row = {var: df_filtered[var].tolist()[0] for var in variables}
        
        # Adiciona os valores de MinTime, MaxTime e MeanTime
        data_row[sel_type] = df_type_data[sel_type]

        all_data.append(data_row)

# Consolidar dados
data = pd.DataFrame(all_data)
# print(data)

# Preparação dos dados para o modelo
X = data.drop(sel_type, axis=1)
y = data[sel_type]

# Adicionando o intercepto
X = sm.add_constant(X)

# Ajuste do Modelo
model = sm.OLS(y, X).fit()

# Exibir e salvar resultados
print(model.summary())
with open(f'model_results_{sel_type}.txt', 'w') as f:
    f.write(model.summary().as_text())
