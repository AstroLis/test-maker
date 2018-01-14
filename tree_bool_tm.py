import random,sys,math
import numpy as np
from shutil import copyfile
from pyx import *
from tex_structures_tm import MakeTable
from graph_tm import dist_
from tex_structures_tm import MakeMatrix
#sys.path.append('./tmUI.py')
#from tmUI import MakeMatrix

# for constructing boolean function tasks simple binary tree
# in this implementation, a node is inserted between an existing node and the root
BoolOperands=['\\wedge','\\vee','\\rightarrow','\\leftrightarrow','|','\\downarrow','\\oplus']
BoolOrder=   [0       ,   1    ,       2      ,         3        , 0 ,     0       ,    3]
varNames=    ['x_1','x_2','x_3','x_4']
varNamesNeg=    ['\\bar{x}_1','\\bar{x}_2','\\bar{x}_3','\\bar{x}_4']
varNamesSet0=['A','B','C','D']
varNamesSet=[' A ',' B ',' C ',' D ']
varNamesSetNeg=['\\overline{A}','\\overline{B}','\\overline{C}','\\overline{D}']
varNamesSet1= ['(x \\in A)','(x \\in B)','(x \\in C)','(x \\in D)']
varNamesSetNeg1= ['(x \\notin A)','(x \\notin B)','(x \\notin C)','(x \\notin D)']
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
    strf+=varNamesNeg[ii]
   else:
    strf+=varNames[ii]
  else:
   if not knf:
    strf+=varNamesNeg[ii]
   else:
    strf+=varNames[ii]
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

def NtoListB(iPerf,l,nv=4):
 ff=[]
 for i in range(0,l):
  if not(nv==3 and i%2):
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
    def __init__(self,vn,basis=0):
      self.left = None
      self.right = None
      self.rootid = BinaryTree.id_count
      BinaryTree.id_count+=1
      self.dimx=0
      self.dimy=0
      self.type=0
      if not basis:
        self.prob=random.randint(0,6)
        self.neg=random.randint(0,5)
      elif basis==1: #Sheffer
        self.prob = 4
        self.neg = 1
      elif basis==2: #Pirs
        self.prob = 5
        self.neg = 1
      self.var=vn

    def getLeftChild(self):
        return self.left
    def getRightChild(self):
        return self.right
    def setNodeValue(self,value):
        self.rootid = value
    def getNodeValue(self):
        return self.rootid

    def randTree(self,num_vars=4,basis=0):
       if(not self.type):
        if(random.randint(0,1)):
          tt=random.randint(1,2)
          self.type=tt
          childvn=random.randint(0,num_vars-1)
          self.left=BinaryTree(childvn, basis)
          self.right=BinaryTree((childvn+1)%num_vars, basis)
       else:
        self.left.randTree(num_vars, basis)
        self.right.randTree(num_vars, basis)
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
        xr=x1-m*2
        yr=y1-m
        hvx=x1-m*2.5
        hv1y=y1+m/2
        hv2y=y1-m/2
#        hv1y=y1
#        hv2y=y1
        if(not tree.type):
          #BinaryTree.ccc.stroke(path.line(x1,y1,x1-m,y1))
          BinaryTree.ccc.text(x1-0.8*m-0.06,y1-0.2*m, "$"+varNames[tree.var]+"$",[text.size.LARGE])
          return
        else:
           if not tree.neg:
            BinaryTree.ccc.stroke(path.rect(xr,yr,m,m*2))
            plotBoolSchemElem(BinaryTree.ccc, '\\downarrow', xr, yr, m)
            BinaryTree.ccc.stroke(path.line(xr,y1,xr-0.5*m,y1))
            xr-=1.5*m
            hvx-=1.5*m
           BinaryTree.ccc.stroke(path.rect(xr,yr,m,m*2))
           plotBoolSchemElem(BinaryTree.ccc, BoolOperands[tree.prob], xr, yr, m)
           BinaryTree.ccc.stroke(path.line(x1,y1,x1-m,y1))
           BinaryTree.ccc.stroke(path.line(hvx,hv1y,hvx+0.5*m,hv1y))
           BinaryTree.ccc.stroke(path.line(hvx,hv2y,hvx+0.5*m,hv2y))
           multl=tree.left.width
           multr=tree.right.width
           ml2= 1 if multl else 0
           mr2= 1 if multr else 0
           yn1=hv1y+ml2*(multr)*(1+mr2*0.1)*m-ml2*mr2*m/2
           yn2=hv2y-mr2*(multl)*(1+ml2*0.1)*m+mr2*ml2*m/2
