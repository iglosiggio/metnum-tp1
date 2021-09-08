#!/usr/bin/env python3
""" Gráfico sobre cuán bueno puede ser el ranking para cada cantidad de
    victorias
"""

import seaborn as sns
import pandas as pd

df = pd.read_csv('naive-opt.txt')
df = df[[
    '#Wins',
    'Best CMM Ranking',
    'Best WP Ranking',
    'Best Justice Ranking',
    'Best Elo Ranking'
]].melt(id_vars=['#Wins'])
g = sns.lineplot(data=df, x='#Wins', y='value', hue='variable')
g.set_ylabel('Mejor ranking encontrado')
g.get_figure().savefig('strategic_wins.pdf')
