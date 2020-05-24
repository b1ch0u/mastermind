import random as rd
import copy


class Solver:
    '''
    Abstract, child classes should implement a `solve` method.
    '''
    forward_func = None

    def __init__(self, domains, check_satisfaction_func):
        '''
        domains should be a list of sets
        '''
        self.domains = domains
        self.sol_len = len(domains)
        self.constraints = []
        self.check_satisfaction_func = check_satisfaction_func

    def add_constraint(self, constraint):
        self.constraints.append(constraint)


class GenerateAndTest(Solver):
    def generate_random_combination(self):
        return ''.join(rd.choice(tuple(dom)) for dom in self.domains)

    def solve(self):
        '''
        Randomly generate combinations until one is found
        satisfying the given constraints.

        constraints is an iterable of tuples (combination, comparison_result)

        Returns a valid combination.
        '''
        comb = self.generate_random_combination()
        while not self.check_satisfaction_func(self.constraints, comb):
            comb = self.generate_random_combination()
            # TODO aleatoire ou augmentation progressive ?
        return comb, True


class ForwardChecking(Solver):
    def solve(self, partial_soln=''):
        if len(partial_soln) == self.sol_len:
            return partial_soln, True
        index = len(partial_soln)
        for val in self.domains[index]:
            sub_partial_soln = partial_soln + val
            if not self.check_satisfaction_func(self.constraints,
                                                sub_partial_soln):
                continue
            domains_copy = copy.deepcopy(self.domains)
            self.forward_func(self.domains, self.constraints, sub_partial_soln)
            comb, is_valid = self.solve(sub_partial_soln)
            self.domains = domains_copy
            if is_valid:
                return comb, True
        return '', False
