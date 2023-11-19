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

regrs = []

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
    regressao = [name, model, r_sq]
    regrs.append(regressao)
    # cria um grafico com uma linha sendo o baseline e outra sendo o comparado
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=model_baseline.predict(x_baseline), x=df_baseline["QTD_Bytes"], name="Regressão " + baseline_name))
    fig.add_trace(go.Scatter(y=model.predict(x), x=df["QTD_Bytes"], name="Regressão " + name))
    fig.update_layout(title_text="Comparação entre " + baseline_name + " e " + name)
    fig.write_image("graphs/regressao/" + baseline_name.split('.')[0] + "X" + name.split('.')[0] + "_regressao.png")
    print("Comparação entre " + baseline_name.split('.')[0] + " e " + name.split('.')[0] + " salva em graphs/" + baseline_name.split('.')[0] + "_" + name.split('.')[0] + "_regressao.png")

# faz um grafico de linha de todas as regressões
# salva como regressions.png    
fig = go.Figure()
for regr in regrs:
    fig.add_trace(go.Scatter(y=regr[1].predict(x_baseline), x=df_baseline["QTD_Bytes"], name="Regressão " + regr[0]))
fig.update_layout(title_text="Regressões")
# deixa a imagem em 1080p e coloca a legenda embaixo
fig.update_layout(width=1920, height=1080, legend_orientation="h")
fig.write_image("graphs/regressao/regressions.png")
print("Regressões salvas em graphs/regressao/regressions.png")

# grafico de barras comparando o 128 de todos
# salva como 128.png
fig = go.Figure()
for df, name in zip(dfs, names):
    fig.add_trace(go.Bar(y=df[df["QTD_Bytes"] == 128]["Tempo_ms"], name=name))
fig.update_layout(title_text="Comparação entre todos os 128")
fig.write_image("graphs/128.png")


# procura o maior tamanho que é comum a todos os arquivos filtrados
max_size = 0

for df1 in dfs:
    # procura o maior tamanho que é comum a todos os arquivos filtrados linha por linha
    for index, row in df1.iterrows():
        # se o tamanho for maior que o max_size e o tamanho estiver em todos os outros arquivos
        if row["QTD_Bytes"] > max_size and all(df2[df2["QTD_Bytes"] == row["QTD_Bytes"]].shape[0] > 0 for df2 in dfs):
            max_size = row["QTD_Bytes"]


print("Maior tamanho comum a todos os arquivos: " + str(max_size))

# faz um grafico de barras comparando o maior tamanho comum a todos os arquivos
# salva como max_size.png
fig = go.Figure()
for df, name in zip(dfs, names):
    fig.add_trace(go.Bar(y=df[df["QTD_Bytes"] == max_size]["Tempo_ms"], name=name))
fig.update_layout(title_text="Comparação entre todos os " + str(max_size))
fig.write_image("graphs/" + str(max_size) + ".png")



    