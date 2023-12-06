import os
import pandas as pd
import numpy as np
from scipy.stats import f_oneway
from scipy.stats import kruskal
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import scikit_posthocs as sp
from pprint import pprint

import scipy.stats as stats
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


# Kruskal-Wallis Test
# Preparando dados para o teste Kruskal-Wallis
kruskal_data = [df['Tempo_ms'] for df in data.values()]
# Realizando o teste Kruskal-Wallis
kruskal_result = kruskal(*kruskal_data)

# Salvando os resultados do Kruskal-Wallis
kruskal_results_df = pd.DataFrame([kruskal_result], columns=['Statistic', 'p-value'])
kruskal_results_df.to_csv('kruskal_results.csv', index=False)



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


def dunn_test(data_dict):
    # Concatena todos os dados e cria os rótulos de grupo
    all_data = np.concatenate(list(data_dict.values()))
    labels = np.array([k for k, v in data_dict.items() for _ in range(len(v))])

    # Realiza o teste Kruskal-Wallis
    kruskal_result = stats.kruskal(*data_dict.values())
    print("Kruskal-Wallis Test:")
    print(f"Statistic: {kruskal_result.statistic}, p-value: {kruskal_result.pvalue}")

    if kruskal_result.pvalue >= 0.05:
        print("Não há diferenças significativas.")
        return

    # Realiza comparações entre pares de grupos
    df_results = pd.DataFrame()
    name1= []
    name2 = []
    z_stats = []
    p_vals = []
    group_keys = list(data_dict.keys())
    for i in range(len(group_keys)):
        for j in range(i+1, len(group_keys)):
            group1 = data_dict[group_keys[i]]
            group2 = data_dict[group_keys[j]]

            # Calcula a estatística de teste e o valor-p
            z_stat, p_val = stats.ranksums(group1, group2)
            p_val_adjusted = p_val * len(group_keys)  # Ajuste Bonferroni
            # print(f"Comparação {group_keys[i]} vs {group_keys[j]}: Z={z_stat}, p={p_val_adjusted}")
            if(p_val_adjusted < 0.05):
                # print(f"Comparação {group_keys[i]} vs {group_keys[j]}: Z={z_stat}, p={p_val_adjusted}"
                z_stats.append(z_stat)
                p_vals.append(p_val_adjusted)
                name1.append(group_keys[i])
                name2.append(group_keys[j])
    df_results['Group 1'] = name1
    df_results['Group VS'] = name2
    df_results['z_stat'] = z_stats
    df_results['p_val'] = p_vals
    df_results.to_csv('dunn_results.csv', index=False)


data_dict = {}
for name, df in data.items():
    #coloca a lo tempo ms como float
    # dropa os nulos
    data_dict[name] = df['Tempo_ms'].astype(float).tolist()
    for v in data_dict[name]:
        if v == 0:
            data_dict[name].remove(v)
    print(len(data_dict[name]))
# pprint(data_dict)
dunn_result = dunn_test(data_dict)
# print(dunn_result)





# Chamar a função para analisar os resultados e salvar a análise
analisar_tukey_significativos("tukey_results.csv")

