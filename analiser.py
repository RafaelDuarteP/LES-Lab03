import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('dados-pr-filtrado.csv')

#Trocar closed e merged por 1 ou 0 para fazer os testes de correlação
df['status'] = df['state'].replace(['MERGED', 'CLOSED'], [1, 0])

#Mudar o tipo das datas
df['created_at'] = pd.to_datetime(df['created_at'])
df['closed_at'] = pd.to_datetime(df['closed_at'])

#Calcular o tempo de vida em horas
df['tempo'] = (df['closed_at'] - df['created_at']).dt.total_seconds() / 3600

metrics = ['tamanho', 'interacoes', 'descricao', 'tempo']
for m in metrics:
    title = f'{m} X reviews'
    sns.pairplot(data=df, y_vars='reviews', x_vars=m, kind="reg", height=10)
    plt.title(title)
    plt.savefig(f'figs/{title}.png')
    plt.show()

for m in metrics:
    title = f'{m} X state'
    medians = df.groupby(['state'])[m].median()
    sns.boxplot(
        data=df,
        y=m,
        x='state',
        width=0.8,
        linewidth=1.0,
        showfliers=False,
    )
    for i, val in enumerate(medians.values[::-1]):
        plt.text(i,
                 val,
                 f'{val:.2f}',
                 horizontalalignment='center',
                 fontweight='bold')
    plt.title(title)
    plt.savefig(f'figs/{title}.png')
    plt.show()

cols = ['tamanho', 'interacoes', 'descricao', 'tempo', 'reviews', 'status']
corr = df[cols].corr('spearman')

corr = corr.drop('tamanho')
corr = corr.drop('interacoes')
corr = corr.drop('descricao')
corr = corr.drop('tempo')
corr.pop('reviews')
corr.pop('status')

print(corr)
sns.heatmap(data=corr, annot=True, square=True, robust=False)
plt.title('Heatmap correlação')
plt.savefig('figs/heatmap.png')
plt.show()