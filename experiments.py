# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 01:27:30 2021

@author: michalm
"""

import pandas as pd
import numpy as np
import time


def random_genome(head_size, tile_size, terms, functions):
    s = list()
    for _ in range(head_size):
        selection = functions if np.random.random() < 0.5 else terms
        s.append(selection[np.random.randint(0, len(selection))])
    for _ in range(tail_size):
        s.append(terms[np.random.randint(0, len(terms))])
    return ''.join(s)


def genome_to_tree(genome, functions):
    off = 0
    queue = list()
    root = {'node': genome[off]}
    off += 1
    queue.append(root)
    while len(queue) > 0:
        current = queue.pop(0)
        if current['node'] in functions:
            current['left'] = {'node': genome[off]}
            off += 1
            queue.append(current['left'])
            current['right'] = {'node': genome[off]}
            off += 1
            queue.append(current['right'])
    return root


def tree_to_program(tree):
    prefix = 'data.'
    if 'left' not in tree or 'right' not in tree:
        return prefix + tree['node']
    left = prefix + tree_to_program(tree['left'])
    right_value = tree_to_program(tree['right'])
    right = prefix + right_value
    tree = '({0} {1} {2})'.format(left, tree['node'], right)
    return tree


def crossover(parent1, parent2, prob_crossover):
    child = parent1
    if np.random.random() < prob_crossover:
        child = ''.join([a if np.random.random() < 0.5 else b for a, b in zip(parent1, parent2)])
    return child


def point_mutation(genome):
    rate = 1.0 / len(genome)
    child = list()
    for i in range(len(genome)):
        bit = genome[i]
        if np.random.random() < rate:
            if i < head_size:
                selection = functions if np.random.random() < 0.5 else terms
                bit = selection[np.random.randint(0, len(selection))]
            else:
                bit = terms[np.random.randint(0, len(terms))]
            print(bit)
        child.append(bit)
    return ''.join(child)


def genome_to_program(genome, functions):
    return tree_to_program(genome_to_tree(genome, functions)).replace('data.(', '(').replace('data.data.', 'data.')


def fitness_function(expected_values, program):
    return np.mean(abs(expected_values - eval(program)))

                   
data_size = 100
data = pd.DataFrame({'a': np.random.rand(data_size), 'b': np.random.rand(data_size)})
data['y'] = data.a + (data.b * data.a)

terms = ['a', 'b']
functions = ['*', '+']
head_size = 10
tail_size = head_size * len(terms) + 1
population_size = 10

number_of_generations = 10

population = pd.DataFrame([random_genome(head_size, tail_size, terms, functions) for _ in range(population_size)], columns=['genome'])
population['program'] = population.apply(lambda x: genome_to_program(x['genome'], functions), axis=1)
population['fitness'] = population.apply(lambda x: fitness_function(data.y, x.program), axis=1)
for _ in range(number_of_generations):
    # selected = binary_tournamen -> wybieraj 2 osobniki losowo i zwracaj lepszy. tyle raz ile osobników. rodzaj selekcji inny niz ruletka
    random_selection = np.random.randint(0, population_size, population_size)
    selected = population.apply(lambda x: (
        x if x.fitness < population.iloc[random_selection[x.name]].fitness 
        else population.iloc[random_selection[x.name]]), axis=1)
    
    # children = reporuction -> wybierz pary co drugi i zrob krzyzowanie z mutacja punktowa
    # wybierz pary
    random_selection = np.random.randint(0, population_size, population_size)
    # corssover
    crossed = selected.copy()
    crossed.genome = selected.apply(lambda x: crossover(x.genome, 
                                                        selected.iloc[random_selection[x.name]].genome, 0.85), axis=1)
    crossed['fitness'] = crossed.apply(lambda x: fitness_function(data.y, x.program), axis=1)

    population = population.append(crossed, ignore_index=True).sort_values('fitness')[:population_size]
    population.index = range(0,len(population))
    
    print(population[['fitness', 'program']])
    # krzyzowanie stosuj tylko w 85% przypadków, a dla 15% zwracaj rodzica pierwszego
    # krzyzowanie powinno wybierać losowe znaki z jednego lub drugiego rodzica
    # mutacja punktowa przeprowadzana jest po krzyzowaniu
    # wybranie najlepszego osobnika i jeżeli fitness jest = 0 zakończyć algorytm
    # zebrać na jednej liscie rodzicow i dzieci, posortowac po fitness, wybrac pierwsze osobniki (do ilosci z populacji)
    # jezeli liczba generacji nie zostala przekroczona kontynuowac kolejne pokolenie
