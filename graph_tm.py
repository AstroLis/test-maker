import random,math
import copy
import numpy as np
import networkx as nx
from shutil import copyfile
from pyx import *

def lts(lst,bb=['\\{','\\}']):
    rz=bb[0]
    f=0
    for i in lst:
        if f: rz+=', '
        f=1
        rz+=str(i)
    rz+=bb[1]
    return rz

def gr_tostr(gr):
    return '('+lts(gr[0])+', '+lts([lts(i,'()') for i in gr[1]])+')'

def wrong_graph(path_to):
    resp=copy.deepcopy(path_to)
    nv=len(resp)
    to_add=[]
    to_del=[]
    for i in range(nv):
        if len(resp[i]): to_del.append(i)
        if len(resp[i])<nv-1: to_add.append(i)
    ii_add=[i for i in to_add]
    ii_del=[i for i in to_del]
    random.shuffle(ii_add)
    random.shuffle(ii_del)
    ia=0
    if len(to_add):
        ia=ii_add[0]
        for i in range(nv):
            if i==ia: continue
            if i in resp[ia]: continue
            resp[ia].append(i)
            break
    for i in ii_del:
        if i==ia: continue
        resp[i].pop()
        break
    return resp
    

def gr_to_graph_tm(gr):
    print('gr_to_graph_tm: ',gr)
    nv = len(gr[0])
    vv=list(gr[0])
    vi={}
    iv={}
    path_to=[]
    path_all=[]
    for i in range(nv):
        path_all.append([])
        vi[i]=vv[i]
        iv[vv[i]]=i
    for i in range(nv):
        path_to.append([])
        for j in gr[1]:
            if j[0]==vi[i]:
                path_to[i].append(iv[j[1]])
                path_all[i].append(iv[j[1]])
            if j[1]==vi[i]:
                path_all[i].append(iv[j[0]])
    return (path_to,path_all)            
                
        
def graph_repr(path_to,directed=1,v_nams=[]):
    nv=len(path_to)
    weighted=0
    random_weights=0
    if v_nams==[]:
        for i in range(nv):
            v_nams.append(i+1)
    rv_nams=[]
    vi={}
    iv={}
    mi={}
    iii={}
    for i in range(nv):
        rv_nams.append(v_nams[i])
        vi[v_nams[i]]=i
        iv[i]=v_nams[i]
    vis=sorted(vi.keys())
    for i in range(len(vis)):
        mi[vis[i]]=i
        iii[vi[vis[i]]]=i
    incin = []
    smezh = [[0 for i in range(0, nv)] for j in range(0, nv)]
    edges=[]
    verts=[]
    edges_s=[]
    if directed:
        bb=['(',')']
    else:
        bb=['\\{','\\}']
    for ii in vi:
        edges+=[bb[0]+str(ii)+',~'+str(iv[j])+bb[1] for j in path_to[vi[ii]]]
        verts.append(str(ii)+': '+lts(sorted([iv[jj] for jj in path_to[vi[ii]]])))
        for j in path_to[vi[ii]]:
            edges_s.append((ii,iv[j]))
    repr_cl = '('+lts(sorted(vis))+', '+lts(sorted(edges))+')'
    repr_vrt =lts(sorted(verts),'  ')
    for ii in vi:
        i=vi[ii]
        for p in path_to[i]:
            if directed:
                incin.append([0 if (not vi[j] == i and not vi[j] == p) else 1 if vi[j] == i else -1 for j in vi])
            else:
                incin.append([0 if (not vi[j] == i and not vi[j] == p) else 1 for j in vi])
            if weighted:
                #sml = int(10 * dist_(probs[i], probs[p]))
                if random_weights:
                    sml = random.randint(1, 5)
            else:
                sml = 1
            smezh[iii[i]][iii[p]] = sml
            if not directed:
                smezh[iii[i]][iii[i]] = sml
    return (smezh,incin,repr_cl,repr_vrt,(set(vis),set(edges_s)))



        # simple binary tree
