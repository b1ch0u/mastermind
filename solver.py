import random as rd
import itertools as it
import copy

import mastermind as mm


class Solver:
    '''
    Abstract, child classes should implement a `solve` method.
    '''
    forward_func = None
    verbose = False

    def __init__(self, domains, check_satisfaction_func):
        '''
        domains should be a list of sets
        '''
        self.domains = domains
        self.sol_len = len(domains)
        self.constraints = []
        self.check_satisfaction_func = check_satisfaction_func
        self.enumerator = it.product(*domains)

    def add_constraint(self, constraint):
        self.constraints.append(constraint)


class GenerateRandomAndTest(Solver):
    def generate_random_combination(self):
        return list(rd.choice(tuple(dom)) for dom in self.domains)

    def solve(self):
        '''
        Randomly generate combinations until one is found
        satisfying the constraints.

        Warning : may not terminate.
        '''
        while True:
            comb = self.generate_random_combination()
            while not self.check_satisfaction_func(self.constraints, comb):
                comb = self.generate_random_combination()
            yield comb, True


class EnumerateAndTest(Solver):
    def solve(self):
        '''
        Enumerate all combinations until one is found
        satisfying the constraints.
        '''
        for comb in self.enumerator:
            if self.check_satisfaction_func(self.constraints, comb):
                yield list(comb), True
        yield None, False


class ForwardChecking(Solver):
    def solve(self, partial_soln=None):
        if partial_soln is None:
            partial_soln = []
        if len(partial_soln) == self.sol_len:
            yield partial_soln, True
        else:
            index = len(partial_soln)
            for val in self.domains[index]:
                sub_partial_soln = partial_soln + [val]
                if not self.check_satisfaction_func(self.constraints,
                                                    sub_partial_soln):
                    continue
                domains_copy = copy.deepcopy(self.domains)
                self.forward_func(self.domains, self.constraints, sub_partial_soln)
                for comb, is_valid in self.solve(sub_partial_soln):
                    if is_valid:
                        yield comb, True
                self.domains = domains_copy
            yield None, False


class AG(Solver):
    def solve(self):
        E = mm.algoGenetique(self.sol_len,self.sol_len*2,100,100,0.8,50,self.constraints)
        if not E:
            return None, False
        return "".join(rd.choice(E)), True


class AG2(Solver):
    def solve(self):
        E = mm.algoGenetique(self.sol_len,self.sol_len*2,100,100,0.8,50,self.constraints)
        if not E:
            return '', False
        iMax=0
        scoreMax=0
        for i in range(len(E)):
            score = mm.evaluate(self.constraints,E[i])
            if score > scoreMax:
                scoreMax = score
                iMax = i
        return "".join(E[i]), True


class AG3(Solver):
    def solve(self):
        E = mm.algoGenetique(self.sol_len,self.sol_len*2,100,100,0.8,50,self.constraints)
        if not E:
            return '', False
        iMin=0
        scoreMin=10000
        for i in range(len(E)):
            score = mm.evaluate(self.constraints,E[i])
            if score < scoreMin:
                scoreMin = score
                iMin = i
        return "".join(E[i]), True
