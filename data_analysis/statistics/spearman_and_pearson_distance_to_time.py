import os
import pandas as pd
from scipy.stats import spearmanr, pearsonr
import numpy as np
import re

def extrair_distancia(nome_arquivo):
    match = re.search(r'(\d+)m', nome_arquivo)
    return int(match.group(1)) if match else 0

def calcular_correlacoes_e_salvar(data_dir, output_csv):
    file_paths = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith('.csv')]
    correlacoes = []

    for file_path in file_paths:
        data = pd.read_csv(file_path)
        distancia = extrair_distancia(file_path)
        data['Distancia'] = distancia
        categoria = file_path.split('/')[-1].replace('.csv', '')

        #  para cada categoria, calcula a correlação de spearman e pearson no Tempo_ms e Distancia
        spearman = spearmanr(data['Tempo_ms'], data['Distancia'])
        
    correlacoes_df = pd.DataFrame(correlacoes, columns=['Categoria', 'Correlação Pearson', 'P-valor Pearson', 'Correlação Spearman', 'P-valor Spearman'])
    correlacoes_df.to_csv(output_csv, index=False)

    return f'Análise salva em {output_csv}'

# Diretório com os dados e arquivo de saída
data_dir = './data'
output_csv = 'correlacoes_speaman_and_pearson_distance_to_time.csv'

# Executando a função
calcular_correlacoes_e_salvar(data_dir, output_csv)
