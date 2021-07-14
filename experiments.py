# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 01:27:30 2021

@author: michalm
"""
from fitness import calculate_fitness
from reproduction import *
from selection import select_by_roulette_wheel
from setup import *


samples = initialize_sample("a + (a * b)")
population = initialize_population()

for generation in range(max_number_of_populations):
    calculate_fitness(population, samples)
    if min(population['fitness']) == 0:
        break
    population = select_by_roulette_wheel(population)
    reproduction(population)


print(generation, population.sort_values('fitness').iloc[0].fitness, population.sort_values('fitness').iloc[0].program.replace('data.', ''))

