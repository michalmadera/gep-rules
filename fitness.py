import numpy as np
import pandas as pd
import tensorflow as tf

from genome import genome_to_program
from setup import data_size


def __fitness_m(program, data):
    return np.mean(abs(data.y - eval(program)))


def __fitness_rse(program, data):
    # Fitness function: relative mean squared error
    guess = eval(program)
    error = sum([pow((guess[i] - data.y[i]) / data.y[i], 2) for i in range(len(data.y))])
    return 1000 * (1 / (1 + (error / data_size)))


def __fitness_rse_tensor(program, d):
    # Fitness function: relative mean squared error
    data = dict()
    for col in d.columns:
        data[str(col)] = tf.constant(d[col].values)
        program = program.replace("data." + col, "data['" + col + "']")

    guess = eval(program)
    error = tf.math.square((guess - data['y']) / data['y'])
    error = tf.math.reduce_sum(error)
    return 1000 * (1 / (1 + (error / data_size)))


def calculate_fitness(population, data, tensor=True):
    population['program'] = population.apply(lambda x: genome_to_program(x.genome), axis=1)
    if tensor:
        population['fitness'] = population.apply(lambda x: __fitness_rse_tensor(x.program, data), axis=1)
    else:
        population['fitness'] = population.apply(lambda x: __fitness_rse(x.program, data), axis=1)
