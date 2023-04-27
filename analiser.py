import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

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
    plt.xscale('log')
    plt.yscale('log')
    plt.title(title)
    plt.savefig(f'figs/{title}.png')
    plt.show()

for m in metrics:
    title = f'{m} X state'
    groups = df.groupby(['state'])
    grupo1 = groups.get_group('MERGED')[m]
    grupo2 = groups.get_group('CLOSED')[m]

    t_stat, p_valor = ttest_ind(grupo1, grupo2)
    medians = groups[m].median()
    sns.boxplot(
        data=df,
        y=m,
        x='state',
        width=0.8,
        linewidth=1.0,
    )
    # plt.xscale('log')
    plt.yscale('log')
    for i, val in enumerate(medians.values[::-1]):
        plt.text(i,
                 val,
                 f'{val:.2f}',
                 horizontalalignment='center',
                 fontweight='bold')
    plt.title(title + f'\nT-stat: {t_stat:.2f} | P-value: {p_valor:.3f}')
    plt.savefig(f'figs/{title}.png')
    plt.show()
    


cols = ['tamanho', 'interacoes', 'descricao', 'tempo', 'reviews']
corr = df[cols].corr('spearman')

corr = corr.drop('tamanho')
corr = corr.drop('interacoes')
corr = corr.drop('descricao')
corr = corr.drop('tempo')
corr.pop('reviews')

print(corr)
sns.heatmap(data=corr, annot=True, square=True, robust=False)
plt.title('Heatmap correlação reviews')
plt.savefig('figs/heatmap.png')
plt.show()