#           yn1=hv1y+multl*m+ml2*0.1*m
#           yn2=hv2y-multr*m-mr2*0.1*m
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
 tex_file.write("\\usepackage{multirow}\n")
 tex_file.write("\\usepackage{rotating}\n")
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
     tb='{'
     tb+=('\\footnotesize\n')
     tb+=('\\begin{tabular}{c|c|c|c|c|c|}\n') 
     tb+=('\\multicolumn{2}{c}{}&\\multicolumn{4}{c}{$x_3x_4$}\\\\\n') 
     tb+=('\\cline{3-6}\n') 
     tb+=('\\multicolumn{2}{c|}{}&\\tiny \\bf 00&\\tiny \\bf 01&\\tiny \\bf 11&\\tiny \\bf 10\\\\\n')  
     tb+=('\\cline{2-6}\n')  
     tb+=('\\multirow{4}{*}{ \\rotatebox[origin=c]{90}{$x_1x_2$}}\n') 
     id=0
     for y in yv4:
      tb+='&\\tiny \\bf '+(str(y))
      for x in xv:
       tb+=('&')
       tb+=(str(val[id]))
       id=id+1
      tb+=('\\\\ \\cline{2-6}')
     tb+=('\\end{tabular} }')
     return tb


   
 
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
     s+='\\;'
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
         s+='\\;'
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
#     s+=' \\neg '+varNames[abs(ff)-1]
#     s+=' \\overline{'+varNames[abs(ff)-1]+'}'
      s+=varNamesNeg[abs(ff)-1]
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
 
def MakeFormulaTM(number_of_element=10,number_of_vars=4,basis=0):
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
     myTree1 = BinaryTree(1,basis)
     while (BinaryTree.id_count!=max_p):
       BinaryTree.id_count = 1
       myTree1 = BinaryTree(1,basis)
       for i in range(10):
         myTree1.randTree(number_of_vars,basis)
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
 strtab=MakeTable('$f$',xHead,yHead,trtab,yAlign=0)
 carno=MakeCarnoMap(yHead)
 optf=OptimalNew(form[1],False)
 optfk=OptimalNew(form[1],True)
 dnf=DStrFromNbool(form[1],number_of_vars,knf=False)
 knf=DStrFromNbool(form[1],number_of_vars,knf=True)
 return (form,"tree"+str(v_cou-1)+".eps",strtab,carno,optf[0],optfk[0],dnf,knf,optf[1],optfk[1])

def TestA(x,A,number_of_vars=3): #1
 if number_of_vars==3:
     xA=math.sqrt(pow(x[0]-A[0],2)+pow(x[1]-A[1],2))
     if(xA<A[2]):
      return 1
     else:
      return 0
 if number_of_vars==4:
    cos_angle = np.cos(np.radians(180.-A[5]))
    sin_angle = np.sin(np.radians(180.-A[5]))

    xc = x[0] - A[6]
    yc = x[1] - A[7]

    xct = xc * cos_angle - yc * sin_angle
    yct = xc * sin_angle + yc * cos_angle 

    rad_cc = (xct**2/(A[3])**2) + (yct**2/(A[4])**2)
    if rad_cc<1:
        return 1
    else:
        return 0
  
