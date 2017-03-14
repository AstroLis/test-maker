import random
from shutil import copyfile
from pyx import *

# for constructing boolean function tasks simple binary tree
# in this implementation, a node is inserted between an existing node and the root
BoolOperands=['\\wedge','\\vee','\\rightarrow','\\leftrightarrow','|','\\downarrow','\\oplus']
BoolOrder=   [0       ,   1    ,       2      ,         3        , 0 ,     0       ,    3]
varNames=    ['x_1','x_2','x_3']
varVal  =    [170,204,240]

def NtoList(iPerf):
 ff=[]
 i=0
 while (iPerf>0):
  if(iPerf%2):
   ff.append(i)
  i=i+1
  iPerf=iPerf>>1
 return ff
def DStrIbool(i):
 #analog of DStrI from optimal forms
 lett=['x_1','x_2','x_3','D','E','F','G']
 strf=''
 n=3
 f=i
 first=1
 for ii in range(0,3):
  if not first:
   strf+=' \\wedge '
  else:
   first=0
  bit=f%2
  if(bit):
   strf+=lett[ii]
  else:
   strf+='\\neg '+lett[ii]
  f=f>>1
 return strf

def DStrFromNbool(n):
 #analog of DStrFromN from optimal forms
 ff=NtoList(n)
 strf=''
 first=1
 for f in ff:
  if not first:
   strf+='\\vee '
  else:
   first=0
  strf+=DStrIbool(f)
 if strf=='':
   strf='\\emptyset'
 return strf

def DoNeg(x1,nb=8):
 mask=pow(2,nb)-1
 return mask^x1
def DoOper(operand,x1,x2,nb=8):
 mask=pow(2,nb)-1
 if operand=='\\wedge':
  return x1&x2
 if operand=='\\vee':
  return x1|x2
 if operand=='\\rightarrow':
  return (DoNeg(x1,nb))|x2
 if operand=='\\leftrightarrow':
  return DoNeg(x1^x2,nb)
 if operand=='|':
  return DoNeg(x1&x2,nb)
 if operand=='\\downarrow':
  return DoNeg(x1|x2,nb)
 if operand=='\\oplus':
  return x1^x2

def NtoListB(iPerf,l):
 ff=[]
 for i in range(0,l):
  ff.append(iPerf%2)
  iPerf=iPerf>>1
 return ff

def DStrI(i):
 lett=['A','B','C','D','E','F','G']
 strf=''
 n=3
 f=i
 first=1
 for ii in range(0,3):
  if not first:
   strf+=' \\cdot '
  else:
   first=0
  bit=f%2
  if(bit):
   strf+=lett[ii]
  else:
   strf+='\\overline{'+lett[ii]+'}'
  f=f>>1
 return strf


def DStrIMask(i,m):
 lett=['A','B','C','D','E','F','G']
 strf=''
 n=3
 f=i
 first=1
 for ii in range(0,3):
  bit=f%2
  f=f>>1
  mbit=m%2
  m=m>>1
  if(not mbit):
   if not first:
    strf+=' \\cdot '
   else:
    first=0
   if(bit):
    strf+=lett[ii]
   else:
    strf+='\\overline{'+lett[ii]+'}'
 return strf


def DStrFrom2fN(n):
 ff=NtoList(n)
 if not len(ff)==2:
  print('error in DStrFrom2fN, not 2forms:')
  print(ff)
  raise SystemExit(-1)
 mask=ff[0]^ff[1]
 #mask=7^mask
 #strf="$"
 strf=DStrIMask(ff[0],mask)
 #strf+="$"
 return strf

def DStrFrom1fN(n):
 ff=NtoList(n)
 if(len(ff)==0):
  return " \\emptyset "
 maskl=[0,0,0]
 mm=NtoListB(ff[0],3)
 for i in range(1,len(ff)):
  k=NtoListB(ff[i],3)
  for j in range(0,3):
   if not mm[j]==k[j]:
    maskl[j]=1
 mask=maskl[0]+maskl[1]*2+maskl[2]*4
 #strf="$"
 strf=DStrIMask(ff[0],mask)
 #strf+="$"
 return strf

def CalcNFromForms123(forms123):
 r=0
 for i in forms123:
  r=r|i[0]
 return r

def Filter3Forms(forms123,N):
  rez=forms123
  for f in forms123:
   if(f[1]==3):
    ff=[f3 for f3 in forms123 if not f3==f]
    if CalcNFromForms123(ff)==N:
     rez=Filter3Forms(ff,N)
  return rez

def Filter2Forms(forms123,N):
  rez=forms123
  for f in forms123:
   if(f[1]==2):
    ff=[f2 for f2 in forms123 if not f2==f]
    if CalcNFromForms123(ff)==N:
     rez=Filter2Forms(ff,N)
     break
  return rez

def Optimize12Forms(forms1,forms2,N):
 forms3=[pow(2,i) for i in range(0,8)]
 rf=[]
 for f in forms1:
  if f&N==f:
   rf.append((f,1))
 for f in forms2:
  if f & N == f:
   rf.append((f, 2))
 for f in forms3:
  if f & N == f:
   rf.append((f, 3))
 rf3=Filter3Forms(rf,N)
 rf2=Filter2Forms(rf3,N)
 return rf2

def GetBit(n):
 for j in range(0,8):
  if(n%2):
   return j
  n=n>>1

