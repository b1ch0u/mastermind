import random as rd


class Solver:
    '''
    Abstract, child classes should implement a `solve` method.
    '''
    def __init__(self, domains, test_func):
        '''
        domains should be a list of sets
        test_func must be able to evaluate partial solutions
        '''
        self.domains = domains
        self.sol_len = len(domains)
        self.constraints = []
        self.test_func = test_func

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    @classmethod
    def complete_solve(cls, domains, test_func, compare_func, comb):
        instance = cls(domains, test_func)
        counter = 1
        prop, _ = instance.solve()
        while prop != comb:
            #print(comb, prop, instance.constraints)
            counter += 1
            instance.add_constraint((prop, compare_func(prop, comb)))
            prop, _ = instance.solve()
        return counter


class A1(Solver):
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
        while not self.test_func(self.constraints, comb):
            comb = self.generate_random_combination()
        return comb, True


class A2(Solver):
    def solve(self, partial_solution=''):
        if len(partial_solution) == self.sol_len:
            return partial_solution, True
        index = len(partial_solution)
        for val in self.domains[index]:
            sub_partial_solution = partial_solution + val
            if not self.test_func(self.constraints, sub_partial_solution):
                continue
            comb, is_valid = self.solve(sub_partial_solution)
            if is_valid:
                return comb, True
        return '', False


class A3(Solver):
    def solve(self, partial_solution=''):
        if len(partial_solution) == self.sol_len:
            return partial_solution, True
        index = len(partial_solution)
        for val in self.domains[index]:
            sub_partial_solution = partial_solution + val
            if not self.test_func(self.constraints, sub_partial_solution):
                continue
            for i in range(index + 1, self.sol_len):
                self.domains[i].remove(val)
            comb, is_valid = self.solve(sub_partial_solution)
            for i in range(index + 1, self.sol_len):
                self.domains[i].add(val)
            if is_valid:
                return comb, True
        return '', False

class A4(Solver):
    def solve(self, partial_solution=''):
        if len(partial_solution) == self.sol_len:
            return partial_solution, True
        index = len(partial_solution)
        for val in self.domains[index]:
            sub_partial_solution = partial_solution + val
            if not self.test_func(self.constraints, sub_partial_solution):
                continue
            # La diff avec A3 est seulement cette condition
            # generalisable facilement
            if index > 0 and any(val in dom for dom in self.domains[index - 1]):
                for i in range(index + 1, self.sol_len):
                    self.domains[i].remove(val)
            comb, is_valid = self.solve(sub_partial_solution)
            for i in range(index + 1, self.sol_len):
                self.domains[i].add(val)  # interet de set, pas de condition
            if is_valid:
                return comb, True
        return '', False
