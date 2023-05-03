import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
from matplotlib.ticker import ScalarFormatter

df = pd.read_csv('dados-pr-filtrado.csv')

#Mudar o tipo das datas
df['created_at'] = pd.to_datetime(df['created_at'])
df['closed_at'] = pd.to_datetime(df['closed_at'])

#Calcular o tempo de vida em horas
df['tempo'] = (df['closed_at'] - df['created_at']).dt.total_seconds() / 3600

#Definir as dimensões analisadas
metrics = ['tamanho', 'interacoes', 'descricao', 'tempo']

# Scatterplots
for m in metrics:
    title = f'{m} X reviews'
    sns.pairplot(data=df, y_vars='reviews', x_vars=m, kind="reg", height=10)
    plt.title(title)
    plt.yscale('log')
    plt.savefig(f'figs/{title}.png')
    plt.show()

#Boxplots
for m in metrics:
    title = f'{m} X state'
    groups = df.groupby(['state'])
    grupo1 = groups.get_group('MERGED')[m]
    grupo2 = groups.get_group('CLOSED')[m]

    t_stat, p_valor = ttest_ind(grupo1, grupo2)
    medians = groups[m].median()
    q1_merged, q3_merged = grupo1.quantile([0.25, 0.75])
    q1_closed, q3_closed = grupo2.quantile([0.25, 0.75])

    sns.boxplot(
        data=df,
        y=m,
        x='state',
        width=0.8,
        linewidth=1.0,
    )

    plt.text(0, q1_merged, f'Q1={q1_merged:.2f}', horizontalalignment='left')
    plt.text(1, q1_closed, f'Q1={q1_closed:.2f}', horizontalalignment='left')
    plt.text(0, q3_merged, f'Q3={q3_merged:.2f}', horizontalalignment='left')
    plt.text(1, q3_closed, f'Q3={q3_closed:.2f}', horizontalalignment='left')
    for i, val in enumerate(medians.values[::-1]):
        plt.text(i,
                 val,
                 f'{val:.2f}',
                 horizontalalignment='center',
                 fontweight='bold')

    plt.title(title + f'\nT-stat: {t_stat:.2f} | P-value: {p_valor:.3f}')
    plt.yscale('log')
    plt.savefig(f'figs/{title}.png')
    plt.show()

#Heatmap de correlações
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
