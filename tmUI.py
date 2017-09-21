from tkinter import *
from tkinter import ttk
import os
import json,random,parser,math,datetime,copy
import numpy as np
sys.path.append('./graph_tm.py')
sys.path.append('./plot_fraspr_tm.py')
sys.path.append('./scheme_tm.py')
sys.path.append('./algebra_tm.py')
sys.path.append('./tree_bool_tm.py')

import graph_tm
import plot_fraspr_tm
import scheme_tm
import algebra_tm
import tree_bool_tm

def Cnm(n,m):
 if n<m:
   return 0
 return math.factorial(n)/(math.factorial(m)*math.factorial(n-m))

def Shuf(x):
 xx=list(x)
 random.shuffle(xx)
 return xx

def RB(s):
 return s.replace('[','\{').replace(']','\}') 
 
def MakeTable(xyT,xHead,yHead,data,ff=2):
 tb=''
 tb+=('\\begin{tabular}{|c|')
 for x in xHead:
  tb+=('c|')
 tb+=('} \\hline ')
 tb+=(str(xyT))
 for x in xHead:
  tb+=('&'+str(x))
 tb+=('\\\\ \\hline')
 id=0
 for y in yHead:
  tb+=(str(y))
  for x in xHead:
   tb+=('&'+'{:4.2f}'.format(data[id]))
   id=id+1
  tb+=('\\\\ \\hline')
 tb+=('\\end{tabular}')
 return tb

def MakeMatrix(data,ff=2):
 tb=''
 tb+=('$$ \\small \\begin{pmatrix}')
 for y in data:
  i=0
  for x in y:
   if i:
    tb+='&'
   else:
    i=1  
   if(x>=0):    
    tb+=('{:g}'.format(x))
   else:
    tb+=('\\text{-}'+'{:g}'.format(-x))   
  tb+=('\\\\')
 tb+=(' \\end{pmatrix}$$')
 return tb
 

def MakeNormalDistr(a,sigm):
 return "$$ f_X(x)=\\frac{1}{"+(str(sigm) if sigm!=1 else "")+" \\sqrt{2 \\pi}} \\cdot e^{- \\frac{"+(("(x"+("-"+str(a) if a>0 else "+"+str(-a))+")^2") if a!=0 else ("x^2"))+"}{"+str(2*sigm*sigm)+"}} $$"

def EvalParams(dParams):
    NL='\n\n'
    SL='\\'
    pars={}
    print(dParams)
    for A in sorted(list(dParams.keys())):
     print(A)
     print(dParams[A])
     exec(str(A)+'='+str(dParams[A]),globals())
     pars[A]=eval(dParams[A],globals())
     print(pars[A])
    return pars 
def EvalAnswerCore(dAnsw,**kwargs):
    return str(eval(parser.expr( dAnsw ).compile()))    
def EvalAnswer(dParams,dAnsw):
    pp=EvalParams(dParams)
    return EvalAnswerCore(dAnsw,**pp)
     
  
def ParseTaskWithParams(data,bAnswer,randAns,compl,**kwargs):
    rt=[]
    NL='\n\n'
    SL='\\'
    print(data['zadacha'])
    rt.append(str(eval(parser.expr( data['zadacha'] ).compile()))+'\n')
    otvs = []
    vv = sorted(list(data['vopros'].keys()))
    oo = sorted(list(data['otvet'].keys()))
    qnum=0
    if randAns:
     qnum=randAns-1
    print(vv)
    print(oo)
    vo = list(zip(vv, oo))
    if(len(vv)>4):
     random.shuffle(vv)
     rt.append(str(eval(parser.expr(data['vopros'][vv[qnum]]).compile())) + '\n\n')
     return (rt, '')
    elif(len(vv)==4):
     #vv=['v1','v2','v3','v4']
     if not randAns:
      random.shuffle(vo)
     rt.append(str(eval(parser.expr(data['vopros'][vo[qnum][0]]).compile()))+'\n\n')
     for o in oo:
      otvs.append(str(eval(parser.expr( data['otvet'][o] ).compile())))
    elif (len(data['vopros'])==1):
     rt.append(str(eval(parser.expr(data['vopros']['v1']).compile()))+'\n\n')
     otvs.append(str(eval(parser.expr( data['otvet']['o1'] ).compile())))
     for i in range(2,5):
          otvs.append(EvalAnswer(data['param'],data['otvet']['o1']))
     
    if len(otvs) > len(set(otvs)):
        return ([],"")
    fl=0
    ncu0=oo.index(vo[qnum][1])    #number of correct answer
    rrr=[0,1,2,3]
    random.shuffle(rrr)
    ncu=rrr.index(ncu0)
    
    if not bAnswer:
     return (rt,otvs[rrr[ncu]])
    
    if("answer_style" in data):
     print(data["answer_style"])
     #if(data["answer_style"]=='line'):
     for i in range(0,4):
       rt.append(str(i+1)+')  '+otvs[rrr[i]]+'\n\n')     
    else: 
     for i in range(0,4):
      #rt.append('\\begin{minipage}[c]{0.24\\textwidth}\n')
      rt.append('\\begin{minipage}[c]{0.02\\linewidth}\n')
      #rt.append('\\small')
      rt.append(str(i+1)+') ')
      rt.append('\\end{minipage}\n')      
      rt.append('\\begin{minipage}[c]{0.2\\linewidth}\n')
      rt.append(otvs[rrr[i]])
      rt.append('\\end{minipage}\n')      
      #if(i==1):
      #  rt.append('\n')
    #rt.append('\nCorrect answer: '+str(ncu+1))
    return (rt,str(ncu+1))
 
