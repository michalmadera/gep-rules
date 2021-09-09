import pandas as pd
import numpy as np

terms = ['a', 'b', 'c']
functions = ['*', '+']

head_size = 5
tail_size = head_size * len(terms) + 1

population_size = 10
max_number_of_cycles = 500

data_size = 100


def __random_genome():
    s = list()
    for _ in range(head_size):
        selection = functions if np.random.random() < 0.5 else terms
        s.append(selection[np.random.randint(0, len(selection))])
    for _ in range(tail_size):
        s.append(terms[np.random.randint(0, len(terms))])
    return ''.join(s)


def initialize_population():
    population_zero = [__random_genome() for _ in range(population_size)]
    return pd.DataFrame(population_zero, columns=['genome'])


def initialize_sample(formula):
    data = pd.DataFrame()
    for term in terms:
        data[term] = np.random.rand(data_size)
        formula = formula.replace(term, 'data.' + term)

    data['y'] = eval(formula)
    return data
