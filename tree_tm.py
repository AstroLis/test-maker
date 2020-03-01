import random
import numpy as np
import networkx as nx
from shutil import copyfile
from pyx import *

# simple binary tree
# in this implementation, a node is inserted between an existing node and the root
class BinaryTree():
    id_count=1
    probs={}
    probs_all=[]
    ccc=canvas.canvas()
    bx = 0.8
    by = 0.4
    def __init__(self,prob):
      self.left = None
      self.right = None
      self.rootid = BinaryTree.id_count
      BinaryTree.probs[self.rootid]=[]
      BinaryTree.id_count+=1
      self.dimx=0
      self.dimy=0
      self.type=0
      self.prob=int(prob*10)/10.

    def getLeftChild(self):
        return self.left
    def getRightChild(self):
        return self.right
    def setNodeValue(self,value):
        self.rootid = value
    def getNodeValue(self):
        return self.rootid

    def insertRight(self,newNode):
        if self.right == None:
            self.right = BinaryTree(newNode)
        else:
            tree = BinaryTree(newNode)
            tree.right = self.right
            self.right = tree

    def insertLeft(self,newNode):
        if self.left == None:
            self.left = BinaryTree(newNode)
        else:
            tree = BinaryTree(newNode)
            self.left = tree
            tree.left = self.left
    def randTree(self):
       if(not self.type):
        if(random.randint(0,1)):
          tt=random.randint(1,2)
          self.type=tt          
          self.left=BinaryTree(random.random())
          BinaryTree.probs[self.rootid].append(self.left.rootid)
          self.right=BinaryTree(random.random())
          BinaryTree.probs[self.rootid].append(self.right.rootid)
       else:
        self.left.randTree()
        self.right.randTree()
def paintTree(tree,lvl,x1,y1,bText=False):
    #print("paintTree")
    #print((lvl,x1,y1))
    #print(("tree type",tree.type))
    
    m=0.1
    if tree != None:
        BinaryTree.ccc.fill(path.circle(x1,y1,m))
        if(not tree.type):
          return
        else:
           y2=y1-0.3
           x0=x1-lvl
           x2=x1+lvl
           lvl=lvl*0.5
           BinaryTree.ccc.stroke(path.line(x1,y1,x0,y2))
           BinaryTree.ccc.stroke(path.line(x1,y1,x2,y2))
           paintTree(tree.getLeftChild(),lvl,x0,y2,bText)
           paintTree(tree.getRightChild(),lvl,x2,y2,bText)
def MakeTreeTM(number_of_element=10,bText=False):
 number_of_chemes=10
 BinaryTree.id_count=1
 varc=open('var_count','r')
 v_cou=int(varc.readline())
 varc.close()
 BinaryTree.ccc=canvas.canvas()
 xx=4
 yy=2
 n_=number_of_element
 v_cou+=1
 max_p=n_*2
 while (BinaryTree.id_count!=max_p):
   BinaryTree.id_count = 1
   BinaryTree.probs = {}
   myTree1 = BinaryTree(0.5)
   for i in range(10):
     myTree1.randTree()
 print(BinaryTree.id_count)    
 lvl=4
 paintTree(myTree1, lvl, 0, 5,bText)
# print(BinaryTree.probs)
 BinaryTree.ccc.writeEPSfile("./tex/tree"+str(v_cou))
# BinaryTree.ccc.writePDFfile("tree"+str(v_cou))
 vc=open('var_count','w')
 vc.write(str(v_cou))
 vc.close()
 return ("tree"+str(v_cou)+".eps",BinaryTree.probs)
def RadDiam(N=10,bText=False):
 (fn,gr)=MakeTreeTM(N,bText)
 print(gr)
 grl=len(gr)
 mm=np.zeros((grl,grl))
 for i in gr:
    for j in gr[i]:
        mm[i-1][j-1]=1
        mm[j-1][i-1]=1
 #print(mm)       
 G=nx.from_numpy_matrix(mm,create_using=nx.MultiDiGraph())
 #for i in G:
 #  print(i,G[i])
 fw=nx.floyd_warshall(G)
 exc=[max([fw[i][j] for j in range(0,grl)]) for i in range(0,grl)]
 mn=min(exc)
 mx=max(exc)
 cluben=[i+1 for i in range(0,grl) if exc[i]==mn]
 perif=[i+1 for i in range(0,grl) if exc[i]==mx]
 print('exc:',exc)
 print(mn,mx)
 print(cluben,perif)
 return (fn,(int(mn),int(mx),len(cluben),len(perif)))
def MakeForrest(): 
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
 tex_file.write("\\usepackage[left=4cm,right=2cm,top=0cm,bottom=2cm,bindingoffset=0cm]{geometry}\n")
 tex_file.write("\\usepackage{caption}\n")
 tex_file.write("\\usepackage{subcaption}\n")
 tex_file.write("\\begin{document}\n")
 tex_file.write("\\pagenumbering{gobble}\n")
 tex_file.write("\\captionsetup{labelformat=empty}\n")
 for i in range(0,10):
    tex_file.write("\\begin{figure}[]\n")
    cn=MakeTreeTM(10)
    rr=random.randint(0,3)
    tex_file.write("\\caption{Вариант "+str(i)+"}\n")
    tex_file.write("\\includegraphics{"+cn+"}\n")
    tex_file.write("\\end{figure}\n")
    if not i%6:
     tex_file.write("\\clearpage\n")
    
 tex_file.write("\\end{document}\n")
 
#RadDiam(11) 
#MakeForrest() 
#tr=MakeTreeTM(10)


