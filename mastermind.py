import random as rd
import time
from collections import Counter


def generate_random_combination(n, p):
    return rd.sample(range(p), n)


def generate_random_2_combination(n, p):
    s1 = rd.sample(range(p), n)
    s2 = rd.sample(range(p), n)
    return list(rd.choice(t) for t in zip(s1, s2))


def generate_domains(res_len, colors_nb):
    return [set(range(colors_nb)) for _ in range(res_len)]


# TODO essayer autre implementation de compare_combinations

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
            return False
    return True


def check_constraints_satisfaction_and_alldiff(constraints, prop):
    if len(set(prop)) != len(prop):
        return False
    return check_constraints_satisfaction(constraints, prop)


def evaluate(previous, prop):
    score = 0
    for comb, res in previous:
        nb_common = sum(a == b for a, b in zip(comb, prop))
        score += 4 * nb_common
    return score


def croisement(parent1, parent2):
    i = rd.randrange(len(parent1))
    p1 = list(parent1)
    p2 = list(parent2)
    fils1 = list(parent1)
    fils2 = list(parent2)
    for j in range(len(fils1)):
        if j <= i:
            for e in p2:
                if e not in fils1[i:]:
                    fils1[j] = e
                    p2.remove(e)
                    break
        else:
            for e in p1:
                if e not in fils2[:i+1]:
                    p1.remove(e)
                    fils2[j] = e
                    break
    return fils1, fils2


def mutation(fils, Dn):
    mut = rd.randrange(3)

    # Changement aléatoire d'un caractère
    if mut == 0:
        i = rd.randrange(len(fils))
        fils[i] = rd.choice(list(set(Dn) - set(fils)))
        return fils

    i, j = rd.sample(range(len(fils)), 2)
    i, j = min(i, j), max(i, j)

    # échange entre deux caractères
    if mut == 1:
        fils[i], fils[j] = fils[j], fils[i]
        return fils

    # inversion de la séquence entre deux caractères
    return fils[0:i] + list(reversed(fils[i: j])) + fils[j:]


def algoGenetique(n,p,N,NbG,Pm, maxSize,constraint):
    P = [generate_random_combination(n, p)
         for _ in range(N)] #Pop initial
    E = []
    #F = [0 for i in range(N)]
    t=time.time()
    k=0
    while len(E) < maxSize and k < NbG or (not E and time.time()-t < 300):
        Pp = []

        for i in range(int(N/2)):

            #Selection:
            parent1, parent2 = rd.sample(P, 2)
            #Croisement:
            fils1, fils2 = croisement(parent1, parent2)
            #Mutation:
            if(rd.random() < Pm):
                fils1 = mutation(fils1, list(range(p)))
            if(rd.random() < Pm):
                fils2 = mutation(fils2, list(range(p)))

            #Insertion:
            Pp += [fils1, fils2]
        P=Pp

        #On regarde dans Pp les nouvelles combinaisons compatibles
        E += [e for e in P if check_constraints_satisfaction(constraint, e)]

        k+=1
    return E
