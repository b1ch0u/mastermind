'''
Evaluate MasterMind strategies.
'''

import time
import statistics

import matplotlib.pyplot as plt

from solver import *  # TODO
import mastermind as mm

'''
une comb est sous la forme d'une chaine de caracteres
'''

##### Partie 1


def play_the_game(cls, n, p, comb):
    #print('\n\nthe solution is', comb)
    domains = mm.generate_domains(n, p)
    instance = cls(domains,
                   mm.check_constraints_satisfaction_and_alldiff)
    counter = 1
    prop, validity = instance.solve()
    while validity and prop != comb:
        counter += 1
        instance.add_constraint((prop, mm.compare_combinations(prop, comb)))
        prop, validity = instance.solve()
    if not validity:
        raise Exception(cls, 'could not find a solution :(')
    return counter


### 1.1

# cf implementations dans solver.py

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


class Forward2Diff(ForwardChecking):
    @staticmethod
    def forward_func(domains, _, partial_soln):
        for val in partial_soln:
            if partial_soln.count(val) == 2:
                for domain in domains[len(partial_soln):]:
                    domain.remove(val)


class ImprovedForward(ForwardChecking):
    @staticmethod
    def forward_func(domains, _, partial_soln):
        pass


n, p = 4, 8
N = 20
instances = [mm.generate_random_combination(n, p) for _ in range(N)]
for cls in [GenerateAndTest, Backtracking, ForwardAllDiff]:
    print('Testing', cls, '...')
    t1 = time.time()
    res = [play_the_game(cls,
                         n, p,
                         comb)
           for comb in instances]
    total_time = time.time() - t1
    print('nb of propositions')
    print('avg :', statistics.mean(res))
    print('std :', statistics.stdev(res))
    print('average time', total_time / N)
    print()


## Etudier ensuite l’évolution du temps moyen de résolution et du nombre moyen d’essais
## nécessaires lorsque n et p augmentent

N_base = 20
def evaluate_algo_over_n(cls, ax_prop, ax_times):
    avg_nb_prop, avg_times = [], []
    n_min, n_max = 2, 7
    print('evaluating', cls)
    for n in range(n_min, n_max):
        p = 2 * n
        N = int(N_base / n)
        instances = [mm.generate_random_combination(n, p) for _ in range(N)]
        t1 = time.time()
        res = [play_the_game(cls,
                             n, p,
                             comb)
               for comb in instances]
        total_time = time.time() - t1
        avg_nb_prop.append(sum(res) / N)
        avg_times.append(total_time / N)
        print('finished n =', n)
    ax_prop.plot(range(n_min, n_max), avg_nb_prop, label=str(cls))
    ax_times.plot(range(n_min, n_max), avg_times, label=str(cls))

fig, (ax_prop, ax_times) = plt.subplots(1, 2)
ax_prop.set_title('Average nb of propositions')
ax_times.set_title('Average time')
ax_times.set_yscale('log')
for cls in [GenerateAndTest, Backtracking, ForwardAllDiff]:
    evaluate_algo_over_n(cls, ax_prop, ax_times)
ax_prop.legend()
ax_times.legend()
plt.show()


### 1.3