def ParseTask(data,bAnswer,randAns=0,compl=0):
   fl=1
   while fl:
    #z=open(TName,"r")
    #zz=z.read()
    #data=json.loads(zz)
    dPars=EvalParams(data['param'])
    print(dPars)
    aa= ParseTaskWithParams(data,bAnswer,randAns,compl,**dPars)
    if(len(aa[0])==0):
     continue
    else:
     return aa


def make_book_theme_head(TName,them_name):
 th=[]
 th.append("\\section{"+them_name+"}") 
 return th
def make_page_head(TName,Nz,ii):
 th=[]
 th.append("\\flushright{"+str(TName)+"}\n\n")
 #th.append("\\centering{ТЕСТ\n\n Теория Вероятностей и Математическая Статистика \n\n Вариант \\textnumero "+str(ii)+"}\n\n \\bigskip\n Уч.взв. \\underline{\\hspace{2cm}} ФИО \\underline{\\hspace{6cm}}\n\n")
 th.append("\\centering{ТЕСТ\n\n Дискретная Математика \n\n Вариант \\textnumero "+str(ii)+"}\n\n \\bigskip\n Уч.взв. \\underline{\\hspace{2cm}} ФИО \\underline{\\hspace{6cm}}\n\n")
 #th.append("\\centering{ТЕСТ по ТВ и МС. Вариант \\textnumero "+str(ii)+"("+str(TName)+")}\n\n \\bigskip\n Уч.взв. \\underline{\\hspace{2cm}} ФИО \\underline{\\hspace{6cm}}\n\n")
 th.append("\\begin{tabular}{|c|");
 for tt in range(0,Nz):
   th.append("c|");
 th.append("}\n")
 #th.append("\hline\n")
 #th.append("ФИО&\\multicolumn{"+str(Nz)+"}{}")
 #th.append("\\\\\n")
 th.append("\hline\n")
 th.append("Задание \\textnumero")
 for tt in range(0,Nz):
   th.append("&"+str(tt+1))
 th.append("\\\\\n")
 th.append("\hline\n")
 th.append("Ответ \\textnumero")
 for tt in range(0,Nz):
   th.append("&")
 th.append("\\\\\n")
 th.append("\hline\n")
 th.append("\\end{tabular}\n") 
 return th
 
def make_test_head(TName,Nz):
 th=[]
 th.append("\\documentclass[12pt]{article}\n")
 th.append("\\usepackage{graphicx}\n")
 th.append("\\usepackage{amsmath}\n")
 th.append("\\usepackage[left=0.5cm,right=1cm,top=0cm,bottom=2cm,bindingoffset=0cm]{geometry}\n")
 th.append("\\usepackage[russian]{babel}\n")
 th.append("\\begin{document}\n")
 #th.append("Тест по теории вероятности "+str(datetime.datetime.now()))
 return th
def make_book_head(TName):
 th=[]
 th.append("\\documentclass[8pt,a5paper]{extbook}\n")
 th.append("\\usepackage{graphicx}\n")
 th.append("\\usepackage{amsmath}\n")
 th.append("\\usepackage[left=1.5cm,right=1.5cm,top=1.6cm,bottom=1.4cm,bindingoffset=0cm]{geometry}\n")
 th.append("\\usepackage[russian]{babel}\n")
 th.append("\\setlength{\\arraycolsep}{1pt}\n")
 th.append("\\setlength{\\tabcolsep}{2pt}\n")
 th.append("\\begin{document}\n")
 th.append("Тест генератора сборника "+str(datetime.datetime.now()))
 return th

def make_book_head0(TName):
 th=[]
 th.append("\\documentclass[12pt]{article}\n")
 th.append("\\usepackage{graphicx}\n")
 th.append("\\usepackage{amsmath}\n")
 th.append("\\usepackage[left=0.5cm,right=1cm,top=0cm,bottom=2cm,bindingoffset=0cm]{geometry}\n")
 th.append("\\usepackage[russian]{babel}\n")
 th.append("\\begin{document}\n")
 th.append("Тест генератора сборника "+str(datetime.datetime.now()))
 return th
 
 