def DStrFrom123Forms(forms123):
 #ff=NtoList(n)
 strf=""
 first=1
 for f123 in forms123:
  if not first:
   strf+='+'
  else:
   first=0
  if(f123[1]==3):
   f=GetBit(f123[0])
   strf+=DStrI(f)
  if(f123[1]==2):
   strf+=DStrFrom2fN(f123[0])
  if (f123[1] == 1):
   strf +=DStrFrom1fN(f123[0])
 if strf=="":
   strf="\\emptyset "
 return strf

def CalcBits(i):
 bits=0
 f=i
 while f>0:
  bit=f%2
  f=f>>1
  bits+=bit
 return bits

def CheckBit(i,bit):
 return (i>>bit)%2


class BinaryTree():
    id_count=1
    probs=[]
    probs_all=[]
    ccc=canvas.canvas()
    bx = 0.8
    by = 0.4
    def __init__(self,vn):
      self.left = None
      self.right = None
      self.rootid = BinaryTree.id_count
      BinaryTree.id_count+=1
      self.dimx=0
      self.dimy=0
      self.type=0
      self.prob=random.randint(0,6)
      self.neg=random.randint(0,5)
      self.var=vn

    def getLeftChild(self):
        return self.left
    def getRightChild(self):
        return self.right
    def setNodeValue(self,value):
        self.rootid = value
    def getNodeValue(self):
        return self.rootid

    def randTree(self):
       if(not self.type):
        if(random.randint(0,1)):
          tt=random.randint(1,2)
          self.type=tt
          childvn=random.randint(0,2)
          self.left=BinaryTree(childvn)
          self.right=BinaryTree((childvn+1)%3)
       else:
        self.left.randTree()
        self.right.randTree()
def MakeFormulaFromTree(tree,oper):
    if tree != None:
        if(not tree.type):
          return (varNames[tree.var],varVal[tree.var])
        else:
           (lleft,lv)=MakeFormulaFromTree(tree.getLeftChild(),tree.prob)
           (rright,rv)=MakeFormulaFromTree(tree.getRightChild(),tree.prob)
           res=lleft+' '+BoolOperands[tree.prob]+' '+rright
           sign=''
           resv=DoOper(BoolOperands[tree.prob],lv,rv,8)
           if not tree.neg:
               sign='\\neg '
               resv=DoNeg(resv)
           if BoolOrder[oper]<BoolOrder[tree.prob]:
               return (sign+'('+res+')',resv)
           else:
               return (sign+res,resv)

def MakeFormulaTM(number_of_element=10):
 number_of_chemes=10
 BinaryTree.id_count=1
 #varc=open('var_count','r')
 #v_cou=int(varc.readline())
 #varc.close()
 xx=4
 yy=2
 #v_cou+=1
 max_p=number_of_element*2
 myTree1 = BinaryTree(1)
 while (BinaryTree.id_count!=max_p):
   BinaryTree.id_count = 1
   myTree1 = BinaryTree(1)
   for i in range(10):
     myTree1.randTree()
 form=MakeFormulaFromTree(myTree1,0)
 print(form)
 return form

def MakeForrestFormulas():
 forms2 = []
 for i in range(0, 8):
   for j in range(0, 8):
     r = 0
     if (CalcBits(i ^ j) == 1):
       r = 1
       forms2.append(pow(2, i) + pow(2, j))
 n_sets = 3
 nforms = pow(2, n_sets)
 forms2 = sorted(list(set(forms2)))
 forms1 = []
 for ib in range(0, 3):
        t0 = 0
        t1 = 0
        for i in range(0, 8):
            if CheckBit(i, ib):
                t0 += pow(2, i)
            else:
                t1 += pow(2, i)
        forms1.append(t0)
        forms1.append(t1)


 v_cou=0
 tex_file=open('tree'+str(v_cou)+'.tex','w')
 tex_cmp=open('cmp_tex.bat','w')
 tex_cmp.write('latex tree'+str(v_cou)+'.tex\n')
 tex_cmp.write('dvips  tree'+str(v_cou)+'.dvi\n')
 tex_cmp.write('ps2pdf tree'+str(v_cou)+'.ps\n')

 tex_file.write("\\documentclass[12pt]{article}\n")
 tex_file.write("\\usepackage{graphics}\n")
 tex_file.write("\\usepackage[cp1251]{inputenc}\n")
 tex_file.write("\\usepackage[russian]{babel}\n")
 tex_file.write("\\usepackage[left=1cm,right=1cm,top=0cm,bottom=2cm,bindingoffset=0cm]{geometry}\n")
 tex_file.write("\\usepackage{caption}\n")
 tex_file.write("\\usepackage{subcaption}\n")
 tex_file.write("\\begin{document}\n")
 tex_file.write("\\pagenumbering{gobble}\n")
 tex_file.write("\\captionsetup{labelformat=empty}\n")
 for i in range(0,100):
    (form1,nform2)=MakeFormulaTM(10)
    of = Optimize12Forms(forms1, forms2, nform2)
    sof=DStrFrom123Forms(of)
    tex_file.write("Formula "+str(i)+":\n$$\n")
    tex_file.write(form1+'\n$$\n Perfect form '+str(i)+': \n$$\n'+DStrFromNbool(nform2)+'\n$$\n')
    tex_file.write('Perfect form opt'+str(i)+': \n$$\n'+sof+'\n')
    tex_file.write("$$\n")

 tex_file.write("\\end{document}\n")
 
#MakeForrest()
#print(MakeTreeTM())

#MakeFormulaTM(10)
MakeForrestFormulas()