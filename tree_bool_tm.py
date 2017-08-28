import random,sys,math
from shutil import copyfile
from pyx import *
from tex_structures_tm import MakeTable
from tex_structures_tm import MakeMatrix
#sys.path.append('./tmUI.py')
#from tmUI import MakeMatrix

# for constructing boolean function tasks simple binary tree
# in this implementation, a node is inserted between an existing node and the root
BoolOperands=['\\wedge','\\vee','\\rightarrow','\\leftrightarrow','|','\\downarrow','\\oplus']
BoolOrder=   [0       ,   1    ,       2      ,         3        , 0 ,     0       ,    3]
varNames=    ['x_1','x_2','x_3','x_4']
varNamesSet0=['A','B','C','D']
varNamesSet= ['(x \\in A)','(x \\in B)','(x \\in C)','(x \\in D)']
varNamesSetNeg= ['(x \\notin A)','(x \\notin B)','(x \\notin C)','(x \\notin D)']
BoolOperandsSet=['\\cap','\\cup','\\rightarrow','\\leftrightarrow','|','\\downarrow','\\Delta']
#varNames=    ['A','B','C','D']
#varVal  =    [170,204,240]
#varVal  =    [43690,52428,61680,65280]
varVal  =    [65280,61680,52428,43690]
#1100110011001100
#1111000011110000
#1111111100000000
def NtoList(iPerf):
 ff=[]
 i=0
 while (iPerf>0):
  if(iPerf%2):
   ff.append(i)
  i=i+1
  iPerf=iPerf>>1
 return ff
def DStrIbool(i,number_of_vars=4,knf=False):
 #analog of DStrI from optimal forms
 #lett=['x_1','x_2','x_3','x_4','E','F','G']
 xxi=[NtoListB(varVal[k],16) for k in range(0,number_of_vars)]
 strf=''
 f=i
 first=1
 for ii in range(0,number_of_vars):
  if not first:
   if(knf):
    strf+=' \\vee '   
   else:
    #strf+=' \\wedge '
    strf+='\\;'
  else:
   first=0
  if(xxi[ii][f]):
   if knf:
    #strf+='\\neg '
    strf+='\\overline{'
   strf+=varNames[ii]
   if knf:
    strf+='}'
  else:
   if not knf:
    #strf+='\\neg '
    strf+='\\overline{'
   strf+=varNames[ii]
   if not knf:
    #strf+='\\neg '
    strf+='}'
 return strf

def DStrIboolSet(i,number_of_vars=4,knf=False):
 xxi=[NtoListB(varVal[k],16) for k in range(0,number_of_vars)]
 strf=''
 f=i
 first=1
 for ii in range(0,number_of_vars):
  if not first:
   if(knf):
    strf+=BoolOperandsSet[1]
   else:
    strf+=BoolOperandsSet[0]
  else:
   first=0
  if(xxi[ii][f]):
   if knf:
    strf+=varNamesSetNeg[ii]
   else: 
    strf+=varNamesSet[ii]
  else:
   if not knf:
    strf+=varNamesSetNeg[ii]
   else: 
    strf+=varNamesSet[ii]
 return strf
 
 
def DStrFromNbool(n,number_of_vars=4,knf=False):
 #analog of DStrFromN from optimal forms
 if knf:
  ff=NtoList(DoNeg(n,nb=16))
 else:
  ff=NtoList(n)
 strf=''
 first=1
 for f in ff:
  if number_of_vars==3 and f%2:
   continue
  if not first:
   if knf:
    #strf+='\\wedge '
    strf+=''
   else:
    strf+='\\vee '
  else:
   first=0
  strf+='('+DStrIbool(f,number_of_vars,knf)+')'
 if strf=='':
   strf='\\emptyset'
 return strf

