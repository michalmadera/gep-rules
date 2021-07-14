

def test_tree_to_string():
    tree = {'node': '+', 'left': {'node': 'b'}, 'right': {'node': '*', 'left': {'node': 'a'}, 'right': {'node': 'a'}}}
    expected_string = '(b + (a * a))'
    assert expected_string == tree_to_string(tree)

    tree = {'node': '+', 'left': {'node': '+', 'left': {'node': '*', 'left': {'node': 'b'}, 'right': {'node': 'b'}}, 'right': {'node': 'b'}},
            'right': {'node': '*', 'left': {'node': 'a'}, 'right': {'node': 'a'}}}
    expected_string = '(((b * b) + b) + (a * a))'
    assert expected_string == tree_to_string(tree)

    tree = {'node': 'b'}
    expected_string = 'b'
    assert expected_string == tree_to_string(tree)


