# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 23:28:41 2021

@author: michalm
"""
import pytest
import gep_logic

DATASET = [[1,2,3],[3,2,9],[4,5,24],[3,5,18]]
GRAMMAR = {'FUNC': ['+', '*'], 'TERM': ['a', 'b']}

@pytest.fixture
def example_gep():
    NUM_TRIALS = 30
    LEN_HEAD = 20
    ITERATIONS = 200
    POP_SIZE = 50
    PROB_CROSS = 0.85
 
    return gep_logic.GEP(GRAMMAR, LEN_HEAD, ITERATIONS, POP_SIZE, PROB_CROSS, NUM_TRIALS)

def test_mapping():
    genome = '+b*aab+++*abab++a+b+aaaaababbaabbbababaababbbabbaabbaabbaabaa'
    expected_tree = {'node': '+', 'left': {'node': 'b'}, 'right': {'node': '*', 'left': {'node': 'a'}, 'right': {'node': 'a'}}}
    tree = gep_logic.GEP.mapping(genome)
    assert tree == expected_tree

    genome = '+a*bc'
    expected_tree = {'node': '+', 'left': {'node': 'a'}, 'right': {'node': '*', 'left': {'node': 'b'}, 'right': {'node': 'c'}}}
    tree = gep_logic.GEP.mapping(genome)
    assert tree == expected_tree

    genome = '+b+++abab'
    expected_program = '(b + ((a + b) + (a + b)))'
    tree = gep_logic.GEP.mapping(genome)
    program = gep_logic.GEP.tree_to_string(tree)
    assert program == expected_program



def test_tree_to_string():
    tree = {'node': '+'}
    program = gep_logic.GEP.tree_to_string(tree)
    assert program == '+'

    tree = {'node': '+', 'left': {'node': 'a'}, 'right': {'node': '*', 'left': {'node': 'a'}, 'right': {'node': 'a'}}}
    program = gep_logic.GEP.tree_to_string(tree)
    expected_program = '(a + (a * a))'
    assert program == expected_program

    tree = {'node': '+', 'left': {'node': 'a'}, 'right': {'node': '*', 'left': {'node': 'b'}, 'right': {'node': 'c'}}}
    program = gep_logic.GEP.tree_to_string(tree)
    expected_program = '(a + (b * c))'
    assert program == expected_program

def test_cost():
    program = '(a + (a * a))'
    res = gep_logic.GEP.cost(program)
    assert res == 3.5

    program = '(((a * a) + a) + b)'
    res = gep_logic.GEP.cost(program)
    assert res == 2

    program = '((a * b) + a)'
    res = gep_logic.GEP.cost(program)
    assert res == 0

def test_random_genome(example_gep):
    genome1 = example_gep.random_genome()
    len_head = example_gep.len_head
    len_tail = example_gep.len_tail
    assert len(genome1) == len_head + len_tail
    
    
        
# def main():
#     #test_mapping()
#     #test_tree_to_string()
#     #test_cost()
#     #test_random_genome(example_gep())

# if __name__ == '__main__':
#     main()