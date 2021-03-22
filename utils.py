def tree_to_string(tree):
    if 'left' not in tree or 'right' not in tree:
        return tree['node']
    left = tree_to_string(tree['left'])
    right = tree_to_string(tree['right'])
    tree = '({0} {1} {2})'.format(left, tree['node'], right)
    return tree



