def __genome_to_tree(genome, functions):
    off = 0
    queue = list()
    root = {'node': genome[off]}
    off += 1
    queue.append(root)
    while len(queue) > 0:
        current = queue.pop(0)
        if current['node'] in functions:
            current['left'] = {'node': genome[off]}
            off += 1
            queue.append(current['left'])
            current['right'] = {'node': genome[off]}
            off += 1
            queue.append(current['right'])
    return root


def __tree_to_program(tree):
    prefix = 'data.'
    if 'left' not in tree or 'right' not in tree:
        return prefix + tree['node']
    left = prefix + __tree_to_program(tree['left'])
    right_value = __tree_to_program(tree['right'])
    right = prefix + right_value
    tree = '({0} {1} {2})'.format(left, tree['node'], right)
    return tree


def genome_to_program(genome, functions):
    return __tree_to_program(__genome_to_tree(genome, functions)).replace('data.(', '(').replace('data.data.', 'data.')
