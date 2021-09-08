# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 01:27:30 2021

@author: michalm
"""
from fitness import calculate_fitness
from reproduction import *
from selection import select_by_roulette_wheel, select_by_random
from setup import *


samples = initialize_sample("a + (c * b)")
population = initialize_population()

for generation in range(max_number_of_cycles):
    calculate_fitness(population, samples)
    if min(population['fitness']) == 0:
        break
    population = select_by_roulette_wheel(population, debug=True)
    # population = select_by_random(population)
    print([str(i) + " " + str(ind.program.replace('data.', '')) for i, ind in population.iterrows()])
    reproduction(population, debug=True)


print(generation, population.sort_values('fitness').iloc[0].fitness, population.sort_values('fitness').iloc[0].program.replace('data.', ''))

