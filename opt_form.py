import random,math
from shutil import copyfile
from pyx import *
from math import sqrt
def FormStr(aa):
 global nforms
 if aa==nforms[0]:
  return '$A \cdot B \cdot C$'
 if aa==nforms[1]:
  return '$\overline{A} \cdot B \cdot C$'
 if aa==nforms[2]:
  return '$A \cdot \overline{B} \cdot C$'
 if aa==nforms[3]:
  return '$A \cdot B \cdot \overline{C}$'
 if aa==nforms[4]:
  return '$\overline{A} \cdot \overline{B} \cdot C$'
 if aa==nforms[5]:
  return '$A \cdot \overline{B} \cdot \overline{C}$'
 if aa==nforms[6]:
  return '$\overline{A} \cdot B \cdot \overline{C}$'
 if aa==nforms[7]:
  return '$\overline{A} \cdot \overline{B} \cdot \overline{C}$'
 
def TestA(x,A): #1
 xA=sqrt(pow(x[0]-A[0],2)+pow(x[1]-A[1],2))
 if(xA<A[2]):
  return 1
 else:
  return 0
  
def CheckDForm(ff,x,y,AA):
 f=ff
 for A in AA:
  bit=f%2
  f=f>>1
  if bit!=TestA((x,y),A):
   return False
 return True
  
def PrintCirq3(cname,imax):
 ccc=canvas.canvas()
 clippath = path.circle(0, 0, 1)
 drawpath = path.line(-2, -2, 1.2, 2)
 AA=[]
 for i in range(0,imax):
  xA=math.cos(math.pi*2.*i/imax)
  yA=math.sin(math.pi*2.*i/imax)
  rA=1.4
  A=[xA,yA,rA]
  AA.append(A)
  ccc.stroke(path.circle(A[0],A[1],A[2]))
 nf=[j for j in range(0,pow(2,imax))]
 random.shuffle(nf)
 maxf=10
 ff=[nf[ii] for ii in range(0,maxf)]
 print(ff)
 ir=100
 for ix in range(-ir,ir,3):
  for iy in range(-ir,ir,3):
   x=3.*ix/ir
   y=3.*iy/ir
   for f in ff:
    if CheckDForm(f,x,y,AA):
     ccc.stroke(path.circle(x,y,0.01))       
 ccc.writePDFfile(cname)
 return 0

def NtoList(iPerf):
 ff=[]
 i=0
 while (iPerf>0):
  if(iPerf%2):
   ff.append(i)
  i=i+1
  iPerf=iPerf>>1
 return ff

def NtoListB(iPerf):
 ff=[]
 for i in range(0,8):
  ff.append(iPerf%2)
  iPerf=iPerf>>1
 return ff


def PrintCirqPerf(cname,iPerf,imax):
 ccc=canvas.canvas()
 AA=[]
 for i in range(0,imax):
  xA=math.cos(math.pi*2.*i/imax)
  yA=math.sin(math.pi*2.*i/imax)
  rA=1.4
  A=[xA,yA,rA]
  AA.append(A)
 ff=NtoList(iPerf)
 print(ff)
 ir=100
 for ix in range(-ir,ir,3):
  for iy in range(-ir,ir,3):
   x=3.*ix/ir
   y=3.*iy/ir
   for f in ff:
    if CheckDForm(f,x,y,AA):
     ccc.stroke(path.circle(x,y,0.01),[color.gray(0.5)])
 for A in AA:
  ccc.stroke(path.circle(A[0],A[1],A[2]))
 #ccc.stroke(path.rect(-2, -2, 4, 4.5))
 #ccc.text(A[0]-A[2],A[1]-A[2], "A", [text.size(2),text.mathmode, text.vshift.mathaxis,text.halign.boxcenter])
 #ccc.text(B[0]+B[2],B[1]-B[2], "B", [text.size(2),text.mathmode, text.vshift.mathaxis,text.halign.boxcenter])
 #ccc.text(C[0],C[1]+C[2]+0.2, "C", [text.size(2),text.mathmode, text.vshift.mathaxis,text.halign.boxcenter])
 #ccc.text(-1.75,2.1, "U", [text.size(2),text.mathmode, text.vshift.mathaxis,text.halign.boxcenter])
 ccc.writeEPSfile(cname)
 return 0

