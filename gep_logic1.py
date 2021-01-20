# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 20:36:52 2021

@author: michalm
"""

import numpy as np

class GEP(object):
    def __init__(self, grammar, len_head, iterations, pop_size, prob_crossover, num_trials):
        self.grammar = grammar
        self.len_head = len_head
        self.len_tail = len_head * (len(grammar['TERM'])) + 1
        self.iterations = iterations
        self.pop_size = pop_size
        self.prob_crossover = prob_crossover
        self.num_trials = num_trials

    def binary_tournament(self):
        a, b = np.random.choice(self.population, 2)
        return a if a.fitness < b.fitness else b

    def point_mutation(self, genome):
        rate = 1.0 / len(genome)
        child = list()
        for i in range(len(genome)):
            bit = genome[i]
            if np.random.random() < rate:
                if i < self.len_head:
                    selection = self.grammar['FUNC'] if np.random.random() < 0.5 else self.grammar['TERM']
                    bit = selection[np.random.randint(0, len(selection))]
                else:
                    bit = self.grammar['TERM'][np.random.randint(0, len(self.grammar['TERM']))]
            child.append(bit)
        return ''.join(child)

    def crossover(self, parent1, parent2):
        print('cross', parent1, parent2)
        
        if np.random.random() < self.prob_crossover:
            child = ''.join([a if np.random.random() < 0.5 else b for a, b in zip(parent1, parent2)])
        else:
            child = parent1
        
        print('child', child)
        return child

    def reproduce(self, selected):
        children = list()
        for a, b in zip(selected[::2], selected[1::2]):
            children.append(Individual(self.point_mutation(self.crossover(a.genome, b.genome))))
        return children

    def random_genome(self):
        s = list()
        for _ in range(self.len_head):
            selection = self.grammar['FUNC'] if np.random.random() < 0.5 else self.grammar['TERM']
            s.append(selection[np.random.randint(0, len(selection))])
        for _ in range(self.len_tail):
            s.append(self.grammar['TERM'][np.random.randint(0, len(self.grammar['TERM']))])
        return ''.join(s)

    @staticmethod
    def cost(program):
        errors = 0.0
        index = 0
        for a, b, y in DATASET:
            expression = program.replace('a', str(a)).replace('b', str(b))
            try:
                score = eval(expression)
            except ZeroDivisionError:
                score = float('inf')
            error = abs(score - y)
            errors += error
            # print(index, program, '->',expression,' = ', score, 'Expected:', y, 'Error:', error)
            index += 1
        if np.isnan(errors):
            errors = float('inf')
        return errors / len(DATASET)

    @staticmethod
    def mapping(genome):
        off = 0
        queue = list()
        root = {'node': genome[off]}
        off += 1
        queue.append(root)
        while len(queue) > 0:
            current = queue.pop(0)
            if current['node'] in GRAMMAR['FUNC']:
                current['left'] = {'node': genome[off]}
                off += 1
                queue.append(current['left'])
                current['right'] = {'node': genome[off]}
                off += 1
                queue.append(current['right'])
        return root

    @staticmethod
    def tree_to_string(exp):
        if 'left' not in exp or 'right' not in exp:
            return exp['node']
        left = GEP.tree_to_string(exp['left'])
        right = GEP.tree_to_string(exp['right'])
        return '({0} {1} {2})'.format(left, exp['node'], right)

    def run(self):
        self.population = [Individual(self.random_genome()) for _ in range(self.pop_size)]
        self.best = sorted(self.population, key=lambda x: x.fitness)[0]
        for gen in range(1, self.iterations + 1):
            print('GENERATION:', gen)
            selected = [self.binary_tournament() for _ in range(self.pop_size)]
            children = self.reproduce(selected)
            children = list(sorted(children, key=lambda x: x.fitness))
            self.best = children[0] if children[0].fitness <= self.best.fitness else self.best
            self.population = sorted((children + self.population), key=lambda x: x.fitness)[:self.pop_size]
            if gen % 50 == 0:
                print('{0}/{1} Current population:'.format(gen, self.iterations))
                print(self.best)
            if self.best.fitness == 0.0:
                print('{0}/{1} Current population:'.format(gen, self.iterations))
                print(self.best)
                break
        return self.best


class Individual(object):
    def __init__(self, genome):
        self.genome = genome
        self.expression = GEP.mapping(genome)
        self.program = GEP.tree_to_string(self.expression)
        self.fitness = GEP.cost(self.program)

    def __str__(self):
        return '{0} = {1}'.format(self.program, self.fitness)


GRAMMAR = {'FUNC': ['+', '*'], 'TERM': ['a', 'b']}
DATASET = [[1,2,3],[3,2,9],[4,5,24],[3,5,18]]

NUM_TRIALS = 30
LEN_HEAD = 20
ITERATIONS = 200
POP_SIZE = 50
PROB_CROSS = 0.85


def main():
    gep = GEP(GRAMMAR, LEN_HEAD, ITERATIONS, POP_SIZE, PROB_CROSS, NUM_TRIALS)
    gep.run()

if __name__ == '__main__':
    main()