# in this implementation, a node is inserted between an existing node and the root
class NewGraph:
    def __init__(self,d=5,n=5,sym=False):
        if sym:
            a=np.random.randint(n, size=(d, d))
            self.smezh=np.tril(a,-1) + np.tril(a, -1).T
        else:
            self.smezh=np.random.randint(n, size=(d, d))

        print(self.smezh)

    def RemoveEdge(self):
        m=copy.copy(self.smezh)
        while True:
            for i in range(self.smezh.shape[0]):
                for j in range(self.smezh.shape[1]):
                    if random.randint(0,10)==5 and self.smezh[i,j]>0:
                        m[i, j]=self.smezh[i, j]-1
                        #print(self.smezh)
                        #print((i+1,j+1))
                        return (m,(i+1,j+1))
    def RemoveNodeI(self,i,m):
        a=np.delete(m,i,0)
        b = np.delete(a, i, 1)
        #self.smezh=b
        return b
    def RemoveNode(self):
        m=copy.copy(self.smezh)
        i=random.randint(0,self.smezh.shape[0]-1)
        return (self.RemoveNodeI(i,m),i + 1)
    def MergeNodeIJDel(self,i,j):
        m=copy.copy(self.smezh)
        m[i, j]=0
        m[j, i]=0
        m[:, i]=m[:,i]+m[:,j]
        m[i, :] = m[i, :] + m[j, :]
        return self.RemoveNodeI(j,m)
    def MergeNodeIJ(self,i,j):
        m=copy.copy(self.smezh)
        m[:, i]=m[:,i]+m[:,j]
        m[i, :] = m[i, :] + m[j, :]
        return self.RemoveNodeI(j,m)
    def kruskal(self):
        G=nx.from_numpy_matrix(self.smezh)
        G1=nx.minimum_spanning_tree(G)
        return nx.to_numpy_matrix(G1)
    def dijkstra1(self,i):
        G=nx.from_numpy_matrix(self.smezh,create_using=nx.MultiDiGraph())
        return nx.single_source_dijkstra(G,i)
        #return nx.bidirectional_dijkstra(G,i)


def grAnd(m1,m2):
    n=m1.shape[0]
    m=copy.copy(m1)
    for i in range(0,n):
        for j in range(0,n):
            m[i,j]=min(m1[i,j],m2[i,j])
    return m
def grOr(m1,m2):
    n=m1.shape[0]
    m=copy.copy(m1)
    for i in range(0,n):
        for j in range(0,n):
            m[i,j]=max(m1[i,j],m2[i,j])
    return m
def grMult(m1,m2):
    return np.matmul(m1,m2)


def MakeMatrix(data,ff=2):
 tb=''
 tb+=(' {$$ \\begin{pmatrix}')
 for y in data:
  i=0
  for x in y:
   if i:
    tb+='&'
   else:
    i=1   
   tb+=('{:g}'.format(x))
  tb+=('\\\\')
 tb+=(' \\end{pmatrix}$$}')
 return tb

