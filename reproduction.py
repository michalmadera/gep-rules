import pandas as pd
import numpy as np

from setup import *


def reproduction(population):
    __point_mutation(population)
    __is_transposition(population)
    __ris_transposition(population)
    __one_point_recombination(population)
    __two_point_recombination(population)


def __replication(population):
    return population.copy()


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
            size = np.random.randint(1, head_size - 1)
            index_of_copying = np.random.randint(0, head_size + tail_size - size)
            index_of_inserting = np.random.randint(1, head_size - size)

            genome = individual['genome']
            insertion_seq = genome[index_of_copying:index_of_copying + size]
            individual['genome'] = genome[:index_of_inserting] + insertion_seq + genome[index_of_inserting+size:head_size] + genome[head_size:]
            # print("===" + str(index_of_copying) + "=" + str(size) + "=" + str(index_of_inserting))
            # print(genome)
            # print(insertion_seq)
            # print(individual.genome)


def __ris_transposition(population, t_rate=0.1):
    for _, individual in population.iterrows():
        if np.random.random() < t_rate:
            size = np.random.randint(1, head_size - 1)
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


def __one_point_recombination(population, prob_crossover=0.85):
    for _ in range(np.random.randint(0, population_size / 2)):
        if np.random.random() < prob_crossover:
            rows = np.random.choice(population_size, 2, False)
            crossover_point = np.random.randint(0, head_size + tail_size)

            genomes = [population.iloc[i, population.columns.get_loc('genome')] for i in rows]
            population.iloc[rows[0], population.columns.get_loc('genome')] = genomes[0][:crossover_point] + genomes[1][crossover_point:]
            population.iloc[rows[1], population.columns.get_loc('genome')] = genomes[1][:crossover_point] + genomes[0][crossover_point:]


def __two_point_recombination(population, prob_crossover=0.85):
    for _ in range(np.random.randint(0, population_size / 2)):
        if np.random.random() < prob_crossover:
            rows = np.random.choice(population_size, 2, False)
            crossover_point_0 = np.random.randint(0, head_size + tail_size)
            crossover_point_1 = np.random.randint(crossover_point_0, head_size + tail_size)

            genomes = [population.iloc[i, population.columns.get_loc('genome')] for i in rows]
            population.iloc[rows[0], population.columns.get_loc('genome')] = \
                genomes[0][:crossover_point_0] + genomes[1][crossover_point_0:crossover_point_1] + genomes[0][crossover_point_1:]
            population.iloc[rows[1], population.columns.get_loc('genome')] = \
                genomes[1][:crossover_point_0] + genomes[0][crossover_point_0:crossover_point_1] + genomes[1][crossover_point_1:]
