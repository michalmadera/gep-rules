import pandas as pd
import numpy as np
import time

import setup
from experiments import experiment


def scenario(file, size, tensor=True):
    data = pd.read_csv(file, nrows=size)
    setup.data_size = size
    setup.terms = data.columns[:-1]
    t1 = time.time()
    generations = experiment(data, tensor)
    duration = time.time() - t1
    return duration, generations


def run_experiment(tensor=True):
    results = pd.DataFrame()
    cols_exp = [5, 10, 15, 20]
    rows_exp = [100, 2500, 5000, 7500, 10_000]

    i = 0
    for ncols in cols_exp:
        print(ncols)
        for nrows in rows_exp:
            print(nrows)
            for ret in range(5):
                duration, generations = scenario('data/sample_' + str(ncols) + '.csv', nrows, tensor)
                results = results.append({'i': ret, 'nrows': nrows, 'ncols': ncols, 'generations': generations,
                                          'duration': duration}, ignore_index=True)
                i = i + 1
                print('run', duration, generations, i, '/', len(cols_exp) * len(rows_exp) * 5)

    if tensor:
        results.to_excel('result/experiment_results_tensor_f1.xlsx')
    else:
        results.to_excel('result/experiment_results_f1.xlsx')

    
run_experiment(False)
run_experiment(True)

