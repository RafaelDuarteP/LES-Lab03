import pandas as pd

lista_dados = []

for i in range(1, 24):
    dados_pr = pd.read_csv(f'dados-pr-{i}.csv')
    dados_pr = dados_pr.drop_duplicates(subset=['id'])
    lista_dados.append(dados_pr)

dados_concatenados = pd.concat(lista_dados)
print(len(dados_concatenados))
dados_concatenados.to_csv('dados-pr.csv', index=False)
