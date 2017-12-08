import random
from shutil import copyfile
from pyx import *

# simple binary tree
# in this implementation, a node is inserted between an existing node and the root
class BinaryTree():
    id_count=1
    probs=[]
    probs_all=[]
    ccc=canvas.canvas()
    bx = 0.8
    by = 0.4
    def __init__(self,prob):
      self.left = None
      self.right = None
      self.rootid = BinaryTree.id_count
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
          self.right=BinaryTree(random.random())
       else:
        self.left.randTree()
        self.right.randTree()
    def calcDim(self):
       if(not self.type):
         BinaryTree.probs.append((self.rootid,self.prob))
         BinaryTree.probs_all.append((self.rootid,self.prob))
         self.dimx=1
         self.dimy=1
         return(1,1,self.prob)
       else:
         (xl,yl,pl)=self.left.calcDim()
         (xr,yr,pr)=self.right.calcDim()
         if(self.type==1):
          self.dimx=xl+xr
          self.dimy=yl if yl>yr else yr
          self.prob=pr*pl
         else:
          self.dimx=xl if xl>xr else xr
          self.dimy=yl+yr
          self.prob = pr+pl-pr * pl
         BinaryTree.probs_all.append((self.rootid,self.prob))
         return (self.dimx,self.dimy,self.prob)

def printTree(tree):
        if tree != None:
            printTree(tree.getLeftChild())
            print(tree.getNodeValue())
            printTree(tree.getRightChild())


def paintTree(tree,x1,y1,x2,y2):
    xx1 = (x1 + x2) / 2.
    yy1 = (y1 + y2) / 2.
    xl1=(x2 - x1)
    yl1=(y2 - y1)
    m=0.1
    if tree != None:
        if(not tree.type):
          BinaryTree.ccc.stroke(path.rect(xx1-BinaryTree.bx/2.,yy1-BinaryTree.by/2.,BinaryTree.bx,BinaryTree.by))
          BinaryTree.ccc.text(xx1, yy1-BinaryTree.by/(2.5), str(tree.rootid), [text.size(1),text.halign.boxcenter])
          BinaryTree.ccc.stroke(path.line(xx1-BinaryTree.bx/2., yy1, x1, yy1))
          BinaryTree.ccc.stroke(path.line(xx1+BinaryTree.bx/2., yy1, x2, yy1))
          return
        else:
          if(tree.type==1):
           #ccc.stroke(path.line(x1,yy1,x1-xl1*m,yy1))
           #ccc.stroke(path.line(x2,yy1,x2+xl1*m,yy1))
           l1=tree.left.dimx
           l2=tree.right.dimx
           mx=x1+(x2-x1)*l1/(l2+l1*1.0)
           paintTree(tree.getLeftChild(),x1,y1,mx,y2)
           paintTree(tree.getRightChild(),mx,y1,x2,y2)
          else:
           l1=tree.left.dimy
           l2=tree.right.dimy
           my=y1+(y2-y1)*l1/(l2+l1*1.0)
           my1=y1+(y2-y1)*l1/(l2+l1*1.0)/2
           my2=y1+(y2-y1)*l1/(l2+l1*1.0)+(y2-y1)*l2/(l2+l1*1.0)/2
           mx1=x1+tree.dimx*m
           mx2=x2-tree.dimx*m

           BinaryTree.ccc.stroke(path.line(x1,(y1+y2)/2,mx1,(y1+y2)/2))
           BinaryTree.ccc.stroke(path.line(x2,(y1+y2)/2,mx2,(y1+y2)/2))

           BinaryTree.ccc.stroke(path.line(mx1,my1,mx1,my2))
           BinaryTree.ccc.stroke(path.line(mx2,my1,mx2,my2))
           paintTree(tree.getLeftChild(),mx1,y1,mx2,my)
           paintTree(tree.getRightChild(),mx1,my,mx2,y2)


def MakeSchemeTM(number_of_element=4):
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
   myTree1 = BinaryTree(0.5)
   for i in range(5):
     myTree1.randTree()
      #printTree(myTree1)
 BinaryTree.ccc.stroke(path.line(-xx, 0, -xx - BinaryTree.bx, 0))
 BinaryTree.ccc.stroke(path.line(xx, 0, xx + BinaryTree.bx, 0))
 BinaryTree.ccc.stroke(path.circle(xx+BinaryTree.bx+0.1, 0, 0.1))
 BinaryTree.ccc.stroke(path.circle(-xx-BinaryTree.bx-0.1, 0, 0.1))
 BinaryTree.probs=[]
 BinaryTree.probs_all=[]
 myTree1.calcDim()
 paintTree(myTree1, -xx, -yy, xx, yy)
 BinaryTree.ccc.writeEPSfile("schem"+str(v_cou))
 print(sorted(BinaryTree.probs_all))
 print(BinaryTree.probs)
 vc=open('var_count','w')
 vc.write(str(v_cou))
 vc.close()
 return ("schem"+str(v_cou)+".eps",sorted(BinaryTree.probs_all)[0][1],BinaryTree.probs)
#random.seed(0)
#print(MakeSchemeTM())