def DStrFromNboolSet(n,number_of_vars=4,knf=False):
 if knf:
  ff=NtoList(DoNeg(n,nb=16))
 else:
  ff=NtoList(n)
 strf=''
 first=1
 for f in ff:
  if number_of_vars==3 and f%2:
   continue
  if not first:
   if knf:
    strf+=BoolOperandsSet[0]
   else:
    strf+=BoolOperandsSet[1]
  else:
   first=0
  strf+='('+DStrIboolSet(f,number_of_vars,knf)+')'
 if strf=='':
   strf='\\emptyset'
 return strf
 
 
def DoNeg(x1,nb=16):
 mask=pow(2,nb)-1
 return mask^x1
def DoOper(operand,x1,x2,nb=16):
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
    width=0
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

    def randTree(self,num_vars=4):
       if(not self.type):
        if(random.randint(0,1)):
          tt=random.randint(1,2)
          self.type=tt
          childvn=random.randint(0,num_vars-1)
          self.left=BinaryTree(childvn)
          self.right=BinaryTree((childvn+1)%num_vars)
       else:
        self.left.randTree(num_vars)
        self.right.randTree(num_vars)
def MakeFormulaFromTree(tree,oper):
    if tree != None:
        if(not tree.type):
          return (varNames[tree.var],varVal[tree.var],0)
        else:
           (lleft,lv,wl)=MakeFormulaFromTree(tree.getLeftChild(),tree.prob)
           (rright,rv,wr)=MakeFormulaFromTree(tree.getRightChild(),tree.prob)
           w=0
           if(wl==0):
            w+=0.5
           if(wr==0):
            w+=0.5
           tree.width=w+wl+wr 
           res=lleft+' '+BoolOperands[tree.prob]+' '+rright
           sign=''
           resv=DoOper(BoolOperands[tree.prob],lv,rv,16)
           if not tree.neg:
               sign='\\neg '
               resv=DoNeg(resv)
           if BoolOrder[oper]<=BoolOrder[tree.prob]:
               return (sign+'('+res+')',resv,tree.width)
           else:
              if(sign==''):
               return (res,resv,tree.width)
              else:
               return (sign+'('+res+')',resv,tree.width)
def plotBoolSchemElem(cc,operand,x,y,m):
    dm=0.1*m
    if operand == '\\wedge':
        #return x1 & x2
        cc.text(x+0.5*m,y+1.5*m, "$\&$",[text.halign.boxcenter])
        return
    if operand == '\\vee':
        #return x1 | x2
        cc.text(x+0.5*m,y+1.5*m, "$1$",[text.halign.boxcenter])
        return

    if operand == '\\rightarrow':
#        return (DoNeg(x1, nb)) | x2
        cc.text(x+0.5*m,y+1.5*m, "$1$",[text.halign.boxcenter])
        cc.stroke(path.circle(x, y+1.5*m, dm))
        return

    if operand == '\\leftrightarrow':
#        return DoNeg(x1 ^ x2, nb)
        cc.text(x + 0.5 * m, y + 1.5 * m, "$=1$",[text.halign.boxcenter])
        cc.stroke(path.circle(x+m, y+m, dm))
        return
    if operand == '|':
#        return DoNeg(x1 & x2, nb)
        cc.text(x+0.5*m,y+1.5*m, "$\&$",[text.halign.boxcenter])
        cc.stroke(path.circle(x+m, y+m, dm))
        return
    if operand == '\\downarrow':
#        return DoNeg(x1 | x2, nb)
        cc.text(x + 0.5 * m, y + 1.5 * m, "$1$",[text.halign.boxcenter])
        cc.stroke(path.circle(x+m, y+m, dm))
        return
    if operand == '\\oplus':
#        return x1 ^ x2
        cc.text(x + 0.5 * m, y + 1.5 * m, "$=1$",[text.halign.boxcenter])
        return


