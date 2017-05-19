import random,math
from shutil import copyfile
from pyx import *
from math import sqrt
def ABC(x,A,B,C): #0
 xA=sqrt(pow(x[0]-A[0],2)+pow(x[1]-A[1],2))
 xB=sqrt(pow(x[0]-B[0],2)+pow(x[1]-B[1],2))
 xC=sqrt(pow(x[0]-C[0],2)+pow(x[1]-C[1],2))
 if(xA<A[2] and xB<B[2] and xC<C[2]):
  return 1
 else:
  return 0
def nABC(x,A,B,C): #1
 xA=sqrt(pow(x[0]-A[0],2)+pow(x[1]-A[1],2))
 xB=sqrt(pow(x[0]-B[0],2)+pow(x[1]-B[1],2))
 xC=sqrt(pow(x[0]-C[0],2)+pow(x[1]-C[1],2))
 if(xA>A[2] and xB<B[2] and xC<C[2]):
  return 1
 else:
  return 0
def AnBC(x,A,B,C): #2
 xA=sqrt(pow(x[0]-A[0],2)+pow(x[1]-A[1],2))
 xB=sqrt(pow(x[0]-B[0],2)+pow(x[1]-B[1],2))
 xC=sqrt(pow(x[0]-C[0],2)+pow(x[1]-C[1],2))
 if(xA<A[2] and xB>B[2] and xC<C[2]):
  return 1
 else:
  return 0
def ABnC(x,A,B,C): #3
 xA=sqrt(pow(x[0]-A[0],2)+pow(x[1]-A[1],2))
 xB=sqrt(pow(x[0]-B[0],2)+pow(x[1]-B[1],2))
 xC=sqrt(pow(x[0]-C[0],2)+pow(x[1]-C[1],2))
 if(xA<A[2] and xB<B[2] and xC>C[2]):
  return 1
 else:
  return 0
def nAnBC(x,A,B,C): #4
 xA=sqrt(pow(x[0]-A[0],2)+pow(x[1]-A[1],2))
 xB=sqrt(pow(x[0]-B[0],2)+pow(x[1]-B[1],2))
 xC=sqrt(pow(x[0]-C[0],2)+pow(x[1]-C[1],2))
 if(xA>A[2] and xB>B[2] and xC<C[2]):
  return 1
 else:
  return 0
def AnBnC(x,A,B,C): #5
 xA=sqrt(pow(x[0]-A[0],2)+pow(x[1]-A[1],2))
 xB=sqrt(pow(x[0]-B[0],2)+pow(x[1]-B[1],2))
 xC=sqrt(pow(x[0]-C[0],2)+pow(x[1]-C[1],2))
 if(xA<A[2] and xB>B[2] and xC>C[2]):
  return 1
 else:
  return 0
def nABnC(x,A,B,C): #6
 xA=sqrt(pow(x[0]-A[0],2)+pow(x[1]-A[1],2))
 xB=sqrt(pow(x[0]-B[0],2)+pow(x[1]-B[1],2))
 xC=sqrt(pow(x[0]-C[0],2)+pow(x[1]-C[1],2))
 if(xA>A[2] and xB<B[2] and xC>C[2]):
  return 1
 else:
  return 0
def nAnBnC(x,A,B,C):#7
 xA=sqrt(pow(x[0]-A[0],2)+pow(x[1]-A[1],2))
 xB=sqrt(pow(x[0]-B[0],2)+pow(x[1]-B[1],2))
 xC=sqrt(pow(x[0]-C[0],2)+pow(x[1]-C[1],2))
 if(xA>A[2] and xB>B[2] and xC>C[2]):
  return 1
 else:
  return 0
nforms=[ABC,nABC,AnBC,ABnC,nAnBC,AnBnC,nABnC,nAnBnC]
def FormStr(aa):
 global nforms
 if aa==nforms[0]:
  return '(x \\in A) \cap (x \\in B) \cap (x \\in C)'
 if aa==nforms[1]:
  return '(x \\notin A) \cap (x \\in B) \cap (x \\in C)'
 if aa==nforms[2]:
  return '(x \\in A) \cap (x \\notin B) \cap (x \\in C)'
 if aa==nforms[3]:
  return '(x \\in A) \cap (x \\in B) \cap (x \\notin C)'
 if aa==nforms[4]:
  return '(x \\notin A) \cap (x \\notin B) \cap (x \\in C)'
 if aa==nforms[5]:
  return '(x \\in A) \cap (x \\notin B) \cap (x \\notin C)'
 if aa==nforms[6]:
  return '(x \\notin A) \cap (x \\in B) \cap (x \\notin C)'
 if aa==nforms[7]:
  return '(x \\notin A) \cap (x \\notin B) \cap (x \\notin C)'

def FormStr0(aa):
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
  
