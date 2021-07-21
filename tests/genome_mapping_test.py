from genome import __genome_to_tree, __tree_to_program, genome_to_program

GRAMMAR = {'FUNC': ['+', '*'], 'TERM': ['a', 'b']}


def test_mapping_tree():
    genome = '+b*aab+++*abab++a+b+aaaaababbaabbbababaababbbabbaabbaabbaabaa'
    expected_tree = {'node': '+', 'left': {'node': 'b'}, 'right': {'node': '*', 'left': {'node': 'a'}, 'right': {'node': 'a'}}}
    assert expected_tree == __genome_to_tree(genome, GRAMMAR['FUNC'])

    genome = '+a*bc'
    expected_tree = {'node': '+', 'left': {'node': 'a'}, 'right': {'node': '*', 'left': {'node': 'b'}, 'right': {'node': 'c'}}}
    assert expected_tree == __genome_to_tree(genome, GRAMMAR['FUNC'])


def test_mapping_program():
    tree = {'node': '+', 'left': {'node': 'b'}, 'right': {'node': '*', 'left': {'node': 'a'}, 'right': {'node': 'a'}}}
    expected_program = '(data.b + (data.a * data.a))'
    assert expected_program == __tree_to_program(tree)

    tree = {'node': '+',
            'left': {'node': '+', 'left': {'node': '*', 'left': {'node': 'b'}, 'right': {'node': 'b'}}, 'right': {'node': 'b'}},
            'right': {'node': '*', 'left': {'node': 'a'}, 'right': {'node': 'a'}}}
    expected_string = '(((data.b * data.b) + data.b) + (data.a * data.a))'
    assert expected_string == __tree_to_program(tree)

    tree = {'node': 'b'}
    expected_string = 'data.b'
    assert expected_string == __tree_to_program(tree)


def test_mapping_genome():
    genome = '+a*bc'
    expected_program = '(data.a + (data.b * data.c))'
    assert expected_program == genome_to_program(genome, GRAMMAR['FUNC'])
