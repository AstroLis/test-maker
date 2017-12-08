import random

def test_union(a):
    return sum([(i|j not in a) for i in a for j in a])

def test_union_monoid(a):
    return sum([sum([(i|j == i) for i in a])==len(a) for j in a])

def test_intersection_monoid(a):
    return sum([sum([(i&j == i) for i in a])==len(a) for j in a])

def test_zazh_monoid(a):
    return sum([sum([(i^j == i) for i in a])==len(a) for j in a])
    
def test_intersection(a):
    return sum([(i&j not in a) for i in a for j in a])

def test_zazhig(a):
    return sum([(i^j not in a) for i in a for j in a])

def test_dif(a):
    return sum([(i-j not in a) for i in a for j in a])
def MakeAlgebraTM(aFl=[1,1,1,1],i_mon=1):
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
      if(aFl==[0,1,0,0]):
       if(test_intersection_monoid(A)!=i_mon):
        continue
      return [list(j) for j in A]
      #return A

#for i in range(0,10):
#  a=MakeAlgebraTM([0,1,0,0],0)         
#  ii=test_union_monoid(a)
#  ii=test_intersection_monoid(a)
#  ii=test_zazh_monoid(a)
#  if(ii==0):
#   print([0,0,1,0],[list(j) for j in a])
#   print(ii)
#print([0,0,0,1],MakeAlgebraTM([0,0,0,1]))
#print([0,0,1,0],MakeAlgebraTM([0,0,1,0]))#
#print([0,0,1,1],MakeAlgebraTM([0,0,1,1]))
#print([0,1,0,0],MakeAlgebraTM([0,1,0,0]))#
#print([0,1,0,1],MakeAlgebraTM([0,1,0,1]))#
#print([0,1,1,0],MakeAlgebraTM([0,1,1,0]))#
#print([0,1,1,1],MakeAlgebraTM([0,1,1,1]))
#print([1,0,0,0],MakeAlgebraTM([1,0,0,0]))
#print([1,0,0,1],MakeAlgebraTM([1,0,0,1]))
#print([1,0,1,0],MakeAlgebraTM([1,0,1,0]))
#print([1,0,1,1],MakeAlgebraTM([1,0,1,1]))
#print([1,1,0,0],MakeAlgebraTM([1,1,0,0]))
#print([1,1,0,1],MakeAlgebraTM([1,1,0,1]))
#print([1,1,1,0],MakeAlgebraTM([1,1,1,0]))
#print([1,1,1,1],MakeAlgebraTM([1,1,1,1]))
##print(MakeAlgebra())
##
##
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#


