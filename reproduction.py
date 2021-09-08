import pandas as pd
import numpy as np

from setup import *


def reproduction(population, debug=False):
    if debug:
        print(population)
    population = __replication(population)
    __point_mutation(population, debug=debug)
    __is_transposition(population, debug=debug)
    __ris_transposition(population, debug=debug)
    __one_point_recombination(population, debug=debug)
    __two_point_recombination(population, debug=debug)
    if debug:
        print(population)
        print("===")


def __replication(population):
    c = population[['genome']].copy()
    return c
    # return c.reset_index(drop=True)


def __point_mutation(population, m_rate=0.1, debug=False):
    for i, individual in population.iterrows():
        genome = individual['genome']
        new_genome = list()
        changed = list()
        for ind in range(len(genome)):
            bit = genome[ind]
            if np.random.random() < m_rate:
                if ind < head_size:
                    selection = functions if np.random.random() < 0.5 else terms
                    bit = selection[np.random.randint(0, len(selection))]
                else:
                    bit = terms[np.random.randint(0, len(terms))]
                changed.append(str(ind) + ": " + genome[ind] + "=>" + bit)
            new_genome.append(bit)
        population.iloc[i, population.columns.get_loc('genome')] = ''.join(new_genome)
        if debug and len(changed) > 0:
            print("pm:", str(i), changed, genome, population.iloc[i, population.columns.get_loc('genome')])


def __is_transposition(population, t_rate=0.1, debug=False):
    for i, individual in population.iterrows():
        if np.random.random() < t_rate:
            size = np.random.randint(1, 4)
            index_of_copying = np.random.randint(0, head_size + tail_size - size)
            index_of_inserting = np.random.randint(1, head_size - size)

            genome = individual.genome
            insertion_seq = genome[index_of_copying:index_of_copying + size]
            population.iloc[i, population.columns.get_loc('genome')] = \
                genome[:index_of_inserting] + insertion_seq + genome[index_of_inserting+size:head_size] + genome[head_size:]
            if debug:
                print("is:", str(i), str(index_of_copying), str(index_of_inserting), insertion_seq, genome,
                      population.iloc[i, population.columns.get_loc('genome')])


def __ris_transposition(population, t_rate=0.5, debug=False):
    for i, individual in population.iterrows():
        if np.random.random() < t_rate:
            size = np.random.randint(1, 4)
            index_of_start_copying = np.random.randint(0, head_size)

            genome = individual.genome
            insertion_seq = ""
            for ind, val in enumerate(genome[index_of_start_copying:]):
                if val in functions:
                    insertion_seq = genome[ind + index_of_start_copying:ind + index_of_start_copying + size]
                    break

            population.iloc[i, population.columns.get_loc('genome')] = \
                insertion_seq + genome[:head_size - len(insertion_seq)] + genome[head_size:]
            if debug:
                print("ris:", str(i), str(index_of_start_copying), insertion_seq, genome, population.iloc[i, population.columns.get_loc('genome')])


def __one_point_recombination(population, r_rate=0.3, debug=False):
    for i, individual in population.iterrows():
        if np.random.random() < r_rate:
            sec_individual = np.random.choice(population_size, 1, False)[0]
            crossover_point = np.random.randint(1, head_size + tail_size)

            g_0 = individual.genome
            g_1 = population.iloc[sec_individual, population.columns.get_loc('genome')]
            population.iloc[i, population.columns.get_loc('genome')] = g_0[:crossover_point] + g_1[crossover_point:]
            population.iloc[sec_individual, population.columns.get_loc('genome')] = g_1[:crossover_point] + g_0[crossover_point:]
            if debug:
                print("opr:", str(i), str(sec_individual), str(crossover_point),
                      population.iloc[i, population.columns.get_loc('genome')][:crossover_point] + "|" + population.iloc[i, population.columns.get_loc('genome')][crossover_point:],
                      population.iloc[sec_individual, population.columns.get_loc('genome')][:crossover_point] + "|" + population.iloc[sec_individual, population.columns.get_loc('genome')][crossover_point:])


def __two_point_recombination(population, r_rate=0.3, debug=False):
    for i, individual in population.iterrows():
        if np.random.random() < r_rate:
            sec_individual = np.random.choice(population_size, 1, False)[0]
            point_0 = np.random.randint(1, head_size + tail_size - 1)
            point_1 = np.random.randint(point_0 + 1, head_size + tail_size)

            g_0 = individual.genome
            g_1 = population.iloc[sec_individual, population.columns.get_loc('genome')]
            population.iloc[i, population.columns.get_loc('genome')] = g_0[:point_0] + g_1[point_0:point_1] + g_0[point_1:]
            population.iloc[sec_individual, population.columns.get_loc('genome')] = g_1[:point_0] + g_0[point_0:point_1] + g_1[point_1:]
            if debug:
                print("tpr:", str(i), str(sec_individual), str(point_0), str(point_1),
                      population.iloc[i, population.columns.get_loc('genome')][:point_0] + "|" + population.iloc[i, population.columns.get_loc('genome')][point_0:point_1] + "|" + population.iloc[i, population.columns.get_loc('genome')][point_1:],
                      population.iloc[sec_individual, population.columns.get_loc('genome')][:point_0] + "|" + population.iloc[sec_individual, population.columns.get_loc('genome')][point_0:point_1] + "|" + population.iloc[sec_individual, population.columns.get_loc('genome')][point_1:])
