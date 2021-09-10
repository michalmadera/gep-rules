import pandas as pd
import numpy as np

terms = ['a', 'b', 'c']
functions = ['*', '+']

head_size = 20
tail_size = head_size * len(terms) + 1

population_size = 10
max_number_of_cycles = 100

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

# d = initialize_sample_file("((a * b) + (c * d) * e)", ["a", "b", "c", "d", "e"], 100_000)
# d.to_csv("data/sample_5.csv", index=False, columns=["a", "b", "c", "d", "e", "y"])

# d = initialize_sample_file("((a * b) + (c * d) + (e * f))", ["a", "b", "c", "d", "e", "f"], 100_000)
# d.to_csv("data/sample_6.csv", index=False, columns=["a", "b", "c", "d", "e", "f", "y"])

# d = initialize_sample_file("((a * b) + (c * d * g) + (e * f))", ["a", "b", "c", "d", "e", "f", "g"], 100_000)
# d.to_csv("data/sample_7.csv", index=False, columns=["a", "b", "c", "d", "e", "f", "g", "y"])

# d = initialize_sample_file("(a + (b * c) + ((d * e) * f) + (g * h))", ["a", "b", "c", "d", "e", "f", "g", "h"], 100_000)
# d.to_csv("data/sample_8.csv", index=False, columns=["a", "b", "c", "d", "e", "f", "g", "h", "y"])

# d = initialize_sample_file("(a + (b * c) + ((d * e) * f) + (g * h) * i)", ["a", "b", "c", "d", "e", "f", "g", "h", "i"], 100_000)
# d.to_csv("data/sample_9.csv", index=False, columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "y"])

# d = initialize_sample_file("(a + (b * c) + ((d * e) * f) + (g * h) + (i * j))", ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"], 100_000)
# d.to_csv("data/sample_10.csv", index=False, columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "y"])