def paintTree(tree,lvl,x1,y1):
    #m=0.1
    m=0.7
    if tree != None:
        #BinaryTree.ccc.fill(path.circle(x1,y1,m))
        xr=x1-m*2
        yr=y1-m
        hvx=x1-m*3
        hv1y=y1+m/2
        hv2y=y1-m/2
        if(not tree.type):
          #BinaryTree.ccc.stroke(path.line(x1,y1,x1-m,y1))
          BinaryTree.ccc.text(x1-0.5*m-0.1,y1, "$"+varNames[tree.var]+"$")
          return
        else:
           if not tree.neg:
            BinaryTree.ccc.stroke(path.rect(xr,yr,m,m*2))
            plotBoolSchemElem(BinaryTree.ccc, '\\downarrow', xr, yr, m)
            BinaryTree.ccc.stroke(path.line(xr,y1,xr-m,y1))
            xr-=2*m
            hvx-=2*m
           BinaryTree.ccc.stroke(path.rect(xr,yr,m,m*2))
           plotBoolSchemElem(BinaryTree.ccc, BoolOperands[tree.prob], xr, yr, m)
           BinaryTree.ccc.stroke(path.line(x1,y1,x1-m,y1))
           BinaryTree.ccc.stroke(path.line(hvx,hv1y,hvx+m,hv1y))
           BinaryTree.ccc.stroke(path.line(hvx,hv2y,hvx+m,hv2y))
           multl=tree.left.width
           multr=tree.right.width
           ml2= 1 if multl else 0
           mr2= 1 if multr else 0
           yn1=hv1y+multl*m+ml2*0.1*m
           yn2=hv2y-multr*m-mr2*0.1*m
           lvl=lvl*0.5
           BinaryTree.ccc.stroke(path.line(hvx,hv1y,hvx,yn1))
           BinaryTree.ccc.stroke(path.line(hvx,hv2y,hvx,yn2))
           #BinaryTree.ccc.stroke(path.line(x1,y1,x2,y0))
           #BinaryTree.ccc.stroke(path.line(x1,y1,x2,y2))
           paintTree(tree.getLeftChild(),lvl,hvx,yn1)
           paintTree(tree.getRightChild(),lvl,hvx,yn2)

 
def writeHead(tex_file): 
 tex_file.write("\\documentclass[12pt]{article}\n")
 tex_file.write("\\usepackage{graphics}\n")
 tex_file.write("\\usepackage[cp1251]{inputenc}\n")
 tex_file.write("\\usepackage[russian]{babel}\n")
 tex_file.write("\\usepackage[left=1cm,right=1cm,top=0cm,bottom=2cm,bindingoffset=0cm]{geometry}\n")
 tex_file.write("\\usepackage{amsmath}\n")
 tex_file.write("\\usepackage{caption}\n")
 tex_file.write("\\usepackage{subcaption}\n")
 tex_file.write("\\begin{document}\n")
 tex_file.write("\\pagenumbering{gobble}\n")
 tex_file.write("\\captionsetup{labelformat=empty}\n")
 return
 
def MakeCarnoMap(tvect):
  ind3=[0,1,3,2,4,5,7,6]
  ind4=[0,1,3,2,4,5,7,6,12,13,15,14,8,9,11,10]
  xv= ['00','01','11','10']
  yv4=['00','01','11','10']
  yv3=['0','1']
  if len(tvect)==8:
   val=[tvect[i] for i in ind3]
#   return MakeTable('$x_1 \setminus x_2 x_3$',xv,yv3,val) 
   return MakeTable(' ',xv,yv3,val) 
  if len(tvect)==16:
   val=[tvect[i] for i in ind4]
