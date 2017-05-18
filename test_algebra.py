import random

def test_union(a):
    return sum([(i|j not in a) for i in a for j in a])

def test_intersection(a):
    return sum([(i&j not in a) for i in a for j in a])

def test_zazhig(a):
    return sum([(i^j not in a) for i in a for j in a])

def test_dif(a):
    return sum([(i-j not in a) for i in a for j in a])
def MakeAlgebra(aFl=1):
 nt=10000
 for i in range(0,nt):
  A0=[random.randint(1,5) for i in range(1,10)]
  A1=set([frozenset([random.randint(A0[7],A0[7]+4) for i in range(0,A0[j])]) for j in range(0,4)])
  A2=set([i^j for i in A1 for j in A1])
  A=A1|A2
  if(not aFl and sum((test_union(A),test_intersection(A),test_zazhig(A),test_dif(A)))):
      return A
  if(aFl and not sum((test_union(A),test_intersection(A),test_zazhig(A),test_dif(A)))):
      return A
cou=[0,0,0,0]
nt=10
for i in range(0,nt):
 A=MakeAlgebra(aFl=1)
 tr=(test_union(A),test_intersection(A),test_zazhig(A),test_dif(A))
 if 0 in tr:
     print(A)
     print(tr)
     for i in range(0,4):
        if tr[i]==0:
            cou[i]+=1
print(cou,' from ',nt)
#test_union(A1)
#A2=set([i.union(j) for i in A1 for j in A1])
#print(A2)
#test_union(A2)
#test_intersection(A2)