def add_task(*args):
 l2.insert('end',l1.get(l1.curselection()))
 l3.insert('end',str(len(task_data[l1.get(l1.curselection())]['vopros'])))
 return

def add_all_task(*args):
 for tkey in l1.get(0, END):
  l2.insert('end',tkey)
 return
 
def remove_task(*args):
 l2.delete(l2.curselection())
 return

def remove_all_task(*args):
 l2.delete(0, END)
 return
 
def select_theme(*args):
   #task_data={}
   l1.delete(0, END)
   for tname in theme_data[l0.get(l0.curselection())]:     
    z=open(tname,"r")
    zz=z.read()
    data=json.loads(zz)
    ttitle=str(data['title'])
    l1.insert('end',ttitle)
    task_data[ttitle]=data
   return
 
def make_book(*args):
    ntests = int(number_of_tests.get())
    bc=int(open('book_count').read().split()[0])
    test_name='book_'+str(bc)+'_'+result_file_name.get()
    with open('book_count', 'w') as f:
     f.write(str(bc+1))
 
    f = open(test_name+'.tex', 'w')
    f.writelines(make_book_head(test_name))
    fsolv = open(test_name+'_solv.txt', 'w')
    j={tkey_name:0 for tkey_name in l2.get(0, END)}
    for tkey_name in l2.get(0, END):
        f.writelines(make_book_theme_head(test_name,tkey_name))
        f.write("\\begin{enumerate}\n")
        fsolv.write("Вариант: "+str(tkey_name)+":  ")
        j[tkey_name]+=1
        i=0
        for iii in range(1, ntests):
            i=i+1
            tname=task_data[tkey_name]
            f.write("\\begin{minipage}{\\linewidth}\n\\item ")
            bAnswer=int(answer_type.get())
            #task = ParseTask(tname,bAnswer,randAns=j[tkey_name],compl=0) #disable random in 4type task
            task = ParseTask(tname,bAnswer)
            filt_sc=[x.replace('includegraphics[]','includegraphics[scale=0.5]') for x in task[0]]
            f.writelines(filt_sc)
            fsolv.write(str(i)+":"+str(task[1])+" ")
            f.write("\n\\end{minipage}\n\n")
        fsolv.write("\n")
        f.write("\\end{enumerate}\n")
        f.write("\\newpage\n")
    f.write("\\end{document}\n")
    f.close()
    fsolv.close()
    tex_cmp = open('cmp_tex.bat', 'w')
    tex_cmp.write('latex "' + test_name + '.tex"\n')
    tex_cmp.write('dvips  "' + test_name + '.dvi"\n')
    tex_cmp.write('ps2pdf "' + test_name + '.ps"\n')
    #tex_cmp.write('latex ' + str(v_cou) + '_solv.tex\n')
    #tex_cmp.write('dvips  ' + str(v_cou) + '_solv.dvi\n')
    #tex_cmp.write('ps2pdf ' + str(v_cou) + '_solv.ps\n')
    tex_cmp.close()
    os.system('cmp_tex.bat')
    return

    
def make_test(*args):
    ntests = int(number_of_tests.get())
    test_name=result_file_name.get()
    f = open(test_name+'.tex', 'w')
    f.writelines(make_test_head(test_name,l2.size()))
    fsolv = open(test_name+'_solv.txt', 'w')
    for iii in range(1, ntests):
        f.writelines(make_page_head(test_name,l2.size(),iii))
        f.write("\\begin{enumerate}\n")
        #fsolv.write("Вариант: "+str(iii)+"\n")
        fsolv.write("Вариант: "+str(iii)+":  ")
        i=0
        for tkey_name in l2.get(0, END):
            i=i+1
            tname=task_data[tkey_name]
            f.write("\\item ")
            bAnswer=int(answer_type.get())
            task = ParseTask(tname,bAnswer)
            f.writelines(task[0])
            fsolv.write(str(i)+":"+str(task[1])+" ")
            f.write("\n\n")
        fsolv.write("\n")
        f.write("\\end{enumerate}\n")
        f.write("\\newpage\n")
    f.write("\\end{document}\n")
    f.close()
    fsolv.close()
    tex_cmp = open('cmp_tex.bat', 'w')
    tex_cmp.write('latex "' + test_name + '.tex"\n')
    tex_cmp.write('dvips  "' + test_name + '.dvi"\n')
    tex_cmp.write('ps2pdf "' + test_name + '.ps"\n')
    #tex_cmp.write('latex ' + str(v_cou) + '_solv.tex\n')
    #tex_cmp.write('dvips  ' + str(v_cou) + '_solv.dvi\n')
    #tex_cmp.write('ps2pdf ' + str(v_cou) + '_solv.ps\n')
    tex_cmp.close()
    os.system('cmp_tex.bat')
    return
    
