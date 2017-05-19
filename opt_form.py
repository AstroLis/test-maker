import random,math
from shutil import copyfile
from pyx import *
from math import sqrt

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

def NtoListB(iPerf,l):
 ff=[]
 for i in range(0,l):
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


def DStrFromN(n):
 ff=NtoList(n)
 strf=""
 first=1
 for f in ff:
  if not first:
   strf+='+'
  else:
   first=0
  strf+=DStrI(f)
 strf+=""
 if strf=="":
   strf="\\emptyset"
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
  return "\\emptyset"
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
  add=''
  if(f123[1]==3):
   f=GetBit(f123[0])
   add+=DStrI(f)
  if(f123[1]==2):
   add+=DStrFrom2fN(f123[0])
  if (f123[1] == 1):
   add +=DStrFrom1fN(f123[0])
  if(not add=='\\emptyset'):
   if not first:
    strf+='+'
   else:
    first=0
   strf+=add
 if strf=="":
   strf="\\emptyset "
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

def CheckBit(i,bit):
 return (i>>bit)%2

forms2=[]
tf=open('test_sm.txt','w')
tf.write("  0 1 2 3 4 5 6 7\n")
get_bin = lambda x, n: format(x, 'b').zfill(n)
for i in range(0,8):
 tf.write(str(i)+" ")
 for j in range(0,8):
  r=0
  if(CalcBits(i^j)==1):
   r=1
   forms2.append(pow(2,i)+pow(2,j))
  tf.write(str(r)+" ")
 tf.write("\n")
n_sets=3
nforms=pow(2,n_sets) 
adj_matr=[[int(CalcBits(i^j)==1) for i in range(0,nforms)] for j in range(0,nforms)]
print(adj_matr)
forms2=sorted(list(set(forms2)))
forms1=[]
for ib in range(0,3):
 t0=0
 t1=0
 for i in range(0,8):
  if CheckBit(i,ib):
   t0+=pow(2,i)
  else:
   t1 += pow(2, i)
 forms1.append(t0)
 forms1.append(t1)
forms1.append(0)
forms1.append(0)
print(forms1)


#for i in forms2:
# print(get_bin(i,8))
# for j in range(0,8):
#  print(CheckBit(i,j))

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
tex_file.write("\\usepackage[left=1cm,right=1cm,top=0cm,bottom=2cm,bindingoffset=0cm]{geometry}\n")
tex_file.write("\\usepackage{caption}\n")
tex_file.write("\\usepackage{subcaption}\n")
tex_file.write("\\begin{document}\n")
tex_file.write("\\pagenumbering{gobble}\n")
tex_file.write("\\captionsetup{labelformat=empty}\n")
#for i in range(0,len(forms2),4):
for i in range(100,108,4):
    tex_file.write("\\begin{figure}[!htb]\n")
    tex_file.write("\\centering\n")
    cname='circl'+str(i)
    cn=[]
    uf=[]
    for j in range(0,4):
     ind=j+i
     #ff=forms2[ind]
     ff=ind
     cn.append(cname+str(j))
     PrintCirqPerf(cname+str(j),ff,n_sets)
     #PrintCirqPerf(cname+str(j),ind,n_sets)
     #uf.append(DStrFromN(ff)+"="+DStrFrom2fN(ff)+"  "+str(VMprod(ff,adj_matr)))
     #uf.append(DStrFromN(ff) + "=" + DStrFrom1fN(ff))
     of=Optimize12Forms(forms1, forms2, ff)
     uf.append(DStrFromN(ff)+"="+DStrFrom123Forms(of))
    fl=1
    tex_file.write("\\begin{subfigure}[t]{0.4\\textwidth}\n")
    tex_file.write("\\includegraphics{"+cn[0]+".eps}\n")
    tex_file.write("\\caption{$"+uf[0]+"$}\n")
    tex_file.write("\\end{subfigure}\n")
    tex_file.write("\\begin{subfigure}[t]{0.4\\textwidth}\n")
    tex_file.write("\\includegraphics{"+cn[1]+".eps}\n")
    tex_file.write("\\caption{$"+uf[1]+"$}\n")
    tex_file.write("\\end{subfigure}\n")
    tex_file.write("\n\\bigskip\n\\vskip 2cm\n\n")
    tex_file.write("\\begin{subfigure}[t]{0.4\\textwidth}\n")
    tex_file.write("\\includegraphics{"+cn[2]+".eps}\n")
    tex_file.write("\\caption{$"+uf[2]+"$}\n")
    tex_file.write("\\end{subfigure}\n")
    tex_file.write("\\begin{subfigure}[t]{0.4\\textwidth}\n")
    tex_file.write("\\includegraphics{"+cn[3]+".eps}\n")
    tex_file.write("\\caption{$"+uf[3]+"$}\n")
    tex_file.write("\\end{subfigure}\n")
    tex_file.write("\\end{figure}\n")
    tex_file.write("\\clearpage\n")

tex_file.write("\\end{document}\n")
 
