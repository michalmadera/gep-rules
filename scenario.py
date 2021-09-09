import pandas as pd
import numpy as np
import time

import setup
from experiments import experiment


def initialize_sample_file(formula, terms, data_size):
    data = pd.DataFrame()
    for term in terms:
        data[term] = np.random.rand(data_size)
        formula = formula.replace(term, 'data.' + term).replace('data.data.', 'data.')

    data['y'] = eval(formula)
    return data


# d = initialize_sample_file("(a * b) + c", ["a", "b", "c"], 100_000)
# d.to_csv("data/sample_3.csv", index=False, columns=["a", "b", "c", "y"])

# d = initialize_sample_file("((a * b) + (c * d))", ["a", "b", "c", "d"], 100_000)
# d.to_csv("data/sample_4.csv", index=False, columns=["a", "b", "c", "d", "y"])

# d = initialize_sample_file("(a + (b * c) + ((d * e) * f) + (g * h))", ["a", "b", "c", "d", "e", "f", "g", "h"], 100000)
# d.to_csv("data/sample_8.csv", index=False, columns=["a", "b", "c", "d", "e", "f", "g", "h", "y"])

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
    # cols_exp = [3, 4, 5, 6, 7, 8, 9, 10]
    # rows_exp = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    cols_exp = [3, 4]
    rows_exp = [100, 200]
    
    for ncols in cols_exp:
        for nrows in rows_exp:
            for index in range(5):
                duration, generations = scenario('data/sample_' + str(ncols) + '.csv', nrows)
                results = results.append({'index':index, 'nrows':nrows, 
                                          'ncols':ncols, 'generations':generations, 
                                          'duration':duration}, 
                                         ignore_index=True)
                print('run', index, duration, results)

    results.to_excel('experiment_results.xlsx')

    
run_experiment()

