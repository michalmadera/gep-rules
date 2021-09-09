import numpy as np

from genome import genome_to_program
from setup import data_size


def __fitness_m(program, data):
    return np.mean(abs(data.y - eval(program)))


def __fitness_rse(program, data):
    # Fitness function: relative mean squared error
    guess = eval(program)
    error = sum([pow((guess[i] - data.y[i]) / data.y[i], 2) for i in range(len(data.y))])
    return 1000 * (1 / (1 + (error / data_size)))


def calculate_fitness(population, data):
    population['program'] = population.apply(lambda x: genome_to_program(x.genome), axis=1)
    population['fitness'] = population.apply(lambda x: __fitness_rse(x.program, data), axis=1)
