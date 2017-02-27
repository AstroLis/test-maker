import random,math
import copy
from shutil import copyfile
from pyx import *

# simple binary tree
# in this implementation, a node is inserted between an existing node and the root


def dist_(d1,d2):
  return math.sqrt((d1[0]-d2[0])*(d1[0]-d2[0])+(d1[1]-d2[1])*(d1[1]-d2[1]))
def norm_(d1):
  dd=math.sqrt(d1[0]*d1[0]+d1[1]*d1[1])
  print(d1,dd)
  return (d1[0]/dd,d1[1]/dd)
def diff_(p1,p2):
  return (p2[0]-p1[0],p2[1]-p1[1])
def sc_p_(v1,v2):
  return v1[0]*v2[0]+v1[1]*v2[1]
  
def dist_p_l( P, P0,P1 ):
      v = diff_(P0,P1)
      w = diff_(P0,P)
      c1= sc_p_(w,v)
      if ( c1  <= 0 ):
            return dist_(P, P0)
      c2=sc_p_(v,v)      
      if ( c2  <= c1 ):
            return dist_(P, P1)
      b = c1 / c2 
      Pb = (P0[0] + b*v[0],P0[1] + b*v[1])
      return dist_(P, Pb)

def calc_path(p_t,ip,cp,fi):
       global all_path
       n_v=len(p_t[cp])
       ll=len(all_path[ip])
       if(ll):
        if(all_path[ip][ll-1][1]==0):
          print('problem')
       all_path[ip].append((cp,n_v))     
       if n_v==0:
         return
       pth=copy.deepcopy(p_t)
       currp=[]
       for t in all_path[ip]:#=copy.copy(all_path[ip])
        currp.append(t)       
       ll3=len(currp)
       if(ll3):
          if(currp[ll3-1][1]==0):
            print('problem3')
       ine=pth[cp][0]
       pth[cp].remove(ine)
       calc_path(pth,ip,ine,fi)
       if n_v==1:
         return         
       for ii in range(1,n_v):
         pth=copy.deepcopy(p_t)
         ine=pth[cp][ii]
         pth[cp].remove(ine)
         iip=len(all_path)
         all_path.append(copy.copy(currp))
         ll2=len(currp)
         if(ll2):
          if(currp[ll2-1][1]==0):
            print('problem2')
         calc_path(pth,iip,ine,fi)
       return         
         
  
def calc_cos(p0,p1,p2):
  return  sc_p_(diff_(p0,p1),diff_(p0,p2))/(dist_(p0,p1)*dist_(p0,p2))
# test tree


