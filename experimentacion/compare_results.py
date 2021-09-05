#!/usr/bin/env python3
"""
Ejecuta nuestra implementación de CMM y compara los resultados con los
ofrecidos por la cátedra
"""
import math
import os
import subprocess

TP_EXE = './tp.f64'
TEST_FOLDER = '../tests'
TEST_INPUT_EXT = '.in'
TEST_OUTPUT_EXT = '.expected'

def leer_tests_de_la_catedra():
    """ Leer los .expected ofrecidos por la cátedra """
    tests = {}

    for dirpath, _, files in os.walk(TEST_FOLDER):
        for filename in files:
            if filename.endswith(TEST_OUTPUT_EXT):
                filepath = os.path.join(dirpath, filename)
                test_name = filename[:-len(TEST_OUTPUT_EXT)]
                input_filepath = os.path.join(dirpath, test_name + TEST_INPUT_EXT)
                with open(filepath, 'r', encoding='utf8') as file:
                    tests[test_name] = (
                        input_filepath,
                        [float(line) for line in file.readlines()]
                    )

    return tests

TESTS = leer_tests_de_la_catedra()

def comparar_resultados(test_name):
    """ Toma el nombre de un test, y lo compara con nuestra implementación
        Retorna una 5-upla (avg-error, std-dev, min-error, max-error, diffs)
    """
    input_filepath, esperado = TESTS[test_name]
    nuestro = subprocess.run(
        [TP_EXE, input_filepath, '/dev/stdout', '0'],
        encoding='utf8',
        capture_output=True,
        check=True
    ).stdout
    nuestro = [float(line) for line in nuestro.split()]

    assert len(esperado) == len(nuestro)

    samples = len(esperado)

    diffs = [a - b for a, b in zip(esperado, nuestro)]
    absdiffs = [abs(v) for v in diffs]
    absdiffs_mean = sum(absdiffs) / samples
    absdiffs_var = sum((v - absdiffs_mean) ** 2 for v in absdiffs) \
                 / (samples - 1)
    absdiffs_stddev = math.sqrt(absdiffs_var)
    absdiffs_min = min(absdiffs)
    absdiffs_max = max(absdiffs)

    return (absdiffs_mean, absdiffs_stddev, absdiffs_min, absdiffs_max, diffs)

if __name__ == '__main__':
    all_diffs = []
    for test in TESTS:
        print(f'=== {test} ===')
        cmp = comparar_resultados(test)
        print(f'Error promedio:      {cmp[0]}')
        print(f'Desviación estándar: {cmp[1]}')
        print(f'Error más chico:     {cmp[2]}')
        print(f'Error más grande:    {cmp[3]}')
        all_diffs.extend(cmp[4])

    try:
        import matplotlib.pyplot as plt
        import seaborn as sns

        histplot = sns.histplot(data=all_diffs, bins=1024)
        histplot.set_ylabel('#valores en el rango')
        histplot.set_xlabel('cátedra - nuestro')
        histplot.get_figure().savefig('error_histogram.pdf')

        plt.show()
    except ModuleNotFoundError:
        print('!! Instale seaborn para ver los gráficos')
