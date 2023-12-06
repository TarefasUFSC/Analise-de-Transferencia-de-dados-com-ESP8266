import pandas as pd
import numpy as np

# cols: Distancia_m,QTD_Paredes,INT_WIFI,INT_WIFI-Mesmo_Canal,INT_WIFI-Proximo,INT_BT,INT_BT-Proximo,INT_MICROONDAS,INT_MICROONDAS-Proximo,INT_FURADEIRA,INT_FURADEIRA-Proximo

# TO DO: Usar o chat GPT para gerar uma analise estatistica para ver a influencia de cada intereferencia
#  é mais forte (gerou mais interferecnia) e qual é a menor (menor interferencia)

df = pd.read_csv("data.csv")
# Configurações específicas fornecidas pelo usuário

specified_configs = [
    ("0m-wifi_same_server"),
    ("0m-wifi_diff_server"),
    ("0m-wifi_diff_server+bl_client"),
    ("0m-wifi_same_server+bl_client"),
    ("1m-wifi_same_server"),
    ("0m-Sem_Interferência"),
    ("1m-Sem_Interferência"),
    ("5m-Sem_Interferência"),
    ("1m-wifi_diff_server+bl_server"),
    ("0m-wifi_same_client+1_parede"),
    ("0m-wifi_diff_client+1_parede"),
    ("0m-wifi_same_client+cem_client"),
    ("0m-wifi_diff_client+cem_client"),
    ("0m-wifi_same_client+microondas_client"),
    ("0m-wifi_diff_client+microondas_client"),
    ("0m-bluetooth_client")
]


# faz um df_configs dropando as colunas QTD_Bytes  | Tempo_ms      
df_configs = df.drop(columns=["QTD_Bytes", "Tempo_ms"])

# faz um merge das celulas que forem iguais e só deixa linhas unicas
df_configs = df_configs.drop_duplicates()


# adiciona uma coluna de nomes
df_configs["Nome"] = specified_configs


# salva em um arquivo csv
df_configs.to_csv("configs.csv", index=False)

# para cada tipo de configuração, cria um novo csv com os dados dessa configuração específica
def get_config_vars(config):
    v_sep = []
    v_sep.append("dist_" + config.split('-')[0])
    for v in config.split('-')[1].split('+'):
        v_sep.append(v)
    return v_sep

vars_sep = []
for config in specified_configs:
    for v in get_config_vars(config):
        vars_sep.append(v)
    # print(vars_sep)
# filtra o varsep só pra ter valores unicos
vars_sep = list(set(vars_sep))
print(vars_sep)

for config in specified_configs:
    df_config_filtered = df_configs[df_configs["Nome"] == config]
    df_config_no_name = df_config_filtered.drop(columns=["Nome"])
    
    # Colunas e valores para filtro
    column_filters = df_config_no_name.columns
    column_filter_values = df_config_no_name.iloc[0]

    # Cria um novo DataFrame para os valores filtrados
    df_filtered = df.copy()

    for column, value in zip(column_filters, column_filter_values):
        # Se o valor para filtrar é NaN, use pd.isna para a comparação
        if pd.isna(value):
            df_filtered = df_filtered[pd.isna(df_filtered[column])]
        else:
            df_filtered = df_filtered[df_filtered[column] == value]

        # print(f"Filtrando {column} = {value}")
        # print(df_filtered.head())

    # cria uma coluna de 1s e 0s para preencher com os valores de interferencia
    this_dt_vars = get_config_vars(config)
    for var in vars_sep:
        if var in this_dt_vars:
            df_filtered[var] = np.ones(len(df_filtered))
        else:
            df_filtered[var] = np.zeros(len(df_filtered))
   
    
    # salva em um arquivo csv
    df_filtered.to_csv("filtered_data/" + config + ".csv", index=False)

# salva num csv as variaveis separadas
df_vars_sep = pd.DataFrame()
df_vars_sep["Variaveis"] = vars_sep
df_vars_sep.to_csv("vars_sep.csv", index=False)