def CheckDForm(ff,x,y,AA,number_of_vars=3):
 xxi=[NtoListB(varVal[k],16) for k in range(0,number_of_vars)]
 for i in range(0,number_of_vars):
  bit=xxi[i][ff]     #f%2
  if bit!=TestA((x,y),AA[i],number_of_vars):
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
 ccc.text(-1.65,1.6, "U", [text.size(2),text.mathmode, text.vshift.mathaxis,text.halign.boxcenter])
 cname="venn"+str(v_cou)
 ccc.writeEPSfile(cname)
 v_cou=v_cou+1
 vc=open('var_count','w')
 vc.write(str(v_cou))
 vc.close()
 return cname

#show Lotos-like Venn diagram for iPerf bool vector
def PrintEllipsePerf(iPerf,imax):
 varc=open('var_count','r')
 v_cou=int(varc.readline())
 varc.close() 
 ccc=canvas.canvas()
 sc=0.65
 AA=[(0,0,1,1*sc,2*sc,-50,  0.2*sc,1*sc-0.7),
     (0,0,1,1*sc,2*sc,-60,    1*sc,0*sc-0.7),
     (0,0,1,1*sc,2*sc,-120,  -1*sc,0*sc-0.7),
     (0,0,1,1*sc,2*sc,-130,-0.2*sc,1*sc-0.7)]
 ff=NtoList(iPerf)
 print(ff)
 ir=100
 for ix in range(-ir,ir,3):
  for iy in range(-ir,ir,3):
   x=2.*ix/ir
   y=2.*iy/ir
   for f in ff:
    if CheckDForm(f,x,y,AA,4):
     ccc.stroke(path.circle(x,y,0.01),[color.gray(0.5)])
 for A in AA:
  circ=path.circle(A[0],A[1],A[2])
  ccc.stroke(circ,[trafo.scale(sx=A[3],sy=A[4]),trafo.rotate(A[5]),trafo.translate(A[6],A[7])])
 ccc.stroke(path.rect(-2, -2, 4, 4))
 for i in range(1,3):
  ccc.text(AA[i][6]*4*sc,AA[i][7]*2*sc+1.3, varNamesSet0[i], [text.size(2),text.mathmode, text.vshift.mathaxis,text.halign.boxcenter])
 for i in [0,3]:
  ccc.text(AA[i][6]*8*sc,AA[i][7]*2*sc+1.3, varNamesSet0[i], [text.size(2),text.mathmode, text.vshift.mathaxis,text.halign.boxcenter])
 ccc.text(-1.65,1.6, "U", [text.size(2),text.mathmode, text.vshift.mathaxis,text.halign.boxcenter])
 cname="venn"+str(v_cou)
 ccc.writeEPSfile(cname)
# ccc.writePDFfile(cname)
 v_cou=v_cou+1
 vc=open('var_count','w')
 vc.write(str(v_cou))
 vc.close()
 return cname

