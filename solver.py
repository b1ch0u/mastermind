import random as rd
import mastermind as mm


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
        self.comb = ""

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    @classmethod
    def complete_solve(cls, domains, test_func, compare_func, comb):
        instance = cls(domains, test_func)
        instance.comb = comb
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

class AG(Solver):
    def __init__(self, domains, test_func):
        self.pMuta = 0.8
        super().__init__(domains,test_func)
    def solve(self):
        return "".join(rd.choice(mm.algoGenetique(self.sol_len,self.sol_len*2,100,100,0.5,50,self.constraints))), True
    def setPMuta(self, pMuta):
        self.pMuta = pMuta
    
    
class AG2(Solver):
    def __init__(self, domains, test_func):
        self.pMuta = 0.8
        super().__init__(domains,test_func)
    def solve(self):
        E = mm.algoGenetique(self.sol_len,self.sol_len*2,100,100,0.5,50,self.constraints)
        iMax=0
        scoreMax=0
        for i in range(len(E)):
            score = mm.evaluate(self.constraints,E[i])
            if score > scoreMax:
                scoreMax = score
                iMax = i
        return "".join(E[i]), True
    def setPMuta(self, pMuta):
        self.pMuta = pMuta
    
class AG3(Solver):
    def __init__(self, domains, test_func):
        self.pMuta = 0.8
        super().__init__(domains,test_func)
    def solve(self):
        E = mm.algoGenetique(self.sol_len,self.sol_len*2,100,100,self.pMuta,50,self.constraints)
        iMin=0
        scoreMin=10000
        for i in range(len(E)):
            score = mm.evaluate(self.constraints,E[i])
            if score < scoreMin:
                scoreMin = score
                iMin = i
        return "".join(E[i]), True
    
    def setPMuta(self, pMuta):
        self.pMuta = pMuta
        
class AG4(Solver):
    def __init__(self, domains, test_func):
        self.pMuta = 0.8
        super().__init__(domains,test_func)
    def solve(self):
        E = mm.algoGenetique(self.sol_len,self.sol_len*2,100,100,self.pMuta,50,self.constraints)
        iBest=0
        bestScore= 10000
        for i in range(len(E)):
            score=0
            newConstraint = self.constraints.copy()
            newConstraint.append((E[i], mm.compare_combinations(E[i], self.comb )))
            
            for j in range(len(E)):
                if mm.check_constraints_satisfaction(newConstraint, E[j]):
                    score+=1
            if score < bestScore:
                bestScore = score
                iBest = i
                    
        return "".join(E[iBest]), True
    
    def setPMuta(self, pMuta):
        self.pMuta = pMuta