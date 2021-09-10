import pandas as pd
import numpy as np
import time

import setup
from experiments import experiment


def scenario(file, size):
    data = pd.read_csv(file, nrows=size)
    setup.data_size = size
    setup.terms = data.columns[:-1]
    t1 = time.time()
    generations = experiment(data)
    duration = time.time() - t1
    return duration, generations


def run_experiment():
    results = pd.DataFrame()
    cols_exp = [3, 4, 5, 6, 7, 8, 9, 10]
    rows_exp = [100, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    # cols_exp = [3, 4]
    # rows_exp = [100, 200]

    i = 0
    for ncols in cols_exp:
        for nrows in rows_exp:
            duration, generations = scenario('data/sample_' + str(ncols) + '.csv', nrows)
            results = results.append({'nrows': nrows, 'ncols': ncols, 'generations': generations,
                                      'duration': duration}, ignore_index=True)
            i = i + 1
            print('run', duration, i)

    results.to_excel('experiment_results_tensor.xlsx')

    
run_experiment()