#generate free-SDNF-cell bool vector
def GenerateNonOverlapCircles(nv=3):
  xyb=[[-0.5,-0.5],[0.5,-0.5],[-0.25,0.25]]
  sm=0.2
  AA=[]
  rb=0.2
  chk0=1
  fcf=[]
  rstr=''
  while chk0:
    rstr = ''
    fcf=[]
    AA = [[random.random()/2 + xyb[0][0], random.random()/4 + xyb[0][1], random.random() + rb],[0,0,0],[0,0,0]]
    chk=1
    while chk:
        AA[1][0] = random.random()/2 + xyb[1][0]  #xB = random.random() / 2 + 0.5
        AA[1][1] = random.random()/4 + xyb[1][1]  #yB = random.random() / 4 - 0.25
        AA[1][2] = random.random()*.7 + rb          #rB = random.random() + 0.3
        chk=(abs(-abs(dist_(AA[1],AA[0])-AA[0][2])+AA[1][2])<sm)

    chk=1
    while chk:
        AA[2][0] = random.random()/4 + xyb[2][0]
        AA[2][1] = random.random()/2 + xyb[2][1]
        AA[2][2] = random.random()*.7 + rb
        chk  = (abs(-abs(dist_(AA[2],AA[0])-AA[0][2])+AA[2][2])<sm)
        chk  = chk or (abs(-abs(dist_(AA[2], AA[1]) - AA[1][2]) + AA[2][2]) < sm)
        r12=AA[0][2]+AA[1][2]
        r1=AA[0][2]
        r2=AA[1][2]
        if not chk and dist_(AA[1],AA[0])<r12:
            x=[0,0]
            x[0] = AA[0][0] + (AA[1][0] - AA[0][0])*r1/r12
            x[1] = AA[0][1] + (AA[1][1] - AA[0][1])*r1/r12
            ax=dist_(AA[0],x)
            xr=math.sqrt(ax*ax+r1*r1)
            chk = (abs(-abs(dist_(AA[2], x) - xr) + AA[2][2]) < sm)
    iPerf=pow(2,16)-1
    ff = NtoList(iPerf)
    cf=[0 for a in ff]
    print(ff)
    ir = 100
    for ix in range(-ir, ir, 3):
        for iy in range(-ir, ir, 3):
            x = 2. * ix / ir
            y = 2. * iy / ir
            for f in range(0,len(ff)):
                if CheckDForm(ff[f], x, y, AA):
                    cf[f]=1
#                    ccc.stroke(path.circle(x, y, 0.01), [color.gray(0.5)])
    ccf=[]
    for i in range(0,len(cf)):
        if(i%2):
            ccf.append(cf[i])
            if cf[i]:
                if random.randint(1,3)==1:
                    fcf.append(ff[i])
                    rstr+='1'
                else:
                    rstr+='0'
            else:
                rstr+='{}-{}'

    print(cf)
    print(ccf)
    chk0=(sum(ccf)==8)
  print('fcf:',fcf)
  print('rstr:',rstr)
  varc = open('var_count', 'r')
  v_cou = int(varc.readline())
  varc.close()
  ccc = canvas.canvas()
  ir = 100
  for ix in range(-ir, ir, 3):
        for iy in range(-ir, ir, 3):
            x = 2. * ix / ir
            y = 2. * iy / ir
            for f in fcf:
                if CheckDForm(f, x, y, AA):
                     ccc.stroke(path.circle(x, y, 0.01), [color.gray(0.5)])
  for A in AA:
      ccc.stroke(path.circle(A[0], A[1], A[2]))
  ccc.stroke(path.rect(-2, -2, 4, 4))
  #for i in range(0, 3):
  ccc.text(AA[0][0]-AA[0][2]-0.1, AA[0][1] - AA[0][2]-0.1, varNamesSet0[0],
           [text.size(2), text.mathmode, text.vshift.mathaxis, text.halign.boxcenter])
  ccc.text(AA[1][0]+AA[1][2]+0.1, AA[1][1] + AA[1][2]+0.1, varNamesSet0[1],
           [text.size(2), text.mathmode, text.vshift.mathaxis, text.halign.boxcenter])
  ccc.text(AA[2][0], AA[2][1] + AA[2][2]+0.2, varNamesSet0[2],
           [text.size(2), text.mathmode, text.vshift.mathaxis, text.halign.boxcenter])
  ccc.text(-1.65, 1.6, "U", [text.size(2), text.mathmode, text.vshift.mathaxis, text.halign.boxcenter])

  cname = "venn" + str(v_cou)
  ccc.writeEPSfile(cname)
  #ccc.writePDFfile(cname)
  v_cou = v_cou + 1
  vc = open('var_count', 'w')
  vc.write(str(v_cou))
  vc.close()
  return (cname,'\\texttt{('+rstr+')}')

