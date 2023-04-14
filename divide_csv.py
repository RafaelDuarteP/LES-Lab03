import pandas as pd

# Carrega o CSV em um DataFrame
df = pd.read_csv('lista-repo.csv')

# Ordena o DataFrame pelo valor de total_prs em ordem decrescente
df = df.sort_values('total_prs', ascending=True)

# Inicializa o primeiro grupo com o primeiro repositório do DataFrame
grupos = [[df.iloc[0]]]
total_prs_grupo = df.iloc[0]['total_prs']

# Itera sobre o DataFrame a partir do segundo repositório
for _, row in df.iloc[1:].iterrows():
    # Se a adição do repositório atual não ultrapassar o limite de 4000 total_prs no grupo atual
    if total_prs_grupo + row['total_prs'] <= 70000:
        # Adiciona o repositório ao grupo atual
        grupos[-1].append(row)
        total_prs_grupo += row['total_prs']
    else:
        # Inicia um novo grupo com o repositório atual
        grupos.append([row])
        total_prs_grupo = row['total_prs']

# Salva cada grupo em um arquivo CSV com um nome único
for i, grupo in enumerate(grupos):
    pd.DataFrame(grupo).to_csv(f'lista-repo-{i+1}.csv', index=False)
