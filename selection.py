import numpy as np

from setup import population_size


def __reverse_fitness(population):
    """ only until the method of calculating fitness is changed """
    max_fitness = population['fitness'].max()
    min_fitness = population['fitness'].min()
    reverse_fitness = list()
    for f in population['fitness']:
        reverse_fitness.append(min_fitness + max_fitness - f)
    population['reversed fitness'] = reverse_fitness


def __determine_probability(population):
    __reverse_fitness(population)
    population.sort_values('reversed fitness', inplace=True)
    sum_fitness = population['reversed fitness'].sum()
    probability = 0.0
    probabilities = list()
    for x in population['reversed fitness']:
        probability = probability + (x / sum_fitness)
        probabilities.append(probability)
    population['probability'] = probabilities


def select_by_roulette_wheel(population, debug=False):
    """https://en.wikipedia.org/wiki/Fitness_proportionate_selection"""
    __determine_probability(population)
    random_selection = np.random.rand(len(population))
    selected = list()
    population.sort_values('probability', inplace=True)
    if debug:
        print(population)
    for rand in random_selection:
        for i, probability in enumerate(population['probability']):
            if rand < probability:
                selected.append(i)
                break
    result = population.iloc[selected]
    if debug:
        print(selected)
        print(result)
    return result


def select_by_random(population):
    selected = np.random.choice(population_size, population_size)
    return population.iloc[selected]


def best_of_population(selected, crossed):
    """DEPRECATED"""
    population = selected.append(crossed, ignore_index=True).sort_values('fitness')[:population_size]
    population.index = range(0, len(population))
    return population


def select_by_binary_tournament(group):
    """DEPRECATED"""
    random_selection = np.random.randint(0, len(group), len(group))
    return group.apply(lambda x: (
        x if x.fitness < group.iloc[random_selection[x.name]].fitness
        else group.iloc[random_selection[x.name]]), axis=1)
