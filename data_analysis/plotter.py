import pandas as pd
import os

#importa o plotly para fazer os graficos
import plotly.graph_objects as go

# importa cada um dos csv que estão na pasta filtered e coloca eles em uma lista [df,nome_aquivo]

# lista de arquivos
files = os.listdir("filtered")
# lista de dataframes
dfs = []
# lista de nomes
names = []
for file in files:
    df = pd.read_csv("filtered/" + file)
    dfs.append(df)
    names.append(file)
baseline_name = "0m-Sem_Interferência.csv"
baseline_index = names.index(baseline_name)
df_baseline = dfs[baseline_index]
dfs.pop(baseline_index)
names.pop(baseline_index)

print("Baseline: " + baseline_name)

# faz um grafico comparando o baseline com cada um dos outros (2 linhas por grafico)
# salva o grafico em um png na pasta graphs com o nome do arquivo sendo o nome do arquivo do baseline + o nome do arquivo do comparado

for df, name in zip(dfs, names):
    # cria um grafico com uma linha sendo o baseline e outra sendo o comparado
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df_baseline["Tempo_ms"], x=df_baseline["QTD_Bytes"], name=baseline_name))
    fig.add_trace(go.Scatter(y=df["Tempo_ms"], x=df["QTD_Bytes"], name=name))
    fig.update_layout(title_text="Comparação entre " + baseline_name + " e " + name)
    fig.write_image("graphs/" + baseline_name.split('.')[0] + "X" + name.split('.')[0] + ".png")
    print("Comparação entre " + baseline_name.split('.')[0] + " e " + name + " salva em graphs/" + baseline_name + "_" + name + ".png")

# faz uma regressão linear para cada um dos outros arquivos comparando com o baseline (com regressão linear)
# salva o grafico em um png na pasta graphs com o nome do arquivo sendo o nome do arquivo do baseline + o nome do arquivo do comparado + _regressao

# regressões
from sklearn.linear_model import LinearRegression
import numpy as np

x_baseline = np.array(df_baseline["QTD_Bytes"]).reshape((-1, 1))
y_baseline = np.array(df_baseline["Tempo_ms"])
model_baseline = LinearRegression().fit(x_baseline, y_baseline)
r_sq_baseline = model_baseline.score(x_baseline, y_baseline)
print('Baseline')
print('coefficient of determination:', r_sq_baseline)
print('intercept:', model_baseline.intercept_)
print('slope:', model_baseline.coef_)
print()

for df, name in zip(dfs, names):
    # calcula cada uma das regressões
    x = np.array(df["QTD_Bytes"]).reshape((-1, 1))
    y = np.array(df["Tempo_ms"])
    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)
    print(name)
    print('coefficient of determination:', r_sq)
    print('intercept:', model.intercept_)
    print('slope:', model.coef_)
    print()
    # cria um grafico com uma linha sendo o baseline e outra sendo o comparado
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=model_baseline.predict(x_baseline), x=df_baseline["QTD_Bytes"], name="Regressão " + baseline_name))
    fig.add_trace(go.Scatter(y=model.predict(x), x=df["QTD_Bytes"], name="Regressão " + name))
    fig.update_layout(title_text="Comparação entre " + baseline_name + " e " + name)
    fig.write_image("graphs/regressao/" + baseline_name.split('.')[0] + "X" + name.split('.')[0] + "_regressao.png")
    print("Comparação entre " + baseline_name.split('.')[0] + " e " + name.split('.')[0] + " salva em graphs/" + baseline_name.split('.')[0] + "_" + name.split('.')[0] + "_regressao.png")
