#!/usr/bin/env python3
""" Histograma sobre la correlación de spearman en distintos tipos de torneo
"""

import seaborn as sns
import pandas as pd

with open('correlations.txt', encoding='utf8') as file:
    correlations = pd.DataFrame([
        (test[:test.rfind('-')], test[test.rfind('.')+1:], float(value))
        for value, test in (line.replace('\n', '').split(' ')
                     for line
                     in file.readlines())
    ], columns=['Test Name', 'Method', 'Correlation'])
g = sns.displot(correlations, x='Correlation', col='Test Name', hue='Method',
                fill=False, element='step', common_bins=False,
                col_wrap=3, facet_kws=dict(sharex=False, sharey=False))
g.set_axis_labels('Correlación de Spearman', '#valores en el rango')
g.savefig('all_correlations.pdf')
