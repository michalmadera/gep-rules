# -*- coding: utf-8 -*-
import setup
from fitness import calculate_fitness
from reproduction import *
from selection import select_by_roulette_wheel
from setup import *


def experiment(samples):
    population = initialize_population()
    setup.data_size = samples.size

    for generation in range(max_number_of_cycles):
        calculate_fitness(population, samples)
        if max(population.fitness) >= 1000 or generation == max_number_of_cycles - 1:
            break
        population = select_by_roulette_wheel(population, debug=False)
        population = reproduction(population, debug=False)

    best = population.sort_values('fitness').iloc[len(population) - 1]
    print(generation, int(best.fitness), best.program.replace('data.', ''))


# experiment(initialize_sample("c + (a * b)"))