#   return MakeTable('$x_1 x_2 \setminus x_3 x_4$',xv,yv4,val) 
   return MakeTable(' ',xv,yv4,val) 
   
 
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

 tex_file_sol=open('tree'+str(v_cou)+'_sol.tex','w')
 tex_cmp.write('latex tree'+str(v_cou)+'_sol.tex\n')
 tex_cmp.write('dvips  tree'+str(v_cou)+'_sol.dvi\n')
 tex_cmp.write('ps2pdf tree'+str(v_cou)+'_sol.ps\n')

 writeHead(tex_file)
 writeHead(tex_file_sol)
  
 for i in range(0,10):
    ((form1,nform2,w),cn)=MakeFormulaTM(5)
    trtab=[]
    xHead=['$'+a+'$' for a in varNames]
    yHead=[]
    Nl=NtoList(nform2)
    for jj in range(0,16):
     ljj=NtoListB(jj,4)
     ii=ljj[3]+2*ljj[2]+4*ljj[1]+8*ljj[0]
     if ii in Nl:
      yHead.append(1)
     else:
      yHead.append(0)
     trtab+=(NtoListB(ii,4))
    strtab=MakeTable('f',xHead,yHead,trtab) 
    #of = Optimize12Forms(forms1, forms2, nform2)
    #sof=DStrFrom123Forms(of)
    #tex_file.write("Вариант "+str(i)+":\n$$\n f(x_1,x_2,x_3,x_4)="+form1+'\n$$\n\\bigskip\n')
    tex_file.write("Вариант "+str(i)+":\n\\includegraphics{"+cn+"}\n\n\\bigskip\n")
    tex_file.write('\\bigskip\n\\noindent\\rule{\\textwidth}{0.4pt}\n\n\\bigskip\n')
    tex_file_sol.write("Вариант "+str(i)+":\n$$\n"+form1+'\n$$\n\\bigskip\n')
    #tex_file_sol.write('Perfect form '+str(i)+': \n$$\n'+DStrFromNbool(nform2)+'\n$$\n')
    #tex_file_sol.write('Perfect form opt '+str(i)+': \n$$\n'+sof+'\n')
    tex_file_sol.write("\\includegraphics{"+cn+"}\n")
    #tex_file.write('Truth table:\n'+MakeMatrix(trtab)+'\n')
    tex_file_sol.write('Truth table:\n'+strtab+'\n\n')
    tex_file_sol.write('\\noindent\\rule{\\textwidth}{0.4pt}\n\n')

 tex_file.write("\\end{document}\n")
 tex_file_sol.write("\\end{document}\n")
def SumNForms(ff,knf):
 if knf:
   r=pow(2,16)-1
 else: 
   r=0
 for f in ff:
  if knf:
   r=r&f
  else: 
   r=r|f
 return r
 
def FilterMarkForm(mf,n,knf):
  rez=mf
  for i in range(4,0,-1):
   for f in list(rez.keys()):
    if(len(rez[f])==i):
     ff={f2:rez[f2] for f2 in rez if not f2==f}
     if SumNForms(ff,knf)==n:
      del rez[f]
  return rez
  
def StrMarkForm(mf,sets,knf):
 first=0
 s=''
 ns=0
 for f in mf:
  if first:
   if sets:
    s+=' {} '.format(BoolOperandsSet[not knf])
   else:
    if not knf:
     s+=' {} '.format(BoolOperands[not knf])
    else:
     s+=' '
  if knf: 
   if len(mf[f])>1:  
    s+='('   
  first=1
  f1=0
  nw=pow(2,16)-1
  for ff in mf[f]:
   if f1:
       if sets:
        s+=' {} '.format(BoolOperandsSet[knf])
       else:
        if not knf:
         s+=' '
        else:
         s+=' {} '.format(BoolOperands[knf])
   f1=1 
   if ff>0:
    if sets:
     s+=varNamesSet[ff-1]
    else: 
     s+=varNames[ff-1]
    if knf:
     nw=nw|varVal[ff-1]
    else: 
     nw=nw&varVal[ff-1]
   else:
    if sets:
     s+=varNamesSetNeg[abs(ff)-1]
    else: 
     s+=' \\neg '+varNames[abs(ff)-1]
    if knf:
     nw=nw|DoNeg(varVal[abs(ff)-1])
    else: 
     nw=nw&DoNeg(varVal[abs(ff)-1])
  if knf:   
   if len(mf[f])>1:  
    s+=')' 
   ns=ns&nw
  else:   
   ns=ns|nw  
 print('ns=',ns)   
 return s   

