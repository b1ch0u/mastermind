import random as rd
import time
from collections import Counter


COLORS = ('0123456789'
          'ABCDEFGHIJKLMNOPQRSTUVWXYZ')


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


def generate_random_combination(n, p):
    return ''.join(rd.sample(COLORS[:p], n))


def generate_random_2_combination(n, p):
    s1 = rd.sample(COLORS[:p], n)
    s2 = rd.sample(COLORS[:p], n)
    return ''.join(rd.choice(t) for t in zip(s1, s2))


def check_constraints_satisfaction(constraints, prop):
    return all(compare_combinations(comb, prop) == res
               for comb, res in constraints)


def check_partial_constraints(constraints, prop):
    for comb, res in constraints:
        comparison = compare_combinations(prop, comb)  # len(prop) <= len(comb)
        if comparison[0] > res[0] \
                or comparison[1] > res[1] \
                or sum(comparison) > sum(res):
            return False
    return True

def check_constraints_compatibility(constraints, prop):
    if not check_partial_constraints(constraints, prop):
        return False
    for comb, res in constraints:
        if len(set(prop) & set(comb)) > sum(res):
            return False
    return True
	
def evaluate(previous, prop):
    p = list(prop)
    score = 0
    for e, r in previous:
        e = list(e)
        for i in range(len(e)):
            if e[i] == p[i]:
                score +=10
            if e[i] in p:
                score +=2
            
    return score

def croisement(parent1, parent2):
    i = rd.randrange(len(parent1))
    p1=list(parent1)
    p2=list(parent2)
    fils1=list(parent1)
    fils2=list(parent2)
    for j in range(len(fils1)):
        if j<=i:
            for e in p2:
                if e not in fils1[i:]:
                    fils1[j]=e
                    p2.remove(e)
                    break
        else:
            for e in p1:
                if e not in fils2[:i+1]:
                    p1.remove(e)
                    fils2[j]=e
                    break
    return fils1, fils2

def mutation(fils, Dn):
    fils=list(fils)
    mut = rd.randrange(3)
    #Changement aléatoire d'un caractère
    if mut == 0:
        i = rd.randrange(len(fils))
        e=rd.choice(Dn)
        while e in fils:
            e=rd.choice(Dn)
        fils[i]=e
        return fils
    #échange entre deux caractères
    elif mut == 1:
        i = rd.randrange(len(fils))
        j = rd.randrange(len(fils))
        while i == j:
            j = rd.randrange(len(fils))
            
        tmp = fils[i]
        fils[i]=fils[j]
        fils[j]=tmp
        return fils
        
    #inversion de la séquence entre deux caractères
    elif mut == 2:
        i = rd.randrange(len(fils))
        j = rd.randrange(len(fils))
        while i == j:
            j = rd.randrange(len(fils))
            
        if i > j:
            tmp = i
            i=j
            j=tmp
        if i<0:
            i==1
        
        #print(fils)
        inv = fils[i:j]
        inv.reverse()
        r=fils[0:i] + inv + fils[j:]
        #print(r, i,j)
        
        return r
    return fils

        

def algoGenetique(n,p,N,NbG,Pm, maxSize,constraint):
    P = [generate_random_combination(n,p) for i in range(N)] #Pop initial
    E = []
    #F = [0 for i in range(N)]
    t=time.time()
    k=0
    while k < NbG or (len(E) <= 0 and time.time()-t < 300):
        Pp = []
        
        for i in range(int(N/2)):
            
            
            #Selection:
            parent1=rd.choice(P)
            parent2=rd.choice(P)
            while parent1==parent2:
                parent2=rd.choice(P)
            #Croisement:
            fils1, fils2 = croisement(parent1,parent2)
            #Mutation:
            if(rd.random()<Pm):
                fils1 = mutation(fils1,COLORS[:p])
            if(rd.random()<Pm):
                fils2 = mutation(fils2,COLORS[:p])
            
            #Insertion:
            Pp.append(fils1)
            Pp.append(fils2)
        P=Pp
    
        #On regarde dans Pp les nouvelles combinaisons compatibles
        for e in P:
            if check_constraints_satisfaction(constraint, e) and e not in E:
                E.append(e)
                
        if len(E)>= maxSize:
            break
        k+=1
    return E
