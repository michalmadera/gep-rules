import pandas as pd
import numpy as np

import setup
from experiments import experiment


def initialize_sample_file(formula, terms, data_size):
    data = pd.DataFrame()
    for term in terms:
        data[term] = np.random.rand(data_size)
        formula = formula.replace(term, 'data.' + term).replace('data.data.', 'data.')

    data['y'] = eval(formula)
    return data


# d = initialize_sample_file("((a * b) + (c * d))", ["a", "b", "c", "d"], 100_000)
# d.to_csv("data/sample_4.csv", index=False, columns=["a", "b", "c", "d", "y"])

# d = initialize_sample_file("(a + (b * c) + ((d * e) * f) + (g * h))", ["a", "b", "c", "d", "e", "f", "g", "h"], 100000)
# d.to_csv("data/sample_8.csv", index=False, columns=["a", "b", "c", "d", "e", "f", "g", "h", "y"])

def scenario(file, size):
    data = pd.read_csv(file, nrows=size)
    setup.data_size = size
    setup.terms = data.columns[:-1]

    experiment(data)


scenario('data/sample_4.csv', 100)