def OptimalNew(n,knf=False):
# ((f,n,w),cn)=MakeFormulaTM(5,4)
# print(((f,n,w),cn))
 forms=[]
 op=BoolOperands[knf]
# forms.append({0:'0',1:'1'})
 forms.append({0:set([0]),pow(2,16)-1:set([10])})
 forms.append({})
 for i in range(4):
  forms[1][varVal[i]]=set([i+1])
  forms[1][DoNeg(varVal[i])]=set([-(i+1)])
#  forms[1][varVal[i]]=varNames[i]
#  forms[1][DoNeg(varVal[i])]='\\neg '+varNames[i]
 forms.append({})
 forms.append({})
 forms.append({})
 for i in range(2,5):
  for f1 in forms[1]:
   for fi in forms[i-1]:
    if not f1==fi: 
     r=DoOper(op,f1,fi,nb=16)
     f=forms[1][f1]|forms[i-1][fi]
     if r not in forms[i-2] and len(f)==i and r not in forms[0]:
       forms[i][r]=f
# for f in forms:
#  print(len(set(f))) 
# for f in forms[4]:
#  print('{:016b}'.format(f),f,forms[4][f]) 
 markform={}
 for ff in forms:
  for f in ff:
   if knf:
    if f|n==f:
     markform[f]=ff[f]
   else:  
    if f&n==f:
     markform[f]=ff[f]
 #print(forms)
# print(markform)
 filtform=FilterMarkForm(markform,n,knf)
 print(markform)
 ss=StrMarkForm(markform,False,knf)
 ss2=StrMarkForm(markform,True,knf)
 print(ss)
 if ss=='':
  return ('0','\\emptyset')
 return (ss,ss2)
 
def MakeFormulaTM(number_of_element=10,number_of_vars=4):
 number_of_chemes=10
 BinaryTree.id_count=1
 #varc=open('var_count','r')
 #v_cou=int(varc.readline())
 #varc.close()
 xx=4
 yy=2
 #v_cou+=1
 form=('',0,0)
 max_p=number_of_element*2
 while form[1]==0 or form[1]==(pow(2,16)-1):
     myTree1 = BinaryTree(1)
     while (BinaryTree.id_count!=max_p):
       BinaryTree.id_count = 1
       myTree1 = BinaryTree(1)
       for i in range(10):
         myTree1.randTree(number_of_vars)
     form=MakeFormulaFromTree(myTree1,0)
 print(form)
 varc=open('var_count','r')
 v_cou=int(varc.readline())
 varc.close()
 BinaryTree.ccc=canvas.canvas()
 text.set(text.LatexRunner)
 lvl=4
 paintTree(myTree1, lvl, 0, 5)
 BinaryTree.ccc.writeEPSfile("tree"+str(v_cou))
 vc=open('var_count','w')
 v_cou=v_cou+1
 vc.write(str(v_cou))
 vc.close()
 trtab=[]
 xHead=['$'+a+'$' for a in varNames]
 if number_of_vars==3:
  xHead.pop()
 yHead=[]
 Nl=NtoList(form[1])                                  #(form1,nform2,w)
 xxi=[NtoListB(varVal[k],16) for k in range(0,number_of_vars)]
 for jj in range(0,16):
  if number_of_vars==3 and jj%2:
   continue
  if jj in Nl:
   yHead.append(1)
  else:
   yHead.append(0)
  for kk in range(0,number_of_vars):
   trtab+=[xxi[kk][jj]]
 strtab=MakeTable('f',xHead,yHead,trtab,yAlign=0) 
 carno=MakeCarnoMap(yHead)
 optf=OptimalNew(form[1],False)
 optfk=OptimalNew(form[1],True)
 dnf=DStrFromNbool(form[1],number_of_vars,knf=False)
 knf=DStrFromNbool(form[1],number_of_vars,knf=True)
 return (form,"tree"+str(v_cou-1)+".eps",strtab,carno,optf[0],optfk[0],dnf,knf,optf[1],optfk[1])

