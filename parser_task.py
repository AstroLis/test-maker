import json,random,parser,math
def ParseTask(TName):
   rt=[]
   fl=1
   while fl: 
    rt=[]
    z=open(TName,"r")
    zz=z.read()
    data=json.loads(zz)
    NL='\n\n'
    SL='\\'
    A1=eval(parser.expr( data['param']['A1'] ).compile())
    A2=eval(parser.expr( data['param']['A2'] ).compile())
    A3=eval(parser.expr( data['param']['A3'] ).compile())
    A4=eval(parser.expr( data['param']['A4'] ).compile())
    A5=eval(parser.expr( data['param']['A5'] ).compile())
    A6=eval(parser.expr( data['param']['A6'] ).compile())
    A7=eval(parser.expr( data['param']['A7'] ).compile())
    rt.append(str(eval(parser.expr( data['zadacha'] ).compile()))+'\n')
    if(len(data['vopros'])==4):
     vv=['v1','v2','v3','v4']
     random.shuffle(vv)
     rt.append(str(eval(parser.expr(data['vopros'][vv[0]]).compile()))+'\n\n')
     otvs=[]
     for oo in data['otvet'].keys():
      otvs.append(str(eval(parser.expr( data['otvet'][oo] ).compile())))
     if len(otvs) > len(set(otvs)):
      continue
     fl=0 
     rt.append('a) '+str(eval(parser.expr( data['otvet']['o1'] ).compile()))+'\n')
     rt.append('b) '+str(eval(parser.expr( data['otvet']['o2'] ).compile()))+'\n')
     rt.append('c) '+str(eval(parser.expr( data['otvet']['o3'] ).compile()))+'\n')
     rt.append('d) '+str(eval(parser.expr( data['otvet']['o4'] ).compile()))+'\n')
    elif (len(data['vopros'])==1):
     rt.append(str(eval(parser.expr(data['vopros']['v1']).compile()))+'\n\n')
     rt.append('1) '+str(eval(parser.expr( data['otvet']['o1'] ).compile()))+'\n')
     for i in range(2,5):
         A1=eval(parser.expr( data['param']['A1'] ).compile())
         A2=eval(parser.expr( data['param']['A2'] ).compile())
         A3=eval(parser.expr( data['param']['A3'] ).compile())
         A4=eval(parser.expr( data['param']['A4'] ).compile())
         A5=eval(parser.expr( data['param']['A5'] ).compile())
         A6=eval(parser.expr( data['param']['A6'] ).compile())
         A7=eval(parser.expr( data['param']['A7'] ).compile())
         rt.append(str(i)+') '+str(eval(parser.expr( data['otvet']['o1'] ).compile()))+'\n')
     fl=0
   return rt
xx=[random.randint(1,11) for c in range(0,5)]
print(xx)
ntests=30
f=open('test1.tex','w')
f.write("\\documentclass[12pt]{article}\n")
f.write("\\usepackage{graphics}\n")
f.write("\\usepackage{amsmath}\n")
f.write("\\usepackage[left=2cm,right=2cm,top=0cm,bottom=2cm,bindingoffset=0cm]{geometry}\n")
f.write("\\usepackage[russian]{babel}\n")
f.write("\\begin{document}\n")
for iii in range(1,ntests): 
    f.write("\\begin{enumerate}\n")
    test_mask=open("test.mask")
    for tname in test_mask.read().splitlines():     
     f.write("\\item ");
     task=ParseTask(tname)
     f.writelines(task)
     f.write("\n\n")
    f.write("\\end{enumerate}\n")
    f.write("\\newpage\n")
    
f.write("\\end{document}\n")