def PaintSDNFGraph(isdnf,knf=False,number_of_vars=3,mark_vert=True):
    varc = open('var_count', 'r')
    v_cou = int(varc.readline())
    if number_of_vars==3:
        s=1
        orts=((-math.sqrt(2)/2,-math.sqrt(2)/2),(1,0),(0,1))
        zc=(-0.2,-0.2)
        sc=1.8
        op=[(ort[0]*sc+ort[1]*0.3,ort[1]*sc+ort[0]*0.3) for ort in orts]
        od=[(ort[0]*sc,ort[1]*sc) for ort in orts]
    else:
        s=1.2
        orts=((-math.sqrt(2)/2*s*1.1,-math.sqrt(2)/2*s*1.1),(1*s,0),(0,1*s),(math.cos(13/16*math.pi)*s,math.sin(13/16*math.pi)*s))
        zc=(0.2,-0.5)
        sc=1.8    
        sc1=1.5
        sc2=1.4
        sc3=1.96
        sc4=2.1
        od=((orts[0][0]*sc1,orts[0][1]*sc1),
            (orts[1][0]*sc2,orts[1][1]*sc2),
            (orts[2][0]*sc3,orts[2][1]*sc3),
            (orts[3][0]*sc4,orts[3][1]*sc4))
        op=((od[0][0]-0.2,od[0][1]+0.2),
            (od[1][0]-0.1,od[1][1]+0.3),
            (od[2][0]+0.3,od[2][1]-0.05),
            (od[3][0]+0.2,od[3][1]+0.2))
    varc.close()
    ccc = canvas.canvas()
    cname = "sdnf_gr" + str(v_cou)
    ccc.stroke(path.rect(-2, -2, 4, 4))
    #ccc.writeEPSfile(cname)
    for i in range(0,len(orts)):
        ort=orts[i]
        ccc.stroke(path.line(*zc, zc[0]+od[i][0],zc[1]+od[i][1]), [deco.earrow([deco.filled()]),style.linestyle.dashed,style.linewidth(0.01)])
        ccc.text(zc[0]+op[i][0],zc[1]+op[i][1], varNames[i], [text.size(1), text.mathmode, text.vshift.mathaxis, text.halign.boxcenter])
    if knf:
        ff0=NtoList(DoNeg(isdnf))
    else:    
        ff0=NtoList(isdnf)
    ff=[]    
    for f in ff0:
        if number_of_vars==3 and f%2: continue
        ff.append(f)
    xxi=[NtoListB(varVal[k],16) for k in range(0,number_of_vars)]
    for f in ff:
        if number_of_vars==3 and f%2: continue
        x=zc[0]+sum([xxi[k][f]*orts[k][0] for k in range(0,number_of_vars)])
        y=zc[1]+sum([xxi[k][f]*orts[k][1] for k in range(0,number_of_vars)])
        if knf:
