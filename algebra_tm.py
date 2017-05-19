import random

def test_union(a):
    return sum([(i|j not in a) for i in a for j in a])

def test_intersection(a):
    return sum([(i&j not in a) for i in a for j in a])

def test_zazhig(a):
    return sum([(i^j not in a) for i in a for j in a])

def test_dif(a):
    return sum([(i-j not in a) for i in a for j in a])
def MakeAlgebraTM(aFl=[1,1,1,1]):
 nt=10000
 for i in range(0,nt):
  A0=[random.randint(1,4) for i in range(1,10)]
  A1=set([frozenset([random.randint(A0[7],A0[7]+4) for i in range(0,A0[j])]) for j in range(0,4)])
  A2=set([i^j for i in A1 for j in A1])
  A=A1|A2
  ta=(test_union(A),test_intersection(A),test_zazhig(A),test_dif(A))
  ta1=[int(i==0) for i in ta]
  #print(ta1)
  #print(aFl)
  if(aFl == ta1):
      return [list(j) for j in A]


      
def MakeAlgebraTM0():
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
#print(MakeAlgebraTM([0,0,0,1]))
#print(MakeAlgebraTM([0,0,1,0]))#
#print(MakeAlgebraTM([0,0,1,1]))
#print(MakeAlgebraTM([0,1,0,0]))#
#print(MakeAlgebraTM([0,1,0,1]))#
#print(MakeAlgebraTM([0,1,1,1]))
#print(MakeAlgebraTM([1,0,0,1]))
#print(MakeAlgebraTM([1,0,1,0]))
#print(MakeAlgebraTM([1,0,1,1]))
#print(MakeAlgebraTM([1,1,0,0]))
#print(MakeAlgebraTM([1,1,0,1]))
#print(MakeAlgebraTM([1,1,1,0]))
#print(MakeAlgebraTM([1,1,1,1]))
#print(MakeAlgebra())