def find_shortest_path(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not start in range(0,len(graph)):
            return None
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = find_shortest_path(graph, node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

def calc_len(smezh,path):
    l=0
    if len(path)<=1:
        return 0
    for i in range(0,len(path)-1):
        l+=smezh[path[i]][path[i+1]]
    return l

def find_shortest_path_smezh(smezh,graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not start in range(0,len(graph)):
            return None
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = find_shortest_path(graph, node, end, path)
                if newpath:
                    if not shortest or calc_len(smezh,newpath) < calc_len(smezh,shortest):
                        shortest = newpath
        return shortest

def dist_(d1,d2):
  return math.sqrt((d1[0]-d2[0])*(d1[0]-d2[0])+(d1[1]-d2[1])*(d1[1]-d2[1]))
def norm_(d1):
  dd=math.sqrt(d1[0]*d1[0]+d1[1]*d1[1])
  if(dd==0.0):
      return (0.0,0.0)
  #print(d1,dd)
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

def PaintGraphTM(gr_name,probs,path_to,path_a,nv,directed=1,calc_random_path=1,v_nm=[]):
    global ccc
    v_nams=[]
    if v_nm==[]:
        for i in range(nv):
            v_nams.append(i+1)
    else:        
        v_nams=copy.copy(v_nm)
    sc=0.7
    scs=1
#    sc=2./3
#    scs=(sc)/0.7
    fi=1
    ccc = canvas.canvas()
    if(calc_random_path):
     ccc.fill(path.circle(probs[0][0],probs[0][1], 0.2))
     ccc.stroke(path.circle(probs[0][0],probs[0][1], 0.15))
     ccc.stroke(path.circle(probs[fi][0],probs[fi][1], 0.2))
    xx=[x[0] for x in probs]
    yy=[y[1] for y in probs]
    #print('xx:',xx)
    #print('yy:',yy)
    minx=min(xx)
    maxx=max(xx)
    miny=min(yy)
    maxy=max(yy)
    for jj in range(nv):
     pp=probs[jj]
     #if(directed):
     # ccc.stroke(path.circle(pp[0],pp[1], 0.1))
     #else:
     ccc.fill(path.circle(pp[0]*sc,pp[1]*sc, 0.1))
     
     for ph in path_to[jj]:
      dxx=pp[0]+(probs[ph][0]-pp[0])*2/3.
      dyy=pp[1]+(probs[ph][1]-pp[1])*2/3.
      if(directed):
       ccc.stroke(path.line(pp[0]*sc, pp[1]*sc, dxx*sc, dyy*sc),[deco.earrow([deco.filled()])])
      ccc.stroke(path.line(pp[0]*sc, pp[1]*sc, probs[ph][0]*sc,probs[ph][1]*sc))
     text_d0=0.0
     text_d1=0.0
     for phi in path_a[jj]:
      if(not phi==jj):
       ph=probs[phi]
       #print(pp,ph)
       d1=diff_(pp,ph)
       dd=math.sqrt(d1[0]*d1[0]+d1[1]*d1[1])
       text_d0+=d1[0]/dd
       text_d1+=d1[1]/dd
     if text_d0==0 and text_d1==0:
        for i in range(nv):
            if i==jj: 
                continue
            ph=probs[i]
            d1=diff_(pp,ph)
            dd=math.sqrt(d1[0]*d1[0]+d1[1]*d1[1])
            text_d0+=d1[0]/dd
            text_d1+=d1[1]/dd           
     ntd=norm_((text_d0,text_d1))
     ccc.text(pp[0]*sc-0.5*ntd[0]*scs,pp[1]*sc-0.5*ntd[1]*scs, str(v_nams[jj]), [text.size(2),text.mathmode, text.vshift.mathaxis,text.halign.boxcenter])
    #ccc.stroke(path.rect(minx-1, miny-1, maxx-minx+2,maxy-miny+2))
    ccc.stroke(path.rect(-3*sc, -3*sc, 6*sc,6*sc))
    #ccc.stroke(path.circle(0,0,3))
    ccc.writeEPSfile('./tex/'+gr_name)
#    ccc.writePDFfile(gr_name)

def MatrMult(a,b):
    return [[sum([a[j][k]*b[k][i] for k in range(0,len(b))]) for i in range(0,len(a[0]))]for j in range(0,len(a))]
    
def PowerSmezh(m,n):
    mm=[[int(i==j) for i in range(0,len(m))]for j in range(0,len(m))]
    for i in range (0,n):
        mm=MatrMult(mm,m)
    return mm
def PlaceGraphVerts(nv):
#generate random placed verticles for graph picture
    sc=4
    s1=2
    do_work = 1
    itry = 0
    probs = []
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
        if tc>100:
          do_work=1
          break
      if do_work:
       break
      probs.append(d1)
     if do_work:
      continue
    return probs

def PaintGraphSet(gr):
    nv=len(gr[0])
    varc=open('var_count','r')
    v_cou=int(varc.readline())
    varc.close()
    vc = open('var_count', 'w')
    vc.write(str(v_cou))
    vc.close()
    (path_to,path_a)=gr_to_graph_tm(gr)
    probs=PlaceGraphVerts(nv)
    fnam="graph"+str(v_cou)
    print(probs)
    print((path_to,path_a))
    PaintGraphTM(fnam,probs,path_to,path_a,nv,directed=1,calc_random_path=0,v_nams=list(gr[0]))
    return fnam
    
def MakeGraphTM(nv=5,directed=1,calc_random_path=1,weighted=0,filter_zero=0,random_weights=0,v_nams=[],paint_fl=1):
    random.seed()
    global id_count
    global all_path
    id_count = 1
    probs = []
    probs_all = []
    all_path = []
    varc=open('var_count','r')
    v_cou=int(varc.readline())
    varc.close()
    ii=1
    v_cou+=1
    #print('ii=',ii)
    id_count = 1
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
     while pathc<nv*4:
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
     if filter_zero:
      for p in path_a:
       if not len(p):
        do_work=1
     if do_work:
      continue     
    
    probs_all=[]
    if paint_fl:
        PaintGraphTM("graph"+str(v_cou),probs,path_to,path_a,nv,directed,calc_random_path,v_nams)
    grfile="graph"+str(v_cou)+".eps"
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
      if weighted: 
       sml=int(10*dist_(probs[i],probs[p]))
       if random_weights:
        sml=random.randint(1,5)
      else:
       sml=1      
      smezh[i][p]=sml
      if not directed:
       smezh[p][i]=sml         
    return (grfile,str(f_prob),incin,smezh,probs,path_to,path_a)
#(a,b,incin,smezh)=MakeGraphTM(5,1)
#print('incinden:')    
#for i in incin:
# print (i)
#print('smzeh:')    
#for i in smezh:
# print (i)
 
def MakeGraphs():
 v_cou=5
 tex_file=open('graphs'+str(v_cou)+'.tex','w')
 tex_cmp=open('cmp_tex.bat','w')
 res_file=open('result.txt','w')
 tex_cmp.write('latex graphs'+str(v_cou)+'.tex\n')
 tex_cmp.write('dvips  graphs'+str(v_cou)+'.dvi\n')
 tex_cmp.write('ps2pdf graphs'+str(v_cou)+'.ps\n')
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
 tex_file.write("\\captionsetup[subfigure]{labelformat=empty}\n")
 for i in range(0,30):
    tex_file.write("\\begin{figure}[!htb]\n")
    tex_file.write("\\centering\n")
    cname='circl'+str(i)
    cn=[]
    uf=[]
    for j in range(0,4):
     cn.append(MakeGraphTM(8,1)[0])
     uf.append("Вариант "+str(i*4+j))
    #tex_file.write("\\caption{Задача "+str(i)+". Какому рисунку соответствует выражение: \\\\")
    tex_file.write("\\begin{subfigure}[t]{0.4\\textwidth}\n")
    tex_file.write("\\includegraphics{"+cn[0]+"}\n")
    tex_file.write("\\caption{"+uf[0]+"}\n")
    tex_file.write("\\end{subfigure}\n")
    tex_file.write("\\begin{subfigure}[t]{0.4\\textwidth}\n")
    tex_file.write("\\includegraphics{"+cn[1]+"}\n")
    tex_file.write("\\caption{"+uf[1]+"}\n")
    tex_file.write("\\end{subfigure}\n")
    tex_file.write("\n\\bigskip\n\\vskip 2cm\n\n")
    tex_file.write("\\begin{subfigure}[t]{0.4\\textwidth}\n")
    tex_file.write("\\includegraphics{"+cn[2]+"}\n")
    tex_file.write("\\caption{"+uf[2]+"}\n")
    tex_file.write("\\end{subfigure}\n")
    tex_file.write("\\begin{subfigure}[t]{0.4\\textwidth}\n")
    tex_file.write("\\includegraphics{"+cn[3]+"}\n")
    tex_file.write("\\caption{"+uf[3]+"}\n")
    tex_file.write("\\end{subfigure}\n")   
    tex_file.write("\\end{figure}\n")
 tex_file.write("\\end{document}\n")
def MakeGraphsMatr():
 v_cou=11
 tex_file=open('graphs'+str(v_cou)+'.tex','w')
 tex_cmp=open('cmp_tex.bat','w')
 res_file=open('result.txt','w')
 tex_cmp.write('latex graphs'+str(v_cou)+'.tex\n')
 tex_cmp.write('dvips  graphs'+str(v_cou)+'.dvi\n')
 tex_cmp.write('ps2pdf graphs'+str(v_cou)+'.ps\n')
 tex_file.write("\\documentclass[12pt]{article}\n")
 tex_file.write("\\usepackage{graphics}\n")
 tex_file.write("\\usepackage{amsmath}\n")
 tex_file.write("\\usepackage[cp1251]{inputenc}\n")
 tex_file.write("\\usepackage[russian]{babel}\n")
 tex_file.write("\\usepackage[left=4cm,right=2cm,top=0cm,bottom=2cm,bindingoffset=0cm]{geometry}\n")
 tex_file.write("\\usepackage{caption}\n")
 tex_file.write("\\usepackage{subcaption}\n")
 tex_file.write("\\begin{document}\n")
 tex_file.write("\\pagenumbering{gobble}\n")
 tex_file.write("\\captionsetup{labelformat=empty}\n")
 tex_file.write("\\captionsetup[subfigure]{labelformat=empty}\n")
 for i in range(0,8):
    if (i and not i%4):
     tex_file.write('\\newpage\n')      
    cname='circl'+str(i)
    cn=[]
    uf=[]
    mf=[]
    for j in range(0,1):
#     tmp=MakeGraphTM(8,1,0,1,1,1)
     tmp = MakeGraphTM(nv = 8, directed = 0, calc_random_path = 0, weighted = 1, filter_zero = 1, random_weights = 1)
     cn.append(tmp[0])
     uf.append("Вариант: "+str(i+1+j))
     mf.append(MakeMatrix(tmp[3]))
    #tex_file.write("\\caption{Задача "+str(i)+". Какому рисунку соответствует выражение: \\\\")
    tex_file.write('\\centering{'+uf[0]+'.}\n\n')      
    tex_file.write('\\begin{minipage}[c]{0.45\\textwidth}\n')
    tex_file.write("\\includegraphics{"+cn[0]+"}\n")
    tex_file.write('\\end{minipage}\n')      
    tex_file.write('\\begin{minipage}[c]{0.45\\textwidth}\n')
    tex_file.write(mf[0])
    tex_file.write('\\end{minipage}\n')      
    tex_file.write("\n\\bigskip\n\\bigskip\n")
 tex_file.write("\\end{document}\n")

def MakeGraphsMatrPath():
 v_cou=12
 tex_file=open('graphs'+str(v_cou)+'.tex','w')
 tex_cmp=open('cmp_tex.bat','w')
 res_file=open('result.txt','w')
 tex_cmp.write('latex graphs'+str(v_cou)+'.tex\n')
 tex_cmp.write('dvips  graphs'+str(v_cou)+'.dvi\n')
 tex_cmp.write('ps2pdf graphs'+str(v_cou)+'.ps\n')
 tex_file.write("\\documentclass[12pt]{article}\n")
 tex_file.write("\\usepackage{graphics}\n")
 tex_file.write("\\usepackage{amsmath}\n")
 tex_file.write("\\usepackage[cp1251]{inputenc}\n")
 tex_file.write("\\usepackage[russian]{babel}\n")
 tex_file.write("\\usepackage[left=4cm,right=2cm,top=0cm,bottom=2cm,bindingoffset=0cm]{geometry}\n")
 tex_file.write("\\usepackage{caption}\n")
 tex_file.write("\\usepackage{subcaption}\n")
 tex_file.write("\\begin{document}\n")
 tex_file.write("\\pagenumbering{gobble}\n")
 tex_file.write("\\captionsetup{labelformat=empty}\n")
 tex_file.write("\\captionsetup[subfigure]{labelformat=empty}\n")
 for i in range(0,64):
    if (i and not i%4):
     tex_file.write('\\newpage\n')
    cname='circl'+str(i)
    cn=[]
    uf=[]
    mf=[]
    for j in range(0,1):
#     tmp=MakeGraphTM(8,1,0,1,1,1)
     nv=8
     tmp = MakeGraphTM(nv, directed = 1, calc_random_path = 0, weighted = 1, filter_zero = 1, random_weights = 1)
     grph=[list(set(x)) for x in tmp[6]]
     maxpts=[len(find_shortest_path_smezh(tmp[3],grph,0,ii)) for ii in range(0,len(tmp[4]))]
     end_p=maxpts.index(max(maxpts))
     sh_pt=find_shortest_path_smezh(tmp[3],grph,0,end_p)
     sh_pto=[[] for i in range(0,len(tmp[4]))]
     sh_pta=[[] for i in range(0,len(tmp[4]))]
     for ii in range(1,len(tmp[4])):
          if ii in sh_pt:
            sh_pto[ii].append(sh_pt[sh_pt.index(ii)-1])
            sh_pta[ii].append(sh_pt[sh_pt.index(ii)-1])
            if(not ii==end_p):
             sh_pta[ii].append(sh_pt[sh_pt.index(ii)+1])
     PaintGraphTM('test_path_'+tmp[0],tmp[4],sh_pto,sh_pta,len(tmp[4]),directed=1,calc_random_path=0)
     cn.append(tmp[0])
     grph=[list(set(x)) for x in tmp[6]]
     uf.append("Вариант: "+str(i+1+j)+" Путь из "+str(end_p+1)+" в 1.")
     mf.append(MakeMatrix(tmp[3]))
    #tex_file.write("\\caption{Задача "+str(i)+". Какому рисунку соответствует выражение: \\\\")
    tex_file.write('\\centering{'+uf[0]+'.}\n\n')
    tex_file.write('\\begin{minipage}[c]{0.45\\textwidth}\n')
    tex_file.write("\\includegraphics{"+cn[0]+"}\n")
    tex_file.write('\\end{minipage}\n')
    tex_file.write('\\centering{'+uf[0]+'.}\n\n')
    tex_file.write('\\begin{minipage}[c]{0.45\\textwidth}\n')
    tex_file.write("\\includegraphics{"+'test_path_'+cn[0]+"}\n")
    tex_file.write('\\end{minipage}\n')
    tex_file.write('\\begin{minipage}[c]{0.45\\textwidth}\n')
    tex_file.write(mf[0])
    tex_file.write('\\end{minipage}\n')
    tex_file.write("\n\\bigskip\n\\bigskip\n")

 tex_file.write("\\end{document}\n")

def LocStructCluben(N):
    #N=8
    tmp = MakeGraphTM(nv = N, directed = 0, calc_random_path = 0, weighted = 0, filter_zero = 1, random_weights = 1)
    #print(tmp)
    nm=np.matrix(tmp[3])
    G=nx.from_numpy_matrix(nm,create_using=nx.MultiDiGraph())
    #print('FW:')
    fw=nx.floyd_warshall(G)
    #for i in fw:
    # print(i,fw[i])
    #print('G:')
    #for i in G:
    # print(i,G[i])
    #print(list(fw[0].keys()))
    exc=[max([fw[i][j] for j in range(0,N)]) for i in range(0,N)]
    #exc=[fw[i] for i in fw]
    m=min(exc)
    cluben=[i+1 for i in range(0,N) if exc[i]==m]
    print('exc:',exc)
    print('Cluben:',cluben)
    return (tmp[0],cluben)

def FindPathsForFixedLenght(N,n,i,j):
    tmp = MakeGraphTM(nv = N, directed = 0, calc_random_path = 0, weighted = 0, filter_zero = 1, random_weights = 1)
    nm=np.matrix(tmp[3])
    mm=np.matrix(tmp[3])
    print('Smezhn:')
    print(mm)    
    for k in range(0,n-1):
        mm=nm*mm
    print(mm)    
    return (tmp[0],mm[i,j])    
    #print(nm)


#a=MakeGraphTM(nv=4,directed=1,calc_random_path=0,weighted=0,filter_zero=0,random_weights=0,v_nams=[],paint_fl=1)
#print(a)
#b=graph_repr(a[5],1)
#for i in b[0]:
#    print(i)
#print(b[2])
#print(b[3])
#print(b[4])
#print(gr_tostr(b[4]))
#print(PaintGraphSet(b[4]))

#b=graph_repr(a[5],1,[2,3,4,5,1])
#for i in b[0]:
#    print(i)
#print(b[2])
#print(b[3])
#b=graph_repr(a[5],1,[3,4,5,1,2])
#for i in b[0]:
#    print(i)
#print(b[2])
#print(b[3])
#b=graph_repr(a[5],1,['A','B','C','D','E','F'])
#for i in b[0]:
#    print(i)
#print(b[2])
#print(b[3])
#vnms=['A','B','C','D','E','F']
#random.shuffle(vnms)
#b=graph_repr(a[5],1,vnms)
#for i in b[0]:
#    print(i)
#print(b[2])
#print(b[3])
#print(FindPathsForFixedLenght(4,3,1,2))
#LocStructCluben(8)
#MakeGraphsMatr()  
#MakeGraphs()  
#mm=np.matrix(tmp[3])
#for k in range(0,4):
#    print(k)
#    print(mm)
#    mm=mm*nm    
    
#print (tmp[6])
#grph=[list(set(x)) for x in tmp[6]]
#print(grph)
#sh_pt=find_shortest_path(grph,0,1)
#print(sh_pt)
#sh_pto=[[] for i in range(0,len(tmp[4]))]
#sh_pta=[[] for i in range(0,len(tmp[4]))]
#for i in range(1,len(tmp[4])):
#     if i in sh_pt:
#       sh_pto[i].append(sh_pt[sh_pt.index(i)-1])
#       sh_pta[i].append(sh_pt[sh_pt.index(i)-1])
#       if(not i==1):
#        sh_pta[i].append(sh_pt[sh_pt.index(i)+1])
#PaintGraphTM('test_gr',tmp[4],sh_pto,sh_pta,len(tmp[4]),directed=1,calc_random_path=1)
#    return (grfile,str(f_prob),incin,smezh,probs,path_to,path_a)
#MakeGraphsMatrPath()
#gr1=NewGraph(4,5,sym=True)
#print(gr1)
#print(gr1.kruskal())
#print(MakeMatrix(gr1.smezh))

#gr2=NewGraph(4,3)
#G=nx.from_numpy_matrix(gr2.smezh,create_using=nx.MultiDiGraph())
#for i in G:
# print(i,G[i])
 
#print(gr2.dijkstra1(1))
#print(grAnd(gr1.smezh,gr2.smezh))
#print(grMult(gr1.smezh,gr2.smezh))
#print(grMult(gr2.smezh,gr1.smezh))
#gr.RemoveEdge()
#gr.RemoveNode()
#gr.MergeNodeIJDel(1, 2)
