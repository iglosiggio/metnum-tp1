#!/usr/bin/env python3

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def read_ranking(filepath):
    with open(filepath, encoding='utf8') as file:
        return [float(v) for v in file.readlines()]

def plot_comparison(test_name):
    plt.clf()
    base = read_ranking('experimental-data/players.txt')
    if 'fifa' in test_name:
        base = base[:32]
    rankings = {
        'Elo Base': base,
        'CMM': read_ranking(f'{test_name}.cmm'),
        'WP': read_ranking(f'{test_name}.wp'),
        'Justice': read_ranking(f'{test_name}.justice'),
        'Elo': read_ranking(f'{test_name}.elo')
    }
    df = pd.DataFrame(rankings)
    g = sns.PairGrid(data=df, x_vars=['CMM', 'WP', 'Justice', 'Elo'], y_vars=['Elo Base'])
    g.map(sns.scatterplot)
    return g

#plot_comparison('big-round-robin')
#plot_comparison('big-fifa')

# Scatterplot mostrando la similaridad entre el Elo base y el inferido por los métodos
plot_comparison('experimental-results-f64/shuffled-single-elimination-3').savefig('shuffled_single_3.pdf')
plot_comparison('experimental-results-f64/shuffled-round-robin-42').savefig('shuffled_round_robin_42.pdf')
plot_comparison('big-tournaments/big-shuffled-single').savefig('big_shuffled_single.pdf')
plot_comparison('big-tournaments/big-same-single').savefig('big_same_single.pdf')
