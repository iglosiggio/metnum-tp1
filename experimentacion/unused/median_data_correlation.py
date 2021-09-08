#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def read_from(filepath):
    """ Read a list of teams from a file """
    with open(filepath, 'r') as file:
        return [float(team_elo) for team_elo in file.readlines()]

if __name__ == '__main__':

    methods = ['wp', 'elo', 'cmm', 'justice']
    names = ['shuffled-round-robin', 'shuffled-single-elimination']

    for name in names:
        medians = [read_from('experimentacion/experimental-data/players.txt')]
        for method in methods:
            matrix_result = []
            for i in range(100):
                matrix_result.append(read_from(f'experimentacion/experimental-data/{name}-{i}.{method}'))
            M = np.array(matrix_result, float)

            median_vector = []
            for j in range(len(medians[0])):
                median_vector.append(np.median(M[:,j]))

            medians.append(median_vector)

        for m in range(len(methods)):
            for i in range(len(medians)):
                corr = np.corrcoef(medians[m+1], medians[i])
                
                otro = 'Elo por default'
                if i != 0: otro = methods[i-1]
                corr = str(corr).replace("\n","")
                print(f'En {name} la correlacion entre {methods[m]} y {otro} es de : {corr}')