def TestA(x,A): #1
 xA=math.sqrt(pow(x[0]-A[0],2)+pow(x[1]-A[1],2))
 if(xA<A[2]):
  return 1
 else:
  return 0
  
def CheckDForm(ff,x,y,AA,number_of_vars=3):
 xxi=[NtoListB(varVal[k],16) for k in range(0,number_of_vars)]
 for i in range(0,number_of_vars):
  bit=xxi[i][ff]     #f%2
  if bit!=TestA((x,y),AA[i]):
   return False
 return True


def PrintCirqPerf(iPerf,imax):
 varc=open('var_count','r')
 v_cou=int(varc.readline())
 varc.close() 
 ccc=canvas.canvas()
 AA=[]
 for i in range(0,imax):
  xA=0.4*math.cos(math.pi*2.*i/imax)
  yA=0.4*math.sin(math.pi*2.*i/imax)
  rA=0.75
  A=[xA,yA,rA]
  AA.append(A)
 ff=NtoList(iPerf)
 print(ff)
 ir=100
 for ix in range(-ir,ir,3):
  for iy in range(-ir,ir,3):
   x=2.*ix/ir
   y=2.*iy/ir
   for f in ff:
    if CheckDForm(f,x,y,AA):
     ccc.stroke(path.circle(x,y,0.01),[color.gray(0.5)])
 for A in AA:
  ccc.stroke(path.circle(A[0],A[1],A[2]))
 ccc.stroke(path.rect(-2, -2, 4, 4))
 for i in range(0,3):
  ccc.text(AA[i][0]*4,AA[i][1]*4, varNamesSet0[i], [text.size(2),text.mathmode, text.vshift.mathaxis,text.halign.boxcenter])
 ccc.text(-1.75,1.7, "U", [text.size(2),text.mathmode, text.vshift.mathaxis,text.halign.boxcenter])
 cname="venn"+str(v_cou)
 ccc.writeEPSfile(cname)
 v_cou=v_cou+1
 vc=open('var_count','w')
 vc.write(str(v_cou))
 vc.close()
 return cname

 
def MakeControlTaskFormulas(nOfTasks=10,nQuest=3,qtt=[1,1,2],qcompl=[5,5,5],qvar=[3,4,4]):
#task type:
#1 - formula
#2 - scheme
#3 - Karnaugh map
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
 fname="BF"+str(nOfTasks)+"_"+str(nQuest)
 print(fname)
 tex_file=open(fname+'.tex','w')
 tex_cmp=open('cmp_tex.bat','w')
 tex_cmp.write('latex '+fname+'.tex\n')
 tex_cmp.write('dvips  '+fname+'.dvi\n')
 tex_cmp.write('ps2pdf '+fname+'.ps\n')

 tex_file_sol=open(fname+'_sol.tex','w')
 tex_cmp.write('latex '+fname+'_sol.tex\n')
 tex_cmp.write('dvips  '+fname+'_sol.dvi\n')
 tex_cmp.write('ps2pdf '+fname+'_sol.ps\n')

 writeHead(tex_file)
 writeHead(tex_file_sol)
 iNewPage=0
 for i in range(0,nOfTasks):
  tex_file.write('\\bigskip\n\\noindent\\rule{\\textwidth}{0.4pt}\n\n\\bigskip\n')
