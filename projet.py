'''
Evaluate MasterMind strategies.
'''

import time

import matplotlib.pyplot as plt

from solver import *
import mastermind as mm

'''
une comb est sous la forme d'une chaine de caracteres
'''


### 1.1

# cf implementations dans solver.py

## Déterminer les temps moyens de détermination du code secret sur 20 instances
## de taille n = 4 et p = 8

n, p = 4, 8
N = 10
instances = [mm.generate_random_combination(n, p) for _ in range(N)]
for cls in Solver.__subclasses__():
    domains = mm.generate_domains(n, p)
    t1 = time.time()
    res = [cls.complete_solve(domains,
                              mm.check_partial_constraints,
                              mm.compare_combinations,
                              comb)
           for comb in instances]
    total_time = time.time() - t1
    print(cls)
    print('average nb of propositions', sum(res) / len(res))
    print('average time', total_time / N)
    print()

## Etudier ensuite l’évolution du temps moyen de résolution et du nombre moyen d’essais
## nécessaires lorsque n et p augmentent

N_base = 10
def evaluate_algo_over_n(cls, ax_prop, ax_times):
    avg_nb_prop, avg_times = [], []
    n_min, n_max = 2, 6
    print('evaluating', cls)
    for n in range(n_min, n_max):
        p = 2 * n
        N = int(N_base / n)
        instances = [mm.generate_random_combination(n, p) for _ in range(N)]
        domains = mm.generate_domains(n, p)
        t1 = time.time()
        res = [cls.complete_solve(domains,
                                  mm.check_partial_constraints,
                                  mm.compare_combinations,
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
for cls in Solver.__subclasses__():
    evaluate_algo_over_n(cls, ax_prop, ax_times)
ax_prop.legend()
ax_times.legend()
plt.show()


### 1.3