def lyview(*args):
    """connect the yview action together"""
    l2.yview(*args)
    l3.yview(*args)
    
random.seed(0)
root = Tk()
root.title("Test Maker")
col0=2
row0=1
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0+col0, row=0+row0, sticky=(N, W, E, S))
#mainframe.columnconfigure(0, weight=1)
#mainframe.rowconfigure(0, weight=1)

l0 = Listbox(mainframe, height=15,width=60)
l0.grid(column=-2+col0, row=0+row0, sticky=(N,W,E,S),rowspan = 15)
s0 = ttk.Scrollbar(mainframe, orient=VERTICAL, command=l0.yview)
s0.grid(column=-1+col0, row=0+row0, sticky=(N,S),rowspan = 15)
l0['yscrollcommand'] = s0.set
l0.bind('<<ListboxSelect>>', select_theme)
l0.activate(2)

l1 = Listbox(mainframe, height=15,width=60)
l1.grid(column=0+col0, row=0+row0, sticky=(N,W,E,S),rowspan = 15)
s1 = ttk.Scrollbar(mainframe, orient=VERTICAL, command=l1.yview)
s1.grid(column=1+col0, row=0+row0, sticky=(N,S),rowspan = 15)
l1['yscrollcommand'] = s1.set
l1.activate(2)

l2 = Listbox(mainframe, height=10,width=60)
l2.grid(column=3+col0, row=0+row0, sticky=(N,W,E,S),rowspan = 15)
l3 = Listbox(mainframe, height=10,width=5)
l3.grid(column=5+col0, row=0+row0, sticky=(N,W,E,S),rowspan = 15)
s2 = ttk.Scrollbar(mainframe, orient=VERTICAL)
s2.grid(column=4+col0, row=0+row0, sticky=(N,S),rowspan = 15)
l2['yscrollcommand'] = s2.set
l3['yscrollcommand'] = s2.set
s2.config(command=lyview)
ttk.Button(mainframe, text="++>>", command=add_task, width = 13).grid(column=2+col0, row=0+row0, sticky=(W,N),columnspan = 1)
ttk.Button(mainframe, text="--<<", command=remove_task, width = 13).grid(column=2+col0, row=1+row0, sticky=(W,N),columnspan = 1)
ttk.Button(mainframe, text="Добавить все", command=add_all_task, width = 13).grid(column=2+col0, row=2+row0, sticky=(W,N),columnspan = 1)
ttk.Button(mainframe, text="Убрать все", command=remove_all_task, width = 13).grid(column=2+col0, row=3+row0, sticky=(W,N),columnspan = 1)
ttk.Button(mainframe, text="MakeTest", command=make_test, width = 13).grid(column=2+col0, row=5+row0, sticky=(W,N),columnspan = 1)


number_of_tests=StringVar()
result_file_name=StringVar()
answer_type=StringVar()
#tester_style=StringVar()

number_of_tests.set(10)
answer_type.set(1)
#tester_style.set('test')

result_file_name.set('test1')
nt_entry = ttk.Entry(mainframe,textvariable=number_of_tests,  width=13)
ttk.Label(mainframe, text="Вариантов:").grid(column=2+col0, row=6+row0, sticky=W)
nt_entry.grid(column=2+col0, row=7+row0,  sticky=(W, E), columnspan = 1)
nt_entry = ttk.Entry(mainframe,textvariable=result_file_name,  width=13)
ttk.Label(mainframe, text="Сохранить как:").grid(column=2+col0, row=8+row0, sticky=W)
nt_entry.grid(column=2+col0, row=9+row0,  sticky=(W, E), columnspan = 1)


ttk.Label(mainframe, text="Наличие ответов:").grid(column=2+col0, row=10+row0, sticky=W)
ttk.Entry(mainframe,textvariable=answer_type,  width=6).grid(column=2+col0, row=11+row0,  sticky=(W, E), columnspan = 1)

ttk.Button(mainframe, text="MakeBook", command=make_book, width = 13).grid(column=2+col0, row=12+row0, sticky=(W,N),columnspan = 1)


ttk.Label(mainframe, text="Тема:").grid(column=-2+col0, row=-1+row0, sticky=W)
ttk.Label(mainframe, text="Задача:").grid(column=0+col0, row=-1+row0, sticky=W)

#for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
jz=open("tlist.json","r")
jzz=jz.read()
themdata=json.loads(jzz)
task_data={}
theme_data={}
for theme in sorted(list(themdata.keys())):
    ttitle=str(theme)
    l0.insert('end',ttitle)
    theme_data[ttitle]=themdata[theme]
root.mainloop()