#  if(i and not i%3):
#   tex_file.write("\\newpage\n")
  tex_file.write("\\begin{minipage}{\\textwidth}\n")  
  tex_file.write("Вариант "+str(i)+":\n\n")
  tex_file_sol.write("Вариант "+str(i)+':\n')
  for j in range(0,nQuest):
    iNewPage+=1
    ((form1,nform2,w),cn,strtab,carno,optf,optfk,dnf,knf,dnfs,knfs)=MakeFormulaTM(qcompl[j],qvar[j])
    dnfset=DStrFromNboolSet(nform2,qvar[j],knf=False)
    knfset=DStrFromNboolSet(nform2,qvar[j],knf=True)
    venn=''
    if qvar[j]==3:
     venn=PrintCirqPerf(nform2,3)
    #of = Optimize12Forms(forms1, forms2, nform2)
    #sof=DStrFrom123Forms(of)
    #tex_file.write("Вариант "+str(i)+":\n$$\n f(x_1,x_2,x_3,x_4)="+form1+'\n$$\n\\bigskip\n')
    arg=varNames[0]
    for k in range(1,qvar[j]):
     arg+=","+varNames[k]
    if(qtt[j]==2):
     tex_file.write("Задача "+str(i)+"."+str(j+1)+":\n\\includegraphics{"+cn+"}\n\n")
    if(qtt[j]==1):
     tex_file.write("Задача "+str(i)+"."+str(j+1)+":\n$f("+arg+")="+form1+"$\n\n")
    if(qtt[j]==3):
     tex_file.write("Задача "+str(i)+"."+str(j+1)+":\nКарта Карно: \n\n"+carno+"\n\n")
     
    #tex_file.write('\\bigskip\n\\noindent\\rule{\\textwidth}{0.4pt}\n\n\\bigskip\n')
    tex_file_sol.write("Задача "+str(i)+"."+str(j+1)+":\n$$\n"+form1+'\n$$\n\\bigskip\n')
    #tex_file_sol.write('Perfect form '+str(i)+': \n$$\n'+DStrFromNbool(nform2)+'\n$$\n')
    #tex_file_sol.write('Perfect form opt '+str(i)+': \n$$\n'+sof+'\n')
    if qvar[j]==3:
     tex_file_sol.write("\\includegraphics{"+venn+"}\n")
    tex_file_sol.write("\\includegraphics{"+cn+"}\n")
    #tex_file.write('Truth table:\n'+MakeMatrix(trtab)+'\n')
    tex_file_sol.write('Truth table:\n'+strtab+'\n\n')
    tex_file_sol.write('Karnaugh map:\n'+carno+'\n\n')
    tex_file_sol.write('Optimal form D:\n$'+optf+'$\n\n')
    tex_file_sol.write('Optimal form K:\n$'+optfk+'$\n\n')
    tex_file_sol.write('DNF :\n$'+dnf+'$\n\n')
    tex_file_sol.write('KNF :\n$'+knf+'$\n\n')
    tex_file_sol.write('DNFs :\n$'+dnfset+'$\n\n')
    tex_file_sol.write('KNFs :\n$'+knfset+'$\n\n')
    tex_file_sol.write('DNFs2 :\n$'+dnfs+'$\n\n')
    tex_file_sol.write('KNFs2 :\n$'+knfs+'$\n\n')
    tex_file_sol.write('\\noindent\\rule{\\textwidth}{0.4pt}\n\n')
    #if(not iNewPage%2):
    # tex_file_sol.write("\\newpage\n")
  tex_file.write("\\end{minipage}\n\n")  

 tex_file.write("\\end{document}\n")
 tex_file_sol.write("\\end{document}\n")

#MakeForrest()
#print(MakeTreeTM())
#OptimalNew()
#print(MakeFormulaTM(number_of_element=7,number_of_vars=3))
#MakeForrestFormulas()
#random.seed(0)
#OptimalNewK()
#MakeControlTaskFormulas()
#MakeControlTaskFormulas(nOfTasks=2,nQuest=3,qtt=[1,1,2],qcompl=[5,5,5],qvar=[3,3,3])
#((form1,nform2,w),cn,strtab,carno,optf,optfk)=MakeFormulaTM(number_of_element=7,number_of_vars=4)
#print(nform2)
#print(form1)
#print(DStrFromNbool(nform2))

