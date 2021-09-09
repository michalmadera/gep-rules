from setup import *


def reproduction(population, debug=False):
    if debug:
        print("===== mutation =====")
        for i, individual in population.iterrows():
            print(str(i), individual.genome)

    population = __replication(population)
    population['genome'] = population.apply(lambda x: __point_mutation(x.genome, debug=debug), axis=1)
    population['genome'] = population.apply(lambda x: __is_transposition(x.genome, debug=debug), axis=1)
    population['genome'] = population.apply(lambda x: __ris_transposition(x.genome, debug=debug), axis=1)
    population['genome'] = population.apply(lambda x: __one_point_recombination(x.genome, population, debug=debug), axis=1)
    population['genome'] = population.apply(lambda x: __two_point_recombination(x.genome, population, debug=debug), axis=1)

    if debug:
        for i, individual in population.iterrows():
            print(str(i), individual.genome)
        print("===== end =====")
    return population


def __replication(population):
    return population[['genome']].copy()


def __point_mutation(genome, m_rate=0.05, debug=False):
    new_genome = list()
    changed = list()
    for ind in range(len(genome)):
        bit = genome[ind]
        if np.random.random() < m_rate:
            if ind < head_size:
                selection = functions if np.random.random() < 0.6 else terms
                bit = selection[np.random.randint(0, len(selection))]
            else:
                bit = terms[np.random.randint(0, len(terms))]
            changed.append(str(ind) + ": " + genome[ind] + ">" + bit)
        new_genome.append(bit)
    result = ''.join(new_genome)

    if debug and len(changed) > 0:
        print("pm:", changed, genome, result)
    return result


def __is_transposition(genome, t_rate=0.1, debug=False):
    new_genome = genome
    if np.random.random() < t_rate:
        size = np.random.randint(1, 4)
        index_of_copying = np.random.randint(0, head_size + tail_size - size)
        index_of_inserting = np.random.randint(1, head_size - size)

        insertion_seq = genome[index_of_copying:index_of_copying + size]
        new_genome = genome[:index_of_inserting] + insertion_seq + genome[index_of_inserting+size:head_size] + genome[head_size:]

        if debug:
            print("is:", str(index_of_inserting), insertion_seq, genome, new_genome)
    return new_genome


def __ris_transposition(genome, t_rate=0.1, debug=False):
    new_genome = genome
    if np.random.random() < t_rate:
        size = np.random.randint(1, 4)
        index_of_start_copying = np.random.randint(1, head_size)

        insertion_seq = ""
        for ind, val in enumerate(genome[index_of_start_copying:]):
            if val in functions:
                insertion_seq = genome[ind + index_of_start_copying:ind + index_of_start_copying + size]
                break

        new_genome = insertion_seq + genome[:head_size - len(insertion_seq)] + genome[head_size:]

        if debug:
            print("ris:", insertion_seq, genome, new_genome)
    return new_genome


def __one_point_recombination(genome, population, r_rate=0.3, debug=False):
    new_genome = genome
    if np.random.random() < r_rate:
        crossover_point = np.random.randint(1, head_size + tail_size)
        sec_individual = np.random.choice(population_size)
        sec_genome = population.iloc[sec_individual, population.columns.get_loc('genome')]

        new_genome = genome[:crossover_point] + sec_genome[crossover_point:]
        new_sec_genome = sec_genome[:crossover_point] + genome[crossover_point:]
        population.iloc[sec_individual, population.columns.get_loc('genome')] = new_sec_genome

        if debug:
            print("opr:", str(sec_individual),
                  new_genome[:crossover_point] + "|" + new_genome[crossover_point:],
                  new_sec_genome[:crossover_point] + "|" + new_sec_genome[crossover_point:])
    return new_genome


def __two_point_recombination(genome, population, r_rate=0.3, debug=False):
    new_genome = genome
    if np.random.random() < r_rate:
        point_0 = np.random.randint(1, head_size + tail_size - 1)
        point_1 = np.random.randint(point_0 + 1, head_size + tail_size)
        sec_individual = np.random.choice(population_size)
        sec_genome = population.iloc[sec_individual, population.columns.get_loc('genome')]

        new_genome = genome[:point_0] + sec_genome[point_0:point_1] + genome[point_1:]
        new_sec_genome = sec_genome[:point_0] + genome[point_0:point_1] + sec_genome[point_1:]
        population.iloc[sec_individual, population.columns.get_loc('genome')] = new_sec_genome

        if debug:
            print("tpr:", str(sec_individual),
                  new_genome[:point_0] + "|" + new_genome[point_0:point_1] + "|" + new_genome[point_1:],
                  new_sec_genome[:point_0] + "|" + new_sec_genome[point_0:point_1] + "|" + new_sec_genome[point_1:])
    return new_genome
