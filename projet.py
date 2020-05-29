'''
Evaluate MasterMind strategies.
'''

import time
import statistics

import matplotlib.pyplot as plt

from solver import *  # TODO
import mastermind as mm


##### Partie 1


def play_the_game(cls, n, p, comb):
    #print('\n\nthe solution is', comb)
    domains = mm.generate_domains(n, p)
    instance = cls(domains,
                   mm.check_constraints_satisfaction)
    counter = 1
    for prop, validity in instance.solve():
        if prop == comb:
            break
        #print('one try', prop)
        if not validity:
            raise Exception(cls, 'could not find a solution :(')
        counter += 1
        instance.add_constraint((prop, mm.compare_combinations(prop, comb)))
    #print('ok, found it')
    return counter


### 1.1

## Déterminer les temps moyens de détermination du code secret sur 20 instances
## de taille n = 4 et p = 8

class Backtracking(ForwardChecking):
    @staticmethod
    def forward_func(*args):
        pass


class ForwardAllDiff(ForwardChecking):
    @staticmethod
    def forward_func(domains, _, partial_soln):
        for domain in domains[len(partial_soln):]:
            domain.remove(partial_soln[-1])


def compare_fixed_n(n, p, N, classes):
    instances = [mm.generate_random_combination(n, p) for _ in range(N)]
    for cls in classes:
        print('Testing', cls, f'(N = {N})')
        t1 = time.time()
        res = [play_the_game(cls,
                             n, p,
                             comb)
               for comb in instances]
        total_time = time.time() - t1
        print('nb of propositions'
              f'\tavg : {statistics.mean(res):.1f}'
              f'\tstd : {statistics.stdev(res):.2f}')
        print(f'average time : {total_time / N:.3f}')
        print()


compare_fixed_n(4, 8, 20,
                [GenerateRandomAndTest, EnumerateAndTest,
                 Backtracking, ForwardAllDiff])

## Etudier ensuite l’évolution du temps moyen de résolution et du nombre moyen d’essais
## nécessaires lorsque n et p augmentent

def evaluate_algo_over_n(cls, ax_prop, ax_times, n_min, n_max, instances_by_size):
    avg_nb_prop, avg_times = [], []
    print('evaluating', cls)
    for n in range(n_min, n_max):
        p = 2 * n
        instances = instances_by_size[n]
        t1 = time.time()
        res = [play_the_game(cls,
                             n, p,
                             comb)
               for comb in instances]
        total_time = time.time() - t1
        avg_nb_prop.append(sum(res) / len(instances))
        avg_times.append(total_time / len(instances))
        print(f'finished n = {n}\t(N = {len(instances)}) in {total_time:.3f}s')
    ax_prop.plot(range(n_min, n_max), avg_nb_prop, label=str(cls))
    ax_times.plot(range(n_min, n_max), avg_times, label=str(cls))


def compare_over_n(n_min, n_max, N_base, classes):
    instances_by_size = {n: [mm.generate_random_combination(n, 2 * n)
                             for _ in range(int(N_base / (2 ** n)))]
                         for n in range(n_min, n_max)}

    _, (ax_prop, ax_times) = plt.subplots(1, 2)
    ax_prop.set_title('Average nb of propositions')
    ax_times.set_title('Average time')
    ax_times.set_yscale('log')

    for cls in classes:
        evaluate_algo_over_n(cls, ax_prop, ax_times,
                            n_min, n_max,
                            instances_by_size)

    ax_prop.legend()
    ax_times.legend()
    plt.show()
'''
'''

compare_over_n(2, 5, 2 ** 5,
               [GenerateRandomAndTest, EnumerateAndTest, Backtracking, ForwardAllDiff])

### 1.2

class Forward2Diff(ForwardChecking):
    @staticmethod
    def forward_func(domains, _, partial_soln):
        for val in partial_soln:
            if partial_soln.count(val) == 2:
                for domain in domains[len(partial_soln):]:
                    domain.remove(val)


### 1.3

class ImprovedForward(ForwardChecking):
    @staticmethod
    def forward_func(domains, constraints, partial_soln):

        if len(partial_soln) >= len(domains):
            return

        # forward alldiff
        for domain in domains[len(partial_soln):]:
            domain.remove(partial_soln[-1])

        for comb, res in constraints:
            partial_comp = mm.compare_combinations(partial_soln, comb)
            if sum(res) == sum(partial_comp):
                for domain in domains[len(partial_soln):]:
                    domain.difference_update(comb)


compare_over_n(2, 5, 2 ** 5,
               [ForwardAllDiff, ImprovedForward])


##### Partie 2

### 2.1

# cf mastermind.py & solver.py

### 2.2

class RandomGenetic(Genetic):
    @staticmethod
    def genetic_choice_func(E, _):
        return rd.choice(E)


class MaxGenetic(Genetic):
    @staticmethod
    def genetic_choice_func(E, constraints):
        return max(E, key=lambda comb: mm.evaluate(constraints, comb))


class MinGenetic(Genetic):
    @staticmethod
    def genetic_choice_func(E, constraints):
        return min(E, key=lambda comb: mm.evaluate(constraints, comb))


compare_over_n(2, 5, 2 ** 5,
               [ImprovedForward, RandomGenetic, MaxGenetic, MinGenetic])
