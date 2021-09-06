import pandas as pd
import numpy as np

from setup import *


def reproduction(population):
    population = __replication(population)
    __point_mutation(population)
    __is_transposition(population)
    __ris_transposition(population)
    __one_point_recombination(population)
    __two_point_recombination(population)


def __replication(population):
    return population[['genome']].copy()


def __point_mutation(population):
    rate = 1.0 / (head_size + tail_size)
    for _, individual in population.iterrows():
        genome = individual['genome']
        new_genome = list()
        for i in range(len(genome)):
            bit = genome[i]
            if np.random.random() < rate:
                if i < head_size:
                    selection = functions if np.random.random() < 0.5 else terms
                    bit = selection[np.random.randint(0, len(selection))]
                else:
                    bit = terms[np.random.randint(0, len(terms))]
            new_genome.append(bit)
        individual['genome'] = ''.join(new_genome)


def __is_transposition(population, t_rate=0.1):
    for _, individual in population.iterrows():
        if np.random.random() < t_rate:
            size = np.random.randint(1, 3)
            index_of_copying = np.random.randint(0, head_size + tail_size - size)
            index_of_inserting = np.random.randint(1, head_size - size)

            genome = individual.genome
            insertion_seq = genome[index_of_copying:index_of_copying + size]
            individual.genome = genome[:index_of_inserting] + insertion_seq + genome[index_of_inserting+size:head_size] + genome[head_size:]
            # print("===" + str(index_of_copying) + "=" + str(size) + "=" + str(index_of_inserting))
            # print(genome)
            # print(insertion_seq)
            # print(individual.genome)


def __ris_transposition(population, t_rate=0.1):
    for _, individual in population.iterrows():
        if np.random.random() < t_rate:
            size = np.random.randint(1, 3)
            index_of_start_copying = np.random.randint(0, head_size)

            genome = individual.genome
            insertion_seq = ""
            for i, val in enumerate(genome[index_of_start_copying:]):
                if val in functions:
                    insertion_seq = genome[i + index_of_start_copying:i + index_of_start_copying + size]
                    break

            individual.genome = insertion_seq + genome[:head_size - len(insertion_seq)] + genome[head_size:]
            # print("===" + str(index_of_start_copying) + "=" + str(size))
            # print(genome)
            # print(insertion_seq)
            # print(individual.genome)


def __one_point_recombination(population, r_rate=0.3):
    for _, individual in population.iterrows():
        if np.random.random() < r_rate:
            sec_individual = np.random.choice(population_size, 1, False)[0]
            crossover_point = np.random.randint(0, head_size + tail_size)

            g_1 = individual.genome
            g_2 = population.iloc[sec_individual, population.columns.get_loc('genome')]
            individual.genome = g_1[:crossover_point] + g_2[crossover_point:]
            population.iloc[sec_individual, population.columns.get_loc('genome')] = g_2[:crossover_point] + g_1[crossover_point:]


def __two_point_recombination(population, r_rate=0.3):
    for _, individual in population.iterrows():
        if np.random.random() < r_rate:
            sec_individual = np.random.choice(population_size, 1, False)[0]
            point_0 = np.random.randint(0, head_size + tail_size)
            point_1 = np.random.randint(point_0, head_size + tail_size)

            g_1 = individual.genome
            g_2 = population.iloc[sec_individual, population.columns.get_loc('genome')]
            individual.genome = g_1[:point_0] + g_2[point_0:point_1] + g_1[point_1:]
            population.iloc[sec_individual, population.columns.get_loc('genome')] = g_2[:point_0] + g_1[point_0:point_1] + g_2[point_1:]