#            ccc.fill(path.circle(x, y, 0.1),[color.gray.white])
            ccc.stroke(path.circle(x, y, 0.1),[style.linewidth(0.03)])
        else:
            ccc.fill(path.circle(x, y, 0.1))
        if number_of_vars==3 :
            vnum=int(f/2)
        else:
            vnum=int(f)        
        if mark_vert:    
            ccc.text(x-0.15,y+0.2, str(vnum), [text.mathmode, text.vshift.mathaxis, text.halign.boxcenter])
        
    if number_of_vars==3:
        ffall=NtoList((pow(2,8)-1))  
    else:
        ffall=NtoList((pow(2,16)-1))  
    for if1 in range(0,len(ffall)):
        for if2 in range(if1,len(ffall)):
            f1=ffall[if1]
            f2=ffall[if2]
            if CalcBits(f1^f2)==1:
                ii1 = NtoListB(f1, 16)
                ii2 = NtoListB(f2, 16)
                x1 = zc[0] + sum([ii1[k] * orts[k][0] for k in range(0, number_of_vars)])
                y1 = zc[1] + sum([ii1[k] * orts[k][1] for k in range(0, number_of_vars)])
                x2 = zc[0] + sum([ii2[k] * orts[k][0] for k in range(0, number_of_vars)])
                y2 = zc[1] + sum([ii2[k] * orts[k][1] for k in range(0, number_of_vars)])
                ccc.stroke(path.line(x1, y1, x2, y2),
                           [style.linestyle.dashed,style.linewidth(0.01)])
    lff=len(ff)
    smezh=[[0 for i in range(0,lff)] for j in range(0,lff)]
    for i1 in range(lff):
        for i2 in range(i1,lff):
            f1=ff[i1]
            f2=ff[i2]
            if CalcBits(f1^f2)==1:
                x1 = zc[0] + sum([xxi[k][f1] * orts[k][0] for k in range(0, number_of_vars)])
                y1 = zc[1] + sum([xxi[k][f1] * orts[k][1] for k in range(0, number_of_vars)])
                x2 = zc[0] + sum([xxi[k][f2] * orts[k][0] for k in range(0, number_of_vars)])
                y2 = zc[1] + sum([xxi[k][f2] * orts[k][1] for k in range(0, number_of_vars)])
                dx=x2-x1
                dy=y2-y1
                r=math.sqrt(dx*dx+dy*dy)
                x1=x1+dx*0.1/r
                x2=x2-dx*0.1/r
                y1=y1+dy*0.1/r
                y2=y2-dy*0.1/r
                ccc.stroke(path.line(x1, y1, x2, y2),
                           [style.linewidth(0.03)])
                smezh[i1][i2]+=1
                smezh[i2][i1]+=1                           
    ccc.writeEPSfile(cname)
    v_cou = v_cou + 1
    vc = open('var_count', 'w')
    vc.write(str(v_cou))
    vc.close()
    return (cname,str(NtoListB(isdnf,16,number_of_vars)),smezh)


def MakeZazhigalkin(nA=5,nV=4):
 va=[i for i in range(0,16)]
 random.shuffle(va)
 rva=va[0:nA]
 strZ=''
 nZ=0
 vGr=[[],
      [0],[1],[2],[3],
      [0,1],[0,2],[0,3],[1,2],[1,3],[2,3],
      [0,1,2],[0,1,3],[0,2,3],[1,2,3],
      [0,1,2,3]]
 ffl=1     
 for i in range(0,16):
     if i in rva:
        term=pow(2,16)-1
        sterm=''
        for j in vGr[i]:
           sterm+=varNames[j]
           term=DoOper('\\wedge',term,varVal[j])
        if sterm=='': sterm='1'
        nZ=DoOper('\\oplus',nZ,term)
        if ffl :
            strZ+=sterm
            ffl=0
        else:
            strZ+='\\oplus '+sterm
 return (nZ,strZ)        

def MakeZazhigalkinTask(nA=5,number_of_vars=4,bOpt=True):
 form=MakeZazhigalkin(nA,number_of_vars)
 if bOpt:
    optf=OptimalNew(form[0],False)
    optfk=OptimalNew(form[0],True)
 dnf=DStrFromNbool(form[0],number_of_vars,knf=False)
 knf=DStrFromNbool(form[0],number_of_vars,knf=True)
 return (form[0],form[1],dnf,knf,optf[0],optfk[0])
 
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

#print(PaintSDNFGraph(random.randint(1,255)))
#GenerateNonOverlapCircles(nv=3)
#PrintEllipsePerf(52344,4)
#print(MakeZazhigalkinTask()) 
#MakeForrest()
#print(MakeTreeTM())
#OptimalNew()
#print(MakeFormulaTM(number_of_element=7,number_of_vars=3))
#MakeForrestFormulas()
#random.seed(9)
#OptimalNewK()
#MakeControlTaskFormulas(1,1,[1],[10],[4])
#MakeControlTaskFormulas(nOfTasks=2,nQuest=3,qtt=[1,1,2],qcompl=[5,5,5],qvar=[3,3,3])
#((form1,nform2,w),cn,strtab,carno,optf,optfk)=MakeFormulaTM(number_of_element=7,number_of_vars=4)
#print(nform2)
#print(form1)
#print(DStrFromNbool(nform2))

