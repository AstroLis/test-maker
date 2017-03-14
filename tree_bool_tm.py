import random
from shutil import copyfile
from pyx import *

# for constructing boolean function tasks simple binary tree
# in this implementation, a node is inserted between an existing node and the root
BoolOperands=['\\wedge','\\vee','\\rightarrow','\\leftrightarrow','|','\\downarrow','\\oplus']
BoolOrder=   [0       ,   1    ,       2      ,         3        , 0 ,     0       ,    3]
varNames=    ['x_1','x_2','x_3']
class BinaryTree():
    id_count=1
    probs=[]
    probs_all=[]
    ccc=canvas.canvas()
    bx = 0.8
    by = 0.4
    def __init__(self):
      self.left = None
      self.right = None
      self.rootid = BinaryTree.id_count
      BinaryTree.id_count+=1
      self.dimx=0
      self.dimy=0
      self.type=0
      self.prob=random.randint(0,6)
      self.neg=random.randint(0,5)

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
          self.left=BinaryTree()
          self.right=BinaryTree()
       else:
        self.left.randTree()
        self.right.randTree()
def MakeFormulaFromTree(tree,oper):
    if tree != None:
        if(not tree.type):
          return varNames[tree.neg%3]
        else:
           lleft=MakeFormulaFromTree(tree.getLeftChild(),tree.prob)
           rright=MakeFormulaFromTree(tree.getRightChild(),tree.prob)
           res=lleft+' '+BoolOperands[tree.prob]+' '+rright
           if BoolOrder[oper]<BoolOrder[tree.prob]:
               return '('+res+')'
           else:
               return res

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
 myTree1 = BinaryTree()
 while (BinaryTree.id_count!=max_p):
   BinaryTree.id_count = 1
   myTree1 = BinaryTree()
   for i in range(10):
     myTree1.randTree()
 form=MakeFormulaFromTree(myTree1,0)
 print(form)
 return form

def MakeForrestFormulas():
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
 for i in range(0,100):
    tex_file.write("$$\n")
    tex_file.write(MakeFormulaTM(10)+'\n')
    tex_file.write("$$\n")

 tex_file.write("\\end{document}\n")
 
#MakeForrest()
#print(MakeTreeTM())

#MakeFormulaTM(10)
MakeForrestFormulas()