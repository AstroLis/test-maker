import random
import string
import copy
import graph_tm

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

     
def MakeSetTask():
    nn=[i+1 for i in range(8)]
    aa=[string.ascii_uppercase[i] for i in range(10)]
    random.shuffle(aa)    
    random.shuffle(nn)
#    A=nn[0]
#    B=frozenset(['A'])
#    C=frozenset(['B'])
#    D=frozenset(nn[1:4])
#    E=frozenset([nn[0]])
#    F=frozenset(nn[2:4])
#    G=frozenset(['D','F'])
    bb=['' for i in range(7)]
    bb[0]=str(nn[0])
    bb[1]=graph_tm.lts([aa[0].lower()])
    bb[2]=graph_tm.lts([aa[1]])
    bb[3]=graph_tm.lts(nn[1:4]+[graph_tm.lts([nn[0]])])
    bb[4]=graph_tm.lts([nn[0]])
    bb[5]=graph_tm.lts(nn[2:4])
    bb[6]=graph_tm.lts([bb[3],bb[5]])
    aa[0]=aa[0].lower()
    sets=['\\mbox{'+aa[i]+' = '+bb[i]+'}' for i in range(7)]
    str_sets=graph_tm.lts(sorted(sets),['',''])
    ri1=random.randint(1,6)
    ri2=random.randint(1,6)
#    cr=[aa[0]+' \\in '+aa[1], aa[0]+' \\notin '+aa[2],aa[1]+' \\in '+aa[2], aa[0]+' \\notin '+aa[3], aa[1]+' \\subseteq '+aa[4], aa[5]+' \\subset '+aa[3], aa[5]+' \\in '+aa[6]]
    cr=[aa[0]+' $\\in$ '+aa[1], aa[0]+' $\\notin$ '+aa[2],aa[1]+' $\\in$ '+aa[2], aa[0]+' $\\notin$ '+aa[3], aa[1]+' $\\subseteq$ '+aa[4], aa[5]+' $\\subset$ '+aa[3], aa[5]+' $\\in$ '+aa[6],'$\\emptyset$ $\\subseteq$ '+aa[ri1],'$\\emptyset$ $\\notin$ '+aa[ri2]]
#              A \in B,             A \notin C,              B \in C,             A \notin D,               B \subsetin E,             F \subset D,               F \in G,                       \emptyset \subseteq aa[ri1]
#    ncr=[aa[0]+' \\subseteq '+aa[1], aa[0]+' \\in '+aa[2],aa[1]+' \\subset '+aa[2], aa[0]+' \\in '+aa[3], aa[1]+' \\subset '+aa[4], aa[5]+' \\in '+aa[3], aa[5]+' \\subseteq '+aa[6]]
    ncr=[aa[0]+' $\\subseteq$ '+aa[1], aa[0]+' $\\in$ '+aa[2],aa[1]+' $\\subset$ '+aa[2], aa[0]+' $\\in$ '+aa[3], aa[1]+' $\\subset$ '+aa[4], aa[5]+' $\\in$ '+aa[3], aa[5]+' $\\subseteq$ '+aa[6],'$\\emptyset$ $\\in$ '+aa[ri1],'\{$\\emptyset$\} $\\subseteq$ '+aa[ri2]]
#              A \subsetin B,               A \in C,           B \subset C,                A \in D,               B \subset E,             F \in D,            F \subsetin G                        \emptyset \in aa[ri1]
    print(len(cr))
    wr=[i for i in range(len(cr))]
    random.shuffle(wr)
    wra=[]
    for i in range(3):
        #w=copy.copy(cr)
        w=cr[:wr[i]]+cr[wr[i]+1:]
        random.shuffle(w)
        #w[wr[i]]=ncr[wr[i]]
        w=w[0:3]+[ncr[wr[i]]]
        random.shuffle(w)
        wra.append(graph_tm.lts(w,[' ',' ']))
    random.shuffle(cr)
    return (str_sets,graph_tm.lts(cr[0:4],[' ',' ']),wra)

#a=MakeSetTask()
#print(a)
#print(a[1])
#print(graph_tm.lts(MakeSetTask()))

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


