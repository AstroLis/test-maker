import random
def MakeAlgebraTM():
         A0=[random.randint(2,4) for i in range(1,10)]
         A1=set([frozenset([random.randint(0,7) for i in range(0,A0[j])]) for j in range(0,4)])
        # B1=set([frozenset(sum([list(j) for j in A1],[]))])
        # B2=set([frozenset(frozenset.intersection(*A1))])
        # B3=A1|B1|B2
         B3=set([i.intersection(j) for i in A1 for j in A1])
         print(A1)
         print(B3)
         E=[list(j) for j in B3]
         return E
print(MakeAlgebraTM())