def CalcBits(i):
 bits=0
 f=i
 while f>0:
  bit=f%2
  f=f>>1
  bits+=bit
 return bits

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

def DStrFromN(n):
 ff=NtoList(n)
 strf="$"
 first=1
 for f in ff:
  if not first:
   strf+='+'
  else:
   first=0
  strf+=DStrI(f)
 strf+="$"
 if strf=="$$":
   strf="$\\emptyset$"
 return strf

def VVprod(v1,v2):
 s=0
 for i in range(0,len(v1)):
  s+=v1[i]*v2[i]
 return s
 #return sum([a[0]*a[1] for a in list(zip(v1,v2))])

def VMprod(v,M):
 fv=NtoListB(v)
 r=[]
 for i in range(0,len(fv)):
  r.append(fv[i]*VVprod(fv,M[i]))
 return r


tf=open('test_sm.txt','w')
tf.write("  0 1 2 3 4 5 6 7\n")
for i in range(0,8):
 tf.write(str(i)+" ")
 for j in range(0,8):
  r=0
  if(CalcBits(i^j)==1):
   r=1
  tf.write(str(r)+" ")
 tf.write("\n")
n_sets=3
nforms=pow(2,n_sets) 
adj_matr=[[int(CalcBits(i^j)==1) for i in range(0,nforms)] for j in range(0,nforms)]  
print(adj_matr)


v_cou=0 
tex_file=open('cc'+str(v_cou)+'.tex','w')
tex_cmp=open('cmp_tex.bat','w')
res_file=open('result.txt','w')
tex_cmp.write('latex cc'+str(v_cou)+'.tex\n')
tex_cmp.write('dvips  cc'+str(v_cou)+'.dvi\n')
tex_cmp.write('ps2pdf cc'+str(v_cou)+'.ps\n')

tex_file.write("\\documentclass[12pt]{article}\n")
tex_file.write("\\usepackage{graphics}\n")
tex_file.write("\\usepackage[cp1251]{inputenc}\n")
tex_file.write("\\usepackage[russian]{babel}\n")
tex_file.write("\\usepackage[left=4cm,right=2cm,top=0cm,bottom=2cm,bindingoffset=0cm]{geometry}\n")
tex_file.write("\\usepackage{caption}\n")
tex_file.write("\\usepackage{subcaption}\n")
tex_file.write("\\begin{document}\n")
tex_file.write("\\pagenumbering{gobble}\n")
tex_file.write("\\captionsetup{labelformat=empty}\n")
for i in range(6,16,4):
    tex_file.write("\\begin{figure}[!htb]\n")
    tex_file.write("\\centering\n")
    cname='circl'+str(i)
    cn=[]
    uf=[]
    for j in range(0,4):
     cn.append(cname+str(j))
     PrintCirqPerf(cname+str(j),j+i,3)
     uf.append(DStrFromN(j+i)+"  "+str(VMprod(j+i,adj_matr)))
    fl=1
    tex_file.write("\\begin{subfigure}[t]{0.4\\textwidth}\n")
    tex_file.write("\\includegraphics{"+cn[0]+".eps}\n")
    tex_file.write("\\caption{"+uf[0]+"}\n")
    tex_file.write("\\end{subfigure}\n")
    tex_file.write("\\begin{subfigure}[t]{0.4\\textwidth}\n")
    tex_file.write("\\includegraphics{"+cn[1]+".eps}\n")
    tex_file.write("\\caption{"+uf[1]+"}\n")
    tex_file.write("\\end{subfigure}\n")
    tex_file.write("\n\\bigskip\n\\vskip 2cm\n\n")
    tex_file.write("\\begin{subfigure}[t]{0.4\\textwidth}\n")
    tex_file.write("\\includegraphics{"+cn[2]+".eps}\n")
    tex_file.write("\\caption{"+uf[2]+"}\n")
    tex_file.write("\\end{subfigure}\n")
    tex_file.write("\\begin{subfigure}[t]{0.4\\textwidth}\n")
    tex_file.write("\\includegraphics{"+cn[3]+".eps}\n")
    tex_file.write("\\caption{"+uf[3]+"}\n")
    tex_file.write("\\end{subfigure}\n")
    tex_file.write("\\end{figure}\n")
    tex_file.write("\\clearpage\n")

tex_file.write("\\end{document}\n")
 