def PrintCirq0(cname):
 global nforms
 ccc=canvas.canvas()
 A=[-0.5,0,1]
 B=[0.5,0,1]
 C=[0,1,1]
 ccc.stroke(path.circle(A[0],A[1],A[2]))
 ccc.stroke(path.circle(B[0],B[1],B[2]))
 ccc.stroke(path.circle(C[0],C[1],C[2]))
 pp=[]
 uf=[]
 for i in range(1,5):
  x=random.random()*3-1.5
  y=random.random()*4-1 
  pp.append((x,y))
  #ccc.fill(path.circle(x,y,0.05))
  for i in range(0,8):
   if nforms[i]((x,y),A,B,C):
    uf.append(i)
    print (nforms[i])
 ir=100
 for ix in range(-ir,ir,3):
  for iy in range(-ir,ir+ir/4,3):
   x=2.*ix/ir
   y=2.*iy/ir
   for f in uf:
    if nforms[f]((x,y),A,B,C):
     ccc.stroke(path.circle(x,y,0.01))       
 ccc.writeEPSfile(cname)
 return set(uf)

def PrintCirq1(cname,imax):
 global nforms
 ccc=canvas.canvas()
 xA=random.random()/2-0.5
 yA=random.random()/4-0.25
 rA=random.random()+0.3
 xB=random.random()/2+0.5
 yB=random.random()/4-0.25
 rB=random.random()+0.3
 if(rB>1):
  rB=rB-0.4
 xC=random.random()/4-0.25
 yC=random.random()/2+0.5
 rC=random.random()+0.3
 if(rC>1):
  rC=rC-0.4
 A=[xA,yA,rA]
 B=[xB,yB,rB]
 C=[xC,yC,rC]
 
 pp=[]
 fnums=[0,1,2,3,4,5,6,7]
 random.shuffle(fnums)
 uf=[]
 for i in range(0,imax):
  uf.append(fnums[i])
  print (nforms[uf[i]])
 ir=100
 for ix in range(-ir,ir,3):
  for iy in range(-ir,ir+int(ir/4),3):
   x=2.*ix/ir
   y=2.*iy/ir
   for f in uf:
    if nforms[f]((x,y),A,B,C):
     ccc.stroke(path.circle(x,y,0.01),[color.gray(0.5)])   
 ccc.stroke(path.circle(A[0],A[1],A[2]))
 ccc.stroke(path.circle(B[0],B[1],B[2]))
 ccc.stroke(path.circle(C[0],C[1],C[2]))
 ccc.stroke(path.rect(-2, -2, 4, 4.5))
 ccc.text(A[0]-A[2],A[1]-A[2], "A", [text.size(2),text.mathmode, text.vshift.mathaxis,text.halign.boxcenter])
 ccc.text(B[0]+B[2],B[1]-B[2], "B", [text.size(2),text.mathmode, text.vshift.mathaxis,text.halign.boxcenter])
 ccc.text(C[0],C[1]+C[2]+0.2, "C", [text.size(2),text.mathmode, text.vshift.mathaxis,text.halign.boxcenter])
 ccc.text(-1.75,2.1, "U", [text.size(2),text.mathmode, text.vshift.mathaxis,text.halign.boxcenter])
     
 ccc.writeEPSfile(cname)
 return set(uf)
 
 
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
for i in range(0,5):
    tex_file.write("\\begin{figure}[!htb]\n")
    tex_file.write("\\centering\n")
    cname='circl'+str(i)
    cn=[]
    uf=[]
    for j in range(0,4):
     cn.append(cname+str(j))
     uf.append(PrintCirq1(cn[j],3))
    tex_file.write("\\caption{Задача "+str(i)+". Какому рисунку соответствует выражение: \\\\")
    fl=1
    rr=random.randint(0,3)
    res_file.write(str(i)+" - "+str(rr)+"\n")
    tex_file.write("$")
    for j in uf[rr]:
     if not fl:
      tex_file.write(' \\cup ')
     tex_file.write(FormStr(nforms[j]))
     fl=0
    tex_file.write("$}\n")
    #tex_file.write("\\includegraphics{"+cname+".eps}\n")
    tex_file.write("\\begin{subfigure}[t]{0.4\\textwidth}\n")
    tex_file.write("\\includegraphics{"+cn[0]+".eps}\n")
    tex_file.write("\\caption{ }\n")
    tex_file.write("\\end{subfigure}\n")
    tex_file.write("\\begin{subfigure}[t]{0.4\\textwidth}\n")
    tex_file.write("\\includegraphics{"+cn[1]+".eps}\n")
    tex_file.write("\\caption{ }\n")
    tex_file.write("\\end{subfigure}\n")
    tex_file.write("\n\\bigskip\n\\vskip 2cm\n\n")
    tex_file.write("\\begin{subfigure}[t]{0.4\\textwidth}\n")
    tex_file.write("\\includegraphics{"+cn[2]+".eps}\n")
    tex_file.write("\\caption{ }\n")
    tex_file.write("\\end{subfigure}\n")
    tex_file.write("\\begin{subfigure}[t]{0.4\\textwidth}\n")
    tex_file.write("\\includegraphics{"+cn[3]+".eps}\n")
    tex_file.write("\\caption{ }\n")
    tex_file.write("\\end{subfigure}\n")   
    tex_file.write("\\end{figure}\n")

tex_file.write("\\end{document}\n")
 
