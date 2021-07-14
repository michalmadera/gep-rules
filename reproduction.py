import pandas as pd
import numpy as np

from setup import *


def reproduction(population):
    __point_mutation(population)
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


def __one_point_recombination(population, prob_crossover=0.85):
    for _ in range(np.random.randint(0, population_size / 2)):
        if np.random.random() < prob_crossover:
            rows = np.random.choice(population_size, 2)
            crossover_point = np.random.randint(0, head_size + tail_size)

            genomes = [population.iloc[i, population.columns.get_loc('genome')] for i in rows]
            population.iloc[rows[0], population.columns.get_loc('genome')] = genomes[0][:crossover_point] + genomes[1][crossover_point:]
            population.iloc[rows[1], population.columns.get_loc('genome')] = genomes[1][:crossover_point] + genomes[0][crossover_point:]


def __two_point_recombination(population, prob_crossover=0.85):
    for _ in range(np.random.randint(0, population_size / 2)):
        if np.random.random() < prob_crossover:
            rows = np.random.choice(population_size, 2)
            crossover_point_0 = np.random.randint(0, head_size + tail_size)
            crossover_point_1 = np.random.randint(crossover_point_0, head_size + tail_size)

            genomes = [population.iloc[i, population.columns.get_loc('genome')] for i in rows]
            population.iloc[rows[0], population.columns.get_loc('genome')] = \
                genomes[0][:crossover_point_0] + genomes[1][crossover_point_0:crossover_point_1] + genomes[0][crossover_point_1:]
            population.iloc[rows[1], population.columns.get_loc('genome')] = \
                genomes[1][:crossover_point_0] + genomes[0][crossover_point_0:crossover_point_1] + genomes[1][crossover_point_1:]
