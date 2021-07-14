import numpy as np

from genome import genome_to_program
from setup import functions


def fitness_function(program, data):
    return np.mean(abs(data.y - eval(program)))


def calculate_fitness(population, data):
    population['program'] = population.apply(lambda x: genome_to_program(x.genome, functions), axis=1)
    population['fitness'] = population.apply(lambda x: fitness_function(x.program, data), axis=1)
