import random as rd
from collections import Counter


COLORS = ('0123456789'
          'ABCDEFGHIJKLMNOPQRSTUVWXYZ')


def generate_random_combination(n, p):
    return ''.join(rd.sample(COLORS[:p], n))


def generate_random_2_combination(n, p):
    s1 = rd.sample(COLORS[:p], n)
    s2 = rd.sample(COLORS[:p], n)
    return ''.join(rd.choice(t) for t in zip(s1, s2))


def generate_domains(res_len, colors_nb):
    return [set(COLORS[:colors_nb]) for _ in range(res_len)]


def compare_combinations(comb, sol):
    '''
    Compare two combinations.
    Assumes len(comb) <= len(sol)

    Return (correct_indices_nb, incorrect_indices_nb)

    >>> compare_combinations('', '')
    (0, 0)

    >>> compare_combinations('1', '1')
    (1, 0)

    >>> compare_combinations('1', '0')
    (0, 0)

    >>> compare_combinations('01', '10')
    (0, 2)

    >>> compare_combinations('1124AB', 'AB1113')
    (0, 4)
    '''
    # TODO add doc partial comparison
    correct_indices = {i for i in range(len(comb))
                       if comb[i] == sol[i]}
    comb_counter = Counter([v for i, v in enumerate(comb)
                            if comb[i] != sol[i]])
    sol_counter = Counter([v for i, v in enumerate(sol)
                           if i >= len(comb) or comb[i] != sol[i]])
    incorrect_indices_nb = sum((comb_counter & sol_counter).values())
    return len(correct_indices), incorrect_indices_nb


def check_constraints_satisfaction(constraints, prop):
    if not constraints:
        return True

    if len(prop) == len(constraints[0][0]):
        return all(compare_combinations(prop, comb) == res
                   for comb, res in constraints)

    for comb, res in constraints:
        comparison = compare_combinations(prop, comb)
        if comparison[0] > res[0] \
                or comparison[1] > res[1]:
                #or len(comb) - sum(res) > len(prop) - sum(comparison):
            return False
    return True


def check_constraints_satisfaction_and_alldiff(constraints, prop):
    if len(set(prop)) != len(prop):
        return False
    return check_constraints_satisfaction(constraints, prop)
