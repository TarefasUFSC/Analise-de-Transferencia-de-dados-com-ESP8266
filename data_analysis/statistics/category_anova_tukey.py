import os
import pandas as pd
import numpy as np
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Diretório com os dados
data_dir = './data'

# Listando os arquivos CSV no diretório
file_paths = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith('.csv')]

# Carregando os dados
data = {file_path.split('/')[-1].replace('.csv', ''): pd.read_csv(file_path) for file_path in file_paths}

# ANOVA
# Preparando dados para o ANOVA
anova_data = {name: df['Tempo_ms'] for name, df in data.items()}
# Realizando o teste ANOVA
anova_result = f_oneway(*anova_data.values())

# Salvando os resultados do ANOVA
anova_results_df = pd.DataFrame([anova_result], columns=['F-statistic', 'p-value'])
anova_results_df.to_csv('anova_results.csv', index=False)

# Calculando os tempos médios de transmissão
mean_times = {name: df['Tempo_ms'].mean() for name, df in data.items()}
mean_times_df = pd.DataFrame(list(mean_times.items()), columns=['Interference_Type', 'Mean_Transmission_Time'])
mean_times_df.to_csv('mean_transmission_times.csv', index=False)

# Tukey
# Preparando dados para o Tukey
tukey_data = pd.DataFrame(columns=['Tempo_ms', 'Interference_Type'])
for name, df in data.items():
    temp_df = pd.DataFrame()
    temp_df['Tempo_ms'] = df['Tempo_ms']
    temp_df['Interference_Type'] = name
    tukey_data = pd.concat([tukey_data, temp_df])

# Realizando o teste Tukey
tukey_result = pairwise_tukeyhsd(endog=tukey_data['Tempo_ms'], groups=tukey_data['Interference_Type'], alpha=0.05)

# Salvando os resultados do Tukey
tukey_results_df = pd.DataFrame(data=tukey_result._results_table.data[1:], columns=tukey_result._results_table.data[0])
tukey_results_df.to_csv('tukey_results.csv', index=False)

# Salvando os dados usados no Tukey
tukey_data.to_csv('tukey_data.csv', index=False)


def analisar_tukey_significativos(csv_path, p_valor_limite=0.05):
    # Carregar os dados
    tukey_results = pd.read_csv(csv_path)

    # Filtrar resultados significativos
    resultados_significativos = tukey_results[(tukey_results['reject']) & (tukey_results['p-adj'] < p_valor_limite)]

    # Inicializar uma string para armazenar a análise
    analysis_text = ""

    # Verificar se há resultados significativos
    if resultados_significativos.empty:
        analysis_text = "Nenhuma diferença estatisticamente significativa encontrada."
    else:
        # Analisar cada linha dos resultados significativos
        for index, row in resultados_significativos.iterrows():
            group1 = row['group1']
            group2 = row['group2']
            meandiff = row['meandiff']
            p_adj = row['p-adj']
            lower = row['lower']
            upper = row['upper']

            analysis_text += f"Comparação: {group1} vs {group2}\n"
            analysis_text += f"Diferença Média: {meandiff}\n"
            analysis_text += f"Intervalo de Confiança: [{lower}, {upper}]\n"
            analysis_text += f"P-valor Ajustado: {p_adj}\n"
            analysis_text += "Esta diferença é estatisticamente significativa.\n"
            analysis_text += "-" * 50 + "\n"

    # Salvar a análise em um arquivo de texto
    with open('tukey_analysis_significativos.txt', 'w') as file:
        file.write(analysis_text)

    return 'Análise salva em tukey_analysis_significativos.txt'


# Chamar a função para analisar os resultados e salvar a análise
analisar_tukey_significativos("tukey_results.csv")
