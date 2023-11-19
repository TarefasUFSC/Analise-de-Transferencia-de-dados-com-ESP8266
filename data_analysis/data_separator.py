import pandas as pd
import numpy as np

# cols: Distancia_m,QTD_Paredes,INT_WIFI,INT_WIFI-Mesmo_Canal,INT_WIFI-Proximo,INT_BT,INT_BT-Proximo,INT_MICROONDAS,INT_MICROONDAS-Proximo,INT_FURADEIRA,INT_FURADEIRA-Proximo


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
    ("0m_Bluetooth")
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

        print(f"Filtrando {column} = {value}")
        print(df_filtered.head())

    # salva em um arquivo csv
    df_filtered.to_csv("filtered/" + config + ".csv", index=False)