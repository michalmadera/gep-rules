import pandas as pd

from experiments import determine_probability, select_by_roulette_wheel


def test_determine_probability():
    group = pd.DataFrame({'fitness': [1, 2, 3, 4, 7], 'id': ['A', 'B', 'C', 'D', 'E']})
    determine_probability(group)
    assert list(group['probability']) == [0.043478260869565216, 0.21739130434782608, 0.43478260869565216, 0.6956521739130435, 1.0]
    assert list(group['id']) == ['E', 'D', 'C', 'B', 'A']

    group = pd.DataFrame({'fitness': [7, 4, 3, 2, 1], 'id': ['A', 'B', 'C', 'D', 'E']})
    determine_probability(group)
    assert list(group['probability']) == [0.043478260869565216, 0.21739130434782608, 0.43478260869565216, 0.6956521739130435, 1.0]
    assert list(group['id']) == ['A', 'B', 'C', 'D', 'E']

    group = pd.DataFrame({'fitness': [0.25, 1.1, 0.08, 0.99, 1.6], 'id': ['A', 'B', 'C', 'D', 'E']})
    determine_probability(group)
    assert list(group['probability']) == [0.018264840182648415, 0.1506849315068493, 0.3082191780821918, 0.634703196347032, 1.0]
    assert list(group['id']) == ['E', 'B', 'D', 'A', 'C']

    group = pd.DataFrame({'fitness': [1]})
    determine_probability(group)
    assert list(group['probability']) == [1.0]

    group = pd.DataFrame({'fitness': []})
    determine_probability(group)
    assert list(group['probability']) == []


def test_select_by_roulette_wheel(mocker):
    group = pd.DataFrame({'fitness': [1, 2, 3, 4, 7], 'id': ['A', 'B', 'C', 'D', 'E']})

    mocker.patch('numpy.random.rand', return_value=[0.99, 0.6, 0.3, 0.17, 0.04])
    selected = select_by_roulette_wheel(group)
    assert list(selected['id']) == ['A', 'B', 'C', 'D', 'E']

    mocker.patch('numpy.random.rand', return_value=[0.2, 0.01, 0.1458, 0.70, 0.99999])
    selected = select_by_roulette_wheel(group)
    assert list(selected['id']) == ['D', 'E', 'D', 'A', 'A']

