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
    # cols_exp = [3, 4, 5, 6, 7, 8, 9, 10]
    # rows_exp = [100, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    cols_exp = [4, 7, 10]
    rows_exp = [100, 500, 1000, 5000, 10_000]

    i = 0
    for ncols in cols_exp:
        for nrows in rows_exp:
            for ret in range(5):
                duration, generations = scenario('data/sample_' + str(ncols) + '.csv', nrows, tensor)
                results = results.append({'i': ret, 'nrows': nrows, 'ncols': ncols, 'generations': generations,
                                          'duration': duration}, ignore_index=True)
                i = i + 1
                print('run', duration, generations, i, '/', len(cols_exp) * len(rows_exp) * 5)
        print(nrows)

    if tensor:
        results.to_excel('result/experiment_results_tensor_f.xlsx')
    else:
        results.to_excel('result/experiment_results_f.xlsx')

    
run_experiment(False)
run_experiment(True)

