import pandas as pd

df_nao_filtrado = pd.read_csv('dados-pr.csv')

# Converter datas de string para datetime
df_nao_filtrado['created_at'] = pd.to_datetime(df_nao_filtrado['created_at'])
df_nao_filtrado['closed_at'] = pd.to_datetime(df_nao_filtrado['closed_at'])

df_filtrado = pd.DataFrame()

for i, row in df_nao_filtrado.iterrows():
    print(i, end='\r')
    tempo = (row['closed_at'] - row['created_at']).total_seconds()
    if row['reviews'] >= 1 and tempo >= 3600:
        df_filtrado = pd.concat([df_filtrado, row.to_frame().T])

print(len(df_filtrado))
df_filtrado.to_csv('dados-pr-filtrado.csv', index=False)