def MakeGraphTM(nv=5,directed=1,calc_random_path=1):
    random.seed()
    global id_count
    global ccc
    global probs
    global probs_all
    global all_path
    id_count = 1
    ccc = canvas.canvas()
    probs = []
    probs_all = []
    all_path = []
    varc=open('var_count','r')
    v_cou=int(varc.readline())
    varc.close()
    ii=1
    v_cou+=1
    print('ii=',ii)
    id_count = 1
    ccc=canvas.canvas()
    sc=4
    s1=2
    #nv=5
    do_work=1
    itry=0
    while do_work:
     print('try:',itry)
     itry=itry+1
     do_work=0
     probs=[]
     path_a=[]
     tc=0
     for jj in range(nv):
      dd=0
      d1=(random.random()*sc-s1,random.random()*sc-s1)
      if len(probs):
       while dd<sc/4:
        d1=(random.random()*sc-s1,random.random()*sc-s1)
        mind=sc
        for d2 in probs:
         if mind>dist_(d1,d2):
          mind=dist_(d1,d2)
        dd=mind
        tc=tc+1 
        if tc>100000 :
          do_work=1
          break
      if do_work:
       break      
      probs.append(d1)  
      nvi=random.randint(0,3)
      path_a.append([])
     if do_work:
      continue     
     fi=1
     curri=0
     pathc=0
     #path_a0=path_a
     path_to=[]
     tc=0
     while pathc<20:
      pathc=0
      path_a=[]
      path_to=[]
      tc=tc+1
      if tc>1000:
       do_work=1
       break
      for jj in range(nv):
       path_a.append([])
       path_to.append([])
      curri=0
      tc2=0
      while not curri==fi:
       inext=curri
       cosfrom=0.0
       costo=0.0
       mind=0.0
       while inext==curri or (curri in path_to[inext]) or cosfrom>0.9 or costo>0.9 or mind<0.3:
        inext=curri
        tc2=tc2+1
        if tc2>1000:
         do_work=1
         break
        while inext==curri: 
          inext=random.randint(0,nv-1)
        cs=0.0
        for p in path_a[curri]:
         c=abs(calc_cos(probs[curri],probs[p],probs[inext]))
         if(c>cs):
           cs=c 
        if(abs(cs-1.)<0.00000001):
          cs=0.0       
        cosfrom=cs
        cs=0.0
        for p in path_a[inext]:
         c=abs(calc_cos(probs[inext],probs[p],probs[curri]))
         if(c>cs):
           cs=c 
        if(abs(cs-1.)<0.00000001):
          cs=0.0       
        costo=cs
        md=sc
        for ip in range(nv):
         if (not ip==curri) and (not ip==inext):
          d=dist_p_l(probs[ip],probs[curri],probs[inext])
          if d<md:
           md=d
        mind=md   
       if do_work:
        break              
       path_a[curri].append(inext)   
       if not inext in path_to[curri]:        
         path_to[curri].append(inext)      
       path_a[inext].append(curri)
       pathc=pathc+1
       if(random.randint(0,1)):
        curri=inext
      if do_work:
       break                     
     if do_work:
      continue     
    
    probs_all=[]
    if(calc_random_path):
     ccc.fill(path.circle(probs[0][0],probs[0][1], 0.2))
     ccc.stroke(path.circle(probs[0][0],probs[0][1], 0.15))
     ccc.stroke(path.circle(probs[fi][0],probs[fi][1], 0.2))
    for jj in range(nv):
     pp=probs[jj]
     #if(directed):
     # ccc.stroke(path.circle(pp[0],pp[1], 0.1))
     #else:
     ccc.fill(path.circle(pp[0],pp[1], 0.1))
     
     for ph in path_to[jj]:
      dxx=pp[0]+(probs[ph][0]-pp[0])*2/3.
      dyy=pp[1]+(probs[ph][1]-pp[1])*2/3.
      if(directed):
       ccc.stroke(path.line(pp[0], pp[1], dxx, dyy),[deco.earrow([deco.filled()])])
      ccc.stroke(path.line(pp[0], pp[1], probs[ph][0],probs[ph][1]))
     text_d0=0.0
     text_d1=0.0
     for phi in path_a[jj]:
      if(not phi==jj):
       ph=probs[phi]
       print(pp,ph)
       d1=diff_(pp,ph)
       dd=math.sqrt(d1[0]*d1[0]+d1[1]*d1[1])
       text_d0+=d1[0]/dd
       text_d1+=d1[1]/dd
     if( not(text_d0==0 and text_d1==0)): 
      ntd=norm_((text_d0,text_d1)) 
     ccc.text(pp[0]-0.5*ntd[0],pp[1]-0.5*ntd[1], str(jj+1), [text.size(2),text.mathmode, text.vshift.mathaxis,text.halign.boxcenter])
    n_try=100
    n_f=0
    n_l=0
    for jj in range(n_try):
       pth=copy.deepcopy(path_to)
       strt=0
       iic=strt
       lost=0
       while not iic==fi:
        np=len(pth[iic])
        if not np:
         lost=1
         break
        p=random.randint(0,np-1) 
        i=pth[iic][p]
        pth[iic].remove(i)
        iic=i
       if lost:
        n_l=n_l+1
       else:
        n_f=n_f+1    
    all_path=[]
    all_path.append([])
    pth=copy.deepcopy(path_to)
    calc_path(pth,0,0,1)
    for kk in all_path:
      print(kk)
    grfile="graph"+str(v_cou)+".eps"
    ccc.writeEPSfile("graph"+str(v_cou))
    #ccc.writePDFfile("graph"+str(v_cou))
    maxL=0
    for tt in all_path:
     if(len(tt)>maxL):
      maxL=len(tt)
    f_prob=0.0
    for tt in all_path:
     mult=1
     for jj in range(maxL):
      if(jj<len(tt)): 
       if(jj<len(tt)-1):
        mult=mult*tt[jj][1]
     if(tt[len(tt)-1][0]==1):
      f_prob+=1./mult      
    vc = open('var_count', 'w')
    vc.write(str(v_cou))
    vc.close()
    incin=[]
    smezh=[[0 for i in range(0,nv)] for j in range(0,nv)]
    for i in range(0,nv):
     for p in path_to[i]:
      if directed:
       incin.append([0 if (not j==i and not j==p) else 1 if j==i else -1 for j in range(0,nv)])
      else:
       incin.append([0 if (not j==i and not j==p) else 1 for j in range(0,nv)])
      
      smezh[i][p]=1
      if not directed:
       smezh[p][i]=1         
    return (grfile,str(f_prob),incin,smezh)
#(a,b,incin,smezh)=MakeGraphTM(5,1)
#print('incinden:')    
#for i in incin:
# print (i)
#print('smzeh:')    
#for i in smezh:
# print (i)
 