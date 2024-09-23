from tkinter import *
from tkinter import ttk
import os
import json,random,parser,math,datetime,copy
import codecs
import moodlexport
import sympy

import numpy as np
sys.path.append('./tree_tm.py')
sys.path.append('./graph_tm.py')
sys.path.append('./plot_fraspr_tm.py')
sys.path.append('./scheme_tm.py')
sys.path.append('./algebra_tm.py')
sys.path.append('./tree_bool_tm.py')

import graph_tm
import tree_tm
import plot_fraspr_tm
import scheme_tm
import algebra_tm
import tree_bool_tm
import teorv_tm

def Cnm(n,m):
 if n<m:
   return 0
 return math.factorial(n)/(math.factorial(m)*math.factorial(n-m))

def powerset(s):
    result = [[]]
    for elem in s:
        result.extend([x + [elem] for x in result])
    return result 
 
def bool_num_term(n,m,nv=3):
 idig=pow(2,nv)
 print('start bool_num_term:',n,m,nv)
 a=random.randint(n,m)
 bits=[i<a for i in range(0,idig)]
 random.shuffle(bits)
 ii=0
 if nv==3:
    for i in range(0,idig):
        ii+=bits[i]*pow(2,i*2+1)
        ii+=bits[i]*pow(2,i*2)
    print('({:08b})'.format(ii)) 
 if nv==4:       
    for i in range(0,idig):
        ii+=bits[i]*pow(2,i)
    print('({:016b})'.format(ii)) 
 return ii

def Shuf(x):
 xx=list(x)
 random.shuffle(xx)
 return xx

def RB(s):
 return s.replace('[','\{').replace(']','\}') 
 
def Ninv(iPerf,l=16):
 ff=0
 if l==16:
    for i in range(0,l):
        ff+=(iPerf%2)*pow(2,l-1-i)
        iPerf=iPerf>>1
 if l==8:
    for i in range(0,l):
        ff+=(iPerf%2)*pow(2,l-1-i)
        iPerf=iPerf>>2
        
 return ff
 
 
def MakeTable(xyT,xHead,yHead,data,ff='{:4.2f}'):
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
   tb+=('&'+ff.format(data[id]))
   id=id+1
  tb+=('\\\\ \\hline')
 tb+=('\\end{tabular}')
 return tb

def MakeVector(data,ff=2,baks=1):
    tb='('
    for x in data:
        if(x>=0):    
            tb+=('{:g},'.format(x))
        else:
            tb+=('\\text{-}'+'{:g},'.format(-x))   
    tb=tb[:-1]
    return tb+')'
    

def MakeMatrix(data,ff=2,baks=1):
 print(data)
 tb=''
 for j in range (0,baks):
     tb+='$'
 tb+=(' \\begin{pmatrix*}[r]')
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
 tb+=(' \\end{pmatrix*}')
 for j in range (0,baks):
     tb+='$'
 return tb
 
def numprint(x,coef=''):
	res=''
	if x==0:
		return ''	
	if x==1:
		return '+'+coef
	if x==-1:
		return '-'+coef		
	if x>0:
		return '+'+str(x)+coef
	return str(x)+coef		

def MakeNormalDistr(a,sigm):
 return "$$ f_X(x)=\\frac{1}{"+(str(sigm) if sigm!=1 else "")+" \\sqrt{2 \\pi}} \\cdot e^{- \\frac{"+(("(x"+("-"+str(a) if a>0 else "+"+str(-a))+")^2") if a!=0 else ("x^2"))+"}{"+str(2*sigm*sigm)+"}} $$"

def EvalParams(dParams,**kwargs):
    NL='\n\n'
    SL='\\'
    pars={}
    print(dParams)
    for A in sorted(list(dParams.keys())):
     print(A)
     print(dParams[A])
     exec(str(A)+'='+str(dParams[A]),globals())
     pars[A]=eval(A,globals())
     print(pars[A])
    return pars 
def EvalAnswerCore(dAnsw,**kwargs):
    return str(eval(parser.expr( dAnsw ).compile()))    
def EvalAnswer(dParams,dAnsw):
    pp=EvalParams(dParams)
    return EvalAnswerCore(dAnsw,**pp)
AnsLabel0=['{{\\bf \\small 1) }}','{{\\bf \\small 2) }}','{{\\bf \\small 3) }}','{{\\bf \\small 4) }}']
AnsLabel=['{{ 1)~~}}','{{ 2)~~}}','{{ 3)~~}}','{{ 4)~~}}']
def MakeQAStyle(quest,ans,style): 
    qa=[]    
    enumstyle='\\flushleft\\begin{enumerate}[leftmargin=*,label={\\arabic*)},itemsep=0pt, parsep=0pt]\n'
    if(style=="'line'"):
        qa.append("\\vskip 2pt\n")
        qa.append(quest[0] + '\\vskip 2pt\n\\flushleft\n')
        for i in range(0,4):
            qa.append(AnsLabel[i]+ans[i]+'\n\n')
        return qa
    if(style=="'q_line'"):
        qa.append(quest[0] + '\\vskip 2pt\n\\flushleft\n')
        for i in range(0,4):
            qa.append(AnsLabel[i]+ans[i]+'\n\n')
        return qa
    if(style=="'line_item'"):
        qa.append(quest[0] + '\\vskip 2pt\n'+enumstyle)
        for i in range(0,4):
            qa.append('\\item '+ans[i]+'\n')
        qa.append('\\end{enumerate}\n')    
        return qa
    if(style=="'one_line'"):
        qa.append("\\vskip 2pt\n")
        qa.append(quest[0] + '\n')
        qa.append("\\vskip 2pt\n")
        for i in range(0,4):
            qa.append("\\begin{minipage}[r]{0.24\\linewidth}\n")
            qa.append(AnsLabel[i]+ans[i]+'\n')
            qa.append("\\end{minipage}\n")
        return qa
    if(style=="'qa_line_item'"):
        qa.append("\\vskip 2pt\n\n\\begin{minipage}[r]{0.25\\linewidth}\n")  
        qa.append(quest[0] + '\n\n')
        qa.append("\\end{minipage}\n")  
        qa.append("\\begin{minipage}[l]{0.75\\linewidth}\n"+enumstyle)  
        for i in range(0,4):
            qa.append('\\item '+ans[i]+'\n')
        qa.append("\\end{enumerate}\n\\end{minipage}\n")  
        return qa
    if(style=="'qa_line_item_inv'"):
        qa.append("\\vskip 2pt\\begin{minipage}[l]{0.75\\linewidth}\n"+enumstyle)  
        for i in range(0,4):
            qa.append('\\item '+ans[i]+'\n')
        qa.append("\\end{enumerate}\n\\end{minipage}\n")  
        qa.append("\n\n\\begin{minipage}[r]{0.25\\linewidth}\n")  
        qa.append(quest[0] + '\n\n')
        qa.append("\\end{minipage}\n")  
        return qa
    if(style=="'qa_line'"):
        qa.append("\\vskip 2pt\n\n\\begin{minipage}[r]{0.33\\linewidth}\n")  
        qa.append(quest[0] + '\n\n')
        qa.append("\\end{minipage}\n")  
        qa.append("\\begin{minipage}[l]{0.66\\linewidth}\n")  
        for i in range(0,4):
            qa.append(AnsLabel[i]+ans[i]+'\n\n')
        qa.append("\\end{minipage}\n")  
        return qa
    if(style=="'qa_line2'"):
        qa.append("\\vskip 2pt\n\n\\begin{minipage}[r]{0.5\\linewidth}\n")  
        qa.append(quest[0] + '\n\n')
        qa.append("\\end{minipage}\n")  
        qa.append("\\begin{minipage}[l]{0.5\\linewidth}\n")  
        for i in range(0,4):
            qa.append(AnsLabel[i]+ans[i]+'\n\n')
        qa.append("\\end{minipage}\n")  
        return qa
    if(style=="'qa_line_1_4'"):
        qa.append("\\vskip 2pt\n\n\\begin{minipage}[r]{0.25\\linewidth}\n")  
        qa.append(quest[0] + '\n\n')
        qa.append("\\end{minipage}\n")  
        qa.append("\\begin{minipage}[l]{0.75\\linewidth}\n")  
        for i in range(0,4):
            qa.append(AnsLabel[i]+ans[i]+'\n\n')
        qa.append("\\end{minipage}\n")  
        return qa
    if(style=="'qa_block'"):
        qa.append("\\vskip 2pt\n\n\\begin{minipage}[r]{0.33\\linewidth}\n\\flushleft\n")
        qa.append(quest[0] + '\n\n')
        qa.append("\\end{minipage}\n")  
        qa.append("\\begin{minipage}[l]{0.76\\linewidth}\n")
        for i in range(0,4):
          qa.append('\\begin{minipage}[c]{0.05\\linewidth}\n')
          qa.append(AnsLabel[i])
          qa.append('\\end{minipage}\n')      
          qa.append('\\begin{minipage}[c]{0.39\\linewidth}\n')
          qa.append(ans[i])
          qa.append('\\end{minipage}\n')
          if(i==1):
            qa.append('\n\n')
        qa.append("\\end{minipage}\n")  
        return qa
    if(style=="'qa_blockm'"):
        qa.append("\\vskip 2pt\n\n\\begin{minipage}[r]{0.33\\linewidth}\n\\flushleft\n")
        qa.append(quest[0] + '\n\n')
        qa.append("\\end{minipage}\n")  
        qa.append("\\begin{minipage}[l]{0.76\\linewidth}\n")
        for i in range(0,4):
          qa.append('\\begin{minipage}[c]{0.05\\linewidth}\n')          
          qa.append(AnsLabel[i])
          qa.append('\\end{minipage}\n')      
          qa.append('\\begin{minipage}[c]{0.3\\linewidth}\n')
          qa.append(ans[i])
          qa.append('\\end{minipage}\n')
          if(i==1):
            qa.append('\n\n')
            qa.append("\\vskip 2pt")
            qa.append('\n\n')
        qa.append("\\end{minipage}\n")
        return qa
    if(style=="'block'"):
        qa.append(quest[0] + '\\vskip 2pt\n\n')
        for i in range(0,4):
          qa.append('\\begin{minipage}[c]{0.04\\linewidth}\n')
          qa.append(AnsLabel[i])
          qa.append('\\end{minipage}\n')      
          qa.append('\\begin{minipage}[c]{0.44\\linewidth}\n')
          qa.append(ans[i])
          qa.append('\\end{minipage}\n')
          if(i==1):
            qa.append('\n\n')
        return qa
    if(style=="'img_row'"):
        qa.append(quest[0] + '\\vskip 2pt\n\n')
        qa.append('\\vskip -0.5cm\n')
#        qa.append('\\vskip 0.4cm\n')        
        for i in range(0,4):
          qa.append('\\begin{minipage}[c]{0.24\\linewidth}\n')
          qa.append('{\\vskip 0.5cm'+AnsLabel[i]+'}\n\\vskip -0.2cm\n')
          qa.append(ans[i])
          qa.append('\\end{minipage}\n')      
        return qa
    if (style == "'truth_tables'"):
        qa.append(quest[0] + '\\vskip 2pt\n\n')
        for i in range(0, 4):
            qa.append('\\begin{minipage}[c]{0.03\\linewidth}\n')
            qa.append(AnsLabel[i])
            qa.append('\\end{minipage}\hspace{5pt}\n')
            qa.append('\\begin{minipage}[c]{0.19\\linewidth}\n')
            qa.append(ans[i])
            qa.append('\\end{minipage}\n')
        return qa
    #default
    qa.append(quest[0] + '\\vskip 2pt\n\n')
    for i in range(0,4):
      qa.append('\\begin{minipage}[c]{0.02\\linewidth}\n')
      qa.append(AnsLabel[i])
      qa.append('\\end{minipage}\n')
      qa.append('\\begin{minipage}[c]{0.21\\linewidth}\n')
      qa.append(ans[i])
      qa.append('\\end{minipage}\n')      
    return qa
  
def ParseTaskWithParams(data,bAnswer,randAns,compl,**kwargs):
    rt=[]
    NL='\n\n'
    SL='\\'
    qast=''       
    na=False
    if("answer_style" in data):
     qast=data["answer_style"]
#    if not bAnswer and 'qa' in qast:
#        na=True
    
    if na:
        rt.append('\\begin{minipage}[]{0.55\\linewidth}\n')
    print(data['zadacha'])
    if not bAnswer and 'task_no_answer' in data:
        #rt.append(str(eval(parser.expr( data['task_no_answer'] ).compile()))+'\n')
        pass
    else:
        rt.append(str(eval(parser.expr( data['zadacha'] ).compile()))+'\n')
    if na:
        rt.append('\\end{minipage}\n')      
    otvs = []
    vopros='vopros'
    otvet='otvet'
    if not bAnswer and 'vopros_no_answer' in data:
        vopros='vopros_no_answer'
    if not bAnswer and 'otvet_no_answer' in data:
        otvet='otvet_no_answer'
    vv = sorted(list(data[vopros].keys()))
    oo = sorted(list(data[otvet].keys()))
    qnum=0
    if randAns:
     qnum=randAns-1
    print(vv)
    print(oo)
    vo = list(zip(vv, oo))
    quest=[]
    answ=[]
    if(len(vv)>4):
     random.shuffle(vv)
     rt.append(str(eval(parser.expr(data[vopros][vv[qnum]]).compile())) + '\n\n')
     return (rt, '')
    elif(len(vv)==4):
     #vv=['v1','v2','v3','v4']
     if not randAns:
      random.shuffle(vo)
     quest.append(str(eval(parser.expr(data[vopros][vo[qnum][0]]).compile())))
     for o in oo:
      otvs.append(str(eval(parser.expr( data[otvet][o] ).compile())))
    elif (len(data[vopros])==1):
     quest.append(str(eval(parser.expr(data[vopros]['v1']).compile()))+'\n\n')
     otvs.append(str(eval(parser.expr( data[otvet]['o1'] ).compile())))
     for i in range(2,5):
          otvs.append(EvalAnswer(data['param'],data[otvet]['o1']))
    elif (len(data[vopros])==2):
     if not bAnswer: # and 'vopros_no_answer' in data:
      #random.shuffle(vo)
#      if random.randint(0,2)==0:
       quest.append(str(eval(parser.expr(data[vopros]['v1']).compile()))+'\n\n')
       otvs.append(str(eval(parser.expr( data[otvet]['o1'] ).compile())))
#      else:
#        quest.append(str(eval(parser.expr(data[vopros]['v2']).compile()))+'\n\n')
#        otvs.append(str(eval(parser.expr( data[otvet]['o2'] ).compile())))
#      quest.append(str(eval(parser.expr(data[vopros][vo[0][0]]).compile()))+'\n\n')
#      otvs.append(str(eval(parser.expr( data[otvet][vo[0][1]] ).compile())))
     # otvs.append(str(eval(parser.expr( data[otvet][vo[1][1]] ).compile())))
     else: 
      quest.append(str(eval(parser.expr(data[vopros]['v1']).compile()))+'\n\n')
      otvs.append(str(eval(parser.expr( data[otvet]['o1'] ).compile())))
      for i in range(2,5):
          otvs.append(EvalAnswer(data['param'],data[otvet]['o2']))

    ncu0=oo.index(vo[qnum][1])    #number of correct answer    
    
    if not bAnswer:
        rt.append(quest[0]+'\n\n')
        return (rt,otvs[ncu0])
     
    if len(otvs) > len(set(otvs)):
        return ([],"")
    fl=0
    rrr=[0,1,2,3]
    random.shuffle(rrr)
    ncu=rrr.index(ncu0)
    
    
    for i in range(0,4):
       answ.append(otvs[rrr[i]])
    rt.extend(MakeQAStyle(quest,answ,qast))  
    #rt.append('\nCorrect answer: '+str(ncu+1))
    return (rt,str(ncu+1))
 
def ParseTask(data,bAnswer,randAns=0,compl=0):
   fl=1
   while fl:
    #z=open(TName,"r")
    #zz=z.read()
    #data=json.loads(zz)
    dPars={}
    if 'const_param' in data:
        cdPars=EvalParams(data['const_param'])
        rdPars=EvalParams(data['param'],**cdPars)
        dPars={**dPars,**rdPars}
    else:
        dPars=EvalParams(data['param'])
    print(dPars)
    aa= ParseTaskWithParams(data,bAnswer,randAns,compl,**dPars)
    if(len(aa[0])==0):
     continue
    else:
     return aa


def make_book_theme_head(TName,them_name,chap_name,part_name,ch=0,pa=0):
 th=[]
 if pa:
    th.append("\n~\n")
    th.append("\\vskip -21pt\n")
    th.append("\\begin{minipage}{\linewidth}\n")
    th.append("\\part{"+part_name+"}\n")
    th.append("\\gdef\parttitle{"+part_name+"}\n")
    th.append("\\thispagestyle{empty1}\n")
    th.append("\\end{minipage}\n")
 if ch:
    th.append("\n~\n")
    th.append("\\begin{minipage}{\linewidth}\n")
    th.append("\\chapter{"+chap_name+"}") 
    th.append("\\gdef\chaptertitle{"+chap_name+"}\n")
    th.append("\\end{minipage}\n\n")
 if '#' in them_name:
  (sn,sm)=them_name.split('#')
 else:
  sn=them_name
  sm=them_name
 th.append("\\begin{minipage}[]{\\linewidth} ")    
 th.append("\\section{"+sn+"}")
 th.append("\\end{minipage}") 
 th.append("\\sectionmark{"+sm+"}")
 #th.append("\n\\vskip -1.5cm\n")
 
 return th
def make_page_head(TName,Nz,ii):
 th=[]
 th.append("\\flushright{"+str(TName.replace('_','\\_'))+"}\n\n")
 #th.append("\\centering{ТЕСТ\n\n Теория Вероятностей и Математическая Статистика \n\n Вариант \\textnumero "+str(ii)+"}\n\n \\bigskip\n Уч.взв. \\underline{\\hspace{2cm}} ФИО \\underline{\\hspace{6cm}}\n\n")
 #th.append("\\centering{ТЕСТ\n\n Дискретная Математика \n\n Вариант \\textnumero "+str(ii)+"}\n\n \\bigskip\n Уч.взв. \\underline{\\hspace{2cm}} ФИО \\underline{\\hspace{6cm}}\n\n")
# th.append("\\centering{ТЕСТ по ТВ и МС. Вариант \\textnumero "+str(ii)+"("+str(TName)+")}\n\n \\bigskip\n Уч.взв. \\underline{\\hspace{2cm}} ФИО \\underline{\\hspace{6cm}}\n\n")
 th.append("\\centering Вариант \\textnumero "+str(ii)+".~~Уч.взв. \\underline{\\hspace{2cm}} ФИО \\underline{\\hspace{6cm}}\n\n")
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
 
def make_exam_page_head(TName,Nz,ii):
 th=[]
 th.append("\\begin{tabular}{|l|c|c|}");
 th.append("\\hline\n");
 th.append("\\begin{minipage}{0.3\\textwidth} ")
 th.append("\\centering")
 th.append("Военная академия связи")
 th.append("\\end{minipage}&")
 th.append("\\begin{minipage}{0.3\\textwidth} ")
 th.append("\\vspace{8pt} \\centering")
 th.append("{\\bf Билет \\textnumero "+str(ii)+"}\\\\")
 th.append("3 кафедра \\\\")
 th.append("Дисциплина Д3-503-03")
 th.append("\\end{minipage}&")
 th.append("\\begin{minipage}{0.3\\textwidth} ")
 th.append("\\vspace{8pt}  \\centering")
 th.append("Утверждаю\\\\ ")
 th.append("Заведующий кафедрой\\\\ ")
 th.append("\\underline{\\hskip 3cm}~~Е.~Рябоконь\\\\ ")
 th.append("10 марта~2021~г.\\\\ ")
 th.append("\\vspace{8pt}  ")
 th.append("\\end{minipage}\\\\ ")
 th.append("\\hline\n") 
 th.append("\multicolumn{3}{|l|}{\\begin{minipage}[t][.9\\textheight]{\\linewidth} ")
 return th
  
def make_test_head(TName,Nz):
 th=[]
 th.append("\\documentclass[12pt]{article}\n")
 th.append("\\usepackage{graphicx}\n")
 th.append("\\usepackage[fleqn]{amsmath}\n")
 th.append("\\usepackage{mathtools}\n")
 th.append("\\usepackage{enumitem}\n")
 th.append("\\usepackage[left=0.5cm,right=1cm,top=1cm,bottom=2cm,bindingoffset=0cm]{geometry}\n")
 th.append("\\usepackage[russian]{babel}\n")
 th.append("\\usepackage{rotating}\n")
 th.append("\\usepackage{supertabular}\n") 
 th.append("\\usepackage{multirow}\n")
 th.append("\\usepackage{chngcntr}\n")
 th.append("\\setlength{\\parindent}{0ex}\n") 
 th.append("\\pagenumbering{gobble}\n") 
 th.append("\\setenumerate{label=\\textbf{\\arabic*.}}\n")
 th.append("\\begin{document}\n")
 #th.append("Тест по теории вероятности "+str(datetime.datetime.now()))
 return th
def make_book_head(TName):
 th=[]
 th.append("\\documentclass[10pt,a5paper]{extbook}\n")
 th.append("\\usepackage{graphicx}\n")
 th.append("\\usepackage{amsmath}\n")
 th.append("\\usepackage{layout}\n")
 th.append("\\usepackage{mathtools}\n")
# th.append("\\usepackage[left=1.5cm,right=1.5cm,top=2cm,bottom=1.5cm,bindingoffset=0cm]{geometry}\n")
 th.append("\\usepackage[]{geometry}\n")
 th.append("\\usepackage[russian]{babel}\n")
 th.append("\\usepackage{fancyhdr}\n")
 th.append("\\usepackage{enumitem}\n")
 th.append("\\usepackage{rotating}")
 th.append("\\usepackage{supertabular}") 
 th.append("\\usepackage{multirow}")
 th.append("\\usepackage{multicol}\n")
 th.append("\\setlength{\\columnseprule}{0.4pt}\n")
 th.append("\\usepackage{chngcntr}\n")
 th.append("\\usepackage{titlesec}\n")
 th.append("\\usepackage{titletoc}\n")
 th.append("\\usepackage{tocloft}\n")
# th.append("\\usepackage{esvect}\n")

 th.append("\\setlength{\\parindent}{0ex}\n")
 
 th.append("\\setlength{\\headsep}{10pt}\n") 
 th.append("\\setlength{\\topmargin}{-21pt}\n") 
 th.append("\\setlength{\\oddsidemargin}{-21pt}\n") 
 th.append("\\setlength{\\evensidemargin}{-21pt}\n") 
 th.append("\\setlength{\\textwidth}{112mm}\n") 
# th.append("\\setlength{\\textheight}{174mm}\n")
 th.append("\\setlength{\\textheight}{473pt}\n")

 th.append("\\pagestyle{fancy}\n")

 #th.append("\\let\\Oldpart\\part\n")
 th.append("\\newcommand{\\parttitle}{}\n")
 #th.append("\\renewcommand{\\part}[1]{\\Oldpart{#1}\\renewcommand{\\parttitle}{#1}}\n")
 th.append("\\newcommand{\\chaptertitle}{}\n")

 th.append("\\renewcommand{\\thechapter}{~}\n")
 th.append("\\renewcommand{\\thepart}{~}\n")

 th.append("\\counterwithout{section}{chapter}\n")

 th.append("\\addto\\captionsrussian{\\renewcommand{\\chaptername}{Часть}}\n")

 th.append("\\titleformat{\\chapter}{\\large\\bfseries}{ }{3pt}{\\centering\\large\\bfseries}\n")

 th.append("\\titleclass{\\part}{straight}\n")
 th.append("\\titleclass{\\chapter}{straight}\n")
 th.append("\\titleclass{\\section}{straight}\n")
 th.append("\\titlespacing*{\\part}{0pt}{0pt}{0pt}\n")
 th.append("\\titlespacing*{\\chapter}{0pt}{0pt}{-5pt}\n")
 th.append("\\titlespacing*{\\section}{0pt}{0pt}{0pt}\n")

 th.append("\\titleformat{\\section}{\\bfseries}{\\thesection.~}{0pt}{\\bfseries}\n")
 th.append("\\titleformat{\\part}{\\Large\\bfseries}{}{3pt}{\centering\Large\\bfseries}\n")
 th.append("\\titleformat{\\chapter}{\\large\\bfseries}{}{3pt}{\centering\large\\bfseries}\n")

 th.append("\\renewcommand{\\chaptermark}[1]{}\n")
 th.append("\\renewcommand{\\sectionmark}[1]{\\markright{\\textbf{\\thesection.}~#1}}\n")


 th.append("\\renewcommand\\cftchapafterpnum{}\n")
 th.append("\\renewcommand\\cftsecafterpnum{}\n")


 th.append("\\fancypagestyle{fancy1}{ % \n")
 th.append("\\renewcommand{\\headrule}{\\vspace{2pt}\\hrule height 0.5pt \\vspace{1pt}\\hrule height 1pt}\n")
 th.append("\\fancyhead[CE]{\\small \\parttitle. \\chaptertitle}\n")
 th.append("\\fancyhead[CO]{\\small \\rightmark}\n")
 th.append("\\fancyhead[LE]{\\small \\bf{\\thepage}}\n")
 th.append("\\fancyhead[RO]{\\small \\bf{\\thepage}}\n")
 th.append("\\fancyhead[RE]{}\n")
 th.append("\\fancyhead[LO]{}\n")
 th.append("\\fancyfoot[C]{}}\n")
 
 th.append("\\fancypagestyle{plain1}{%\n")
 th.append("\\fancyhf{} \n")
 th.append("\\renewcommand{\\headrule}{\\vspace{2pt}\\hrule height 0.5pt \\vspace{1pt}\\hrule height 1pt}\n")
 th.append("\\fancyhead[CE]{}\n")
 th.append("\\fancyhead[CO]{}\n")
 th.append("\\fancyhead[LE]{\\small \\bf{\\thepage}}\n")
 th.append("\\fancyhead[RO]{\\small \\bf{\\thepage}}\n")
 th.append("\\fancyhead[RE]{}\n")
 th.append("\\fancyhead[LO]{}\n")
 th.append("\\fancyfoot[C]{} }\n")

 th.append("\\fancypagestyle{empty1}{%\n")
 th.append("\\fancyhf{} \n")
 th.append("\\renewcommand{\\headrule}{}\n")
 th.append("\\fancyfoot[C]{} }\n")
 
 th.append("\\setenumerate{label=\\textbf{\\thesection.\\arabic*.}}\n")
 th.append("\\renewcommand\\thesection{\\arabic{section}}\n")

 th.append("\\setlength{\\arraycolsep}{1pt}\n")
 th.append("\\setlength{\\tabcolsep}{2pt}\n")
 th.append("\\setlength{\\parskip}{\\baselineskip}\n")

 th.append("\\setlength{\\cftbeforetoctitleskip}{0pt}\n")
 th.append("\\setlength{\\cftaftertoctitleskip}{4pt}\n")
 th.append("\\setlength{\\cftbeforepartskip}{4pt}\n")
 th.append("\\setlength{\\cftbeforechapskip}{0pt}\n")
 th.append("\\setlength{\\cftbeforesecskip}{0pt}\n")
 th.append("\\setlength{\\cftchapindent}{-20pt}\n")
 th.append("\\setlength{\\cftsecindent}{-2pt}\n")
 
 th.append("\\addto\\captionsrussian{\\renewcommand{\\contentsname}{\\hfill О\\,Г\\,Л\\,А\\,В\\,Л\\,Е\\,Н\\,И\\,Е\\hfill}}\n")
 th.append("\\renewcommand{\\cfttoctitlefont}{\\large\\bfseries}\n")
 th.append("\\renewcommand{\\cftaftertoctitle}{ }\n")
 th.append("\\renewcommand{\\cftsecpresnum}{ }\n")
 th.append("\\renewcommand{\\cftsecaftersnum}{.}\n")
 th.append("\\renewcommand{\\cftpartfont}{\\hfil\\large\\bfseries\hspace{10pt}}\n")
 th.append("\\renewcommand{\\cftchapleader}{\\cftdotfill{\\cftdotsep}}\n")
 th.append("\\cftpagenumbersoff{part}\n")
 th.append("\\renewcommand{\\cftaftertoctitle}{\\thispagestyle{empty1}}\n")
 
 th.append("\\begin{document}\n")
# th.append("\\layout\n")
 th.append("\\pagestyle{plain1}\n")
 th.append("\\tableofcontents\n")
 th.append("\\clearpage\n")
 th.append("\\pagestyle{fancy1}\n")

 th.append("%Тест генератора сборника "+str(datetime.datetime.now()))
 return th

def make_book_head_solv(TName,fname):
 th=[]
 th.append("\\documentclass[10pt,a5paper]{extbook}\n")
 th.append("\\usepackage{graphicx}\n")
 th.append("\\usepackage{amsmath}\n")
 th.append("\\usepackage{layout}\n")
 th.append("\\usepackage{mathtools}\n")
# th.append("\\usepackage[left=1.5cm,right=1.5cm,top=2cm,bottom=1.5cm,bindingoffset=0cm]{geometry}\n")
 th.append("\\usepackage[]{geometry}\n")
 th.append("\\usepackage[russian]{babel}\n")
 th.append("\\usepackage{fancyhdr}\n")
 th.append("\\usepackage{enumitem}\n")
 th.append("\\usepackage{rotating}")
 th.append("\\usepackage{supertabular}") 
 th.append("\\usepackage{multirow}")
 th.append("\\usepackage{multicol}\n")
 th.append("\\setlength{\\columnseprule}{0.4pt}\n")
 th.append("\\usepackage{chngcntr}\n")
 th.append("\\usepackage{titlesec}\n")
 th.append("\\usepackage{titletoc}\n")
 th.append("\\usepackage{tocloft}\n")
# th.append("\\usepackage{esvect}\n")

 th.append("\\setlength{\\parindent}{0ex}\n")
 
 th.append("\\setlength{\\headsep}{10pt}\n") 
 th.append("\\setlength{\\topmargin}{-21pt}\n") 
 th.append("\\setlength{\\oddsidemargin}{-21pt}\n") 
 th.append("\\setlength{\\evensidemargin}{-21pt}\n") 
 th.append("\\setlength{\\textwidth}{112mm}\n") 
# th.append("\\setlength{\\textheight}{174mm}\n")
 th.append("\\setlength{\\textheight}{473pt}\n")

 th.append("\\pagestyle{fancy}\n")

 #th.append("\\let\\Oldpart\\part\n")
 th.append("\\newcommand{\\parttitle}{}\n")
 #th.append("\\renewcommand{\\part}[1]{\\Oldpart{#1}\\renewcommand{\\parttitle}{#1}}\n")
 th.append("\\newcommand{\\chaptertitle}{}\n")

 th.append("\\renewcommand{\\thechapter}{~}\n")
 th.append("\\renewcommand{\\thepart}{~}\n")

 th.append("\\counterwithout{section}{chapter}\n")

 th.append("\\addto\\captionsrussian{\\renewcommand{\\chaptername}{Часть}}\n")

 th.append("\\titleformat{\\chapter}{\\large\\bfseries}{ }{3pt}{\\centering\\large\\bfseries}\n")

 th.append("\\titleclass{\\part}{straight}\n")
 th.append("\\titleclass{\\chapter}{straight}\n")
 th.append("\\titleclass{\\section}{straight}\n")
 th.append("\\titlespacing*{\\part}{0pt}{0pt}{0pt}\n")
 th.append("\\titlespacing*{\\chapter}{0pt}{0pt}{-5pt}\n")
 th.append("\\titlespacing*{\\section}{0pt}{0pt}{0pt}\n")

 th.append("\\titleformat{\\section}{\\bfseries}{\\thesection.~}{0pt}{\\bfseries}\n")
 th.append("\\titleformat{\\part}{\\Large\\bfseries}{}{3pt}{\centering\Large\\bfseries}\n")
 th.append("\\titleformat{\\chapter}{\\large\\bfseries}{}{3pt}{\centering\large\\bfseries}\n")

 th.append("\\renewcommand{\\chaptermark}[1]{}\n")
 th.append("\\renewcommand{\\sectionmark}[1]{\\markright{\\textbf{\\thesection.}~#1}}\n")


 th.append("\\renewcommand\\cftchapafterpnum{}\n")
 th.append("\\renewcommand\\cftsecafterpnum{}\n")


 th.append("\\fancypagestyle{fancy1}{ % \n")
 th.append("\\renewcommand{\\headrule}{\\vspace{2pt}\\hrule height 0.5pt \\vspace{1pt}\\hrule height 1pt}\n")
 th.append("\\fancyhead[CE]{\\small \\parttitle. \\chaptertitle}\n")
 th.append("\\fancyhead[CO]{\\small \\rightmark}\n")
 th.append("\\fancyhead[LE]{\\small \\bf{\\thepage}}\n")
 th.append("\\fancyhead[RO]{\\small \\bf{\\thepage}}\n")
 th.append("\\fancyhead[RE]{}\n")
 th.append("\\fancyhead[LO]{}\n")
 th.append("\\fancyfoot[C]{}}\n")
 
 th.append("\\fancypagestyle{plain1}{%\n")
 th.append("\\fancyhf{} \n")
 th.append("\\renewcommand{\\headrule}{\\vspace{2pt}\\hrule height 0.5pt \\vspace{1pt}\\hrule height 1pt}\n")
 th.append("\\fancyhead[CE]{}\n")
 th.append("\\fancyhead[CO]{}\n")
 th.append("\\fancyhead[LE]{\\small \\bf{\\thepage}}\n")
 th.append("\\fancyhead[RO]{\\small \\bf{\\thepage}}\n")
 th.append("\\fancyhead[RE]{}\n")
 th.append("\\fancyhead[LO]{}\n")
 th.append("\\fancyfoot[C]{} }\n")

 th.append("\\fancypagestyle{empty1}{%\n")
 th.append("\\fancyhf{} \n")
 th.append("\\renewcommand{\\headrule}{}\n")
 th.append("\\fancyfoot[C]{} }\n")
 
 th.append("\\setenumerate{label=\\textbf{\\thesection.\\arabic*.}}\n")
 th.append("\\renewcommand\\thesection{\\arabic{section}}\n")

 th.append("\\setlength{\\arraycolsep}{1pt}\n")
 th.append("\\setlength{\\tabcolsep}{2pt}\n")
 th.append("\\setlength{\\parskip}{\\baselineskip}\n")

 th.append("\\setlength{\\cftbeforetoctitleskip}{0pt}\n")
 th.append("\\setlength{\\cftaftertoctitleskip}{4pt}\n")
 th.append("\\setlength{\\cftbeforepartskip}{4pt}\n")
 th.append("\\setlength{\\cftbeforechapskip}{0pt}\n")
 th.append("\\setlength{\\cftbeforesecskip}{0pt}\n")
 th.append("\\setlength{\\cftchapindent}{-20pt}\n")
 th.append("\\setlength{\\cftsecindent}{-2pt}\n")
 
 th.append("\\addto\\captionsrussian{\\renewcommand{\\contentsname}{\\hfill О\\,Г\\,Л\\,А\\,В\\,Л\\,Е\\,Н\\,И\\,Е\\hfill}}\n")
 th.append("\\renewcommand{\\cfttoctitlefont}{\\large\\bfseries}\n")
 th.append("\\renewcommand{\\cftaftertoctitle}{ }\n")
 th.append("\\renewcommand{\\cftsecpresnum}{ }\n")
 th.append("\\renewcommand{\\cftsecaftersnum}{.}\n")
 th.append("\\renewcommand{\\cftpartfont}{\\hfil\\large\\bfseries\hspace{10pt}}\n")
 th.append("\\renewcommand{\\cftchapleader}{\\cftdotfill{\\cftdotsep}}\n")
 th.append("\\cftpagenumbersoff{part}\n")
 th.append("\\renewcommand{\\cftaftertoctitle}{\\thispagestyle{empty1}}\n")
 
 th.append("\\begin{document}\n")
# th.append("\\layout\n")
 th.append("\\pagestyle{plain1}\n")
# th.append("\\tableofcontents\n")
# th.append("\\clearpage\n")
 th.append("\\pagestyle{fancy1}\n")

 th.append("%Тест генератора сборника "+str(datetime.datetime.now()))
 
 th.append("\n\n\\part{"+fname+"}\n")
 th.append("\\gdef\parttitle{"+fname+"}\n")
 th.append("\\gdef\chaptertitle{"+fname+"}\n") 
 return th

 
def add_task(*args):
 l2.insert('end',l1.get(l1.curselection()))
 l3.insert('end',str(curr_task_num.get()))
 curr_task_num.set(int(curr_task_num.get())+1)
 return

def add_task_nopp(*args):
 l2.insert('end',l1.get(l1.curselection()))
 l3.insert('end',str(curr_task_num.get()))
 return
 
 
def add_all_task(*args):
 for tkey in l1.get(0, END):
  l2.insert('end',tkey)
  l3.insert('end',str(curr_task_num.get()))
  curr_task_num.set(int(curr_task_num.get())+1)
 return
 
def remove_task(*args):
 l3.delete(l2.curselection())
 l2.delete(l2.curselection())
 return

def remove_all_task(*args):
 l2.delete(0, END)
 l3.delete(0, END)
 return
 
def select_theme(*args):
   #task_data={}
   if l0.curselection()==():
       return
   l1.delete(0, END)
   print(l0.curselection())
  # l0.
   #print(l0.get(l0.curselection()))

  # exit(0)
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
 
    f = codecs.open("./tex/"+test_name+'.tex', 'w', "utf-8-sig")
    f.writelines(make_book_head(test_name))
    fsolv = codecs.open("./tex/"+test_name+'_solv.tex', 'w', "utf-8-sig")
    fsolv.writelines(make_book_head_solv(test_name,test_name.replace('_','\_')))

    j={tkey_name:0 for tkey_name in l2.get(0, END)}
    ch_name0=''
    p_name0=''
    th_name=''
    for tkey_name in l2.get(0, END):
        if 'chapter' in task_data[tkey_name]:
            (part_name,ch_name)=task_data[tkey_name]['chapter'].split('.')
        else:
            ch_name=''
        if 'titleb' in task_data[tkey_name]:
            th_name=task_data[tkey_name]['titleb']
        else:
            th_name=tkey_name
        f.writelines(make_book_theme_head(test_name,th_name,ch_name,part_name,ch_name!=ch_name0,part_name!=p_name0))
        fsolv.write('\n\n')
        ch_name0=ch_name
        p_name0=part_name
        bAnswer=int(answer_type.get())
#        print(task_data[tkey_name])
#        print(not bAnswer)
#        print("task_style" in task_data[tkey_name])
#        print(task_data[tkey_name]["task_style"])
#        print(task_data[tkey_name]["task_no_answer"])
#        print(task_data[tkey_name]["task_style"]=="na1")
        lindent=10
        if not bAnswer and "task_no_answer" in task_data[tkey_name]:
            f.write('\n'+task_data[tkey_name]["task_no_answer"])
        if not bAnswer and "task_style" in task_data[tkey_name]:
            if task_data[tkey_name]["task_style"]=="na2":
                f.write("\\begin{multicols}{2}\n")
            if task_data[tkey_name]["task_style"]=="na3":
                f.write("\\begin{multicols}{3}\n")
            if task_data[tkey_name]["task_style"]=="na4":
                f.write("\\begin{multicols}{4}\n")
            lindent=0
        f.write("\\begin{enumerate}[leftmargin=*,wide, labelwidth=!,labelindent="+str(lindent)+"pt,nosep]\n")
        fsolv.write("\nВариант: "+str(tkey_name)+":  ")
        j[tkey_name]+=1
        i=0
        for iii in range(1, ntests):
            i=i+1
            tname=task_data[tkey_name]       
            f.write("\n\\vspace{4pt}\n\n\\begin{minipage}{\\linewidth}\n\\vskip 4pt\n\\item ")
            #f.write("\n\\vspace{8pt plus 0pt minus 8pt}\n\n\\begin{minipage}{\\linewidth}\n\\vskip 4pt\n\\item ")
            #task = ParseTask(tname,bAnswer,randAns=j[tkey_name],compl=0) #disable random in 4type task
            task = ParseTask(tname,bAnswer)
            filt_sc=[x.replace('includegraphics[]','includegraphics[scale=0.55]') for x in task[0]]
            f.writelines(filt_sc)
            fsolv.write(str(i)+":"+str(task[1])+"\n ")
            f.write("\n\\end{minipage}\n")
        fsolv.write("\n")
        f.write("\\end{enumerate}\n")
        if not bAnswer and "task_style" in task_data[tkey_name]:
            if task_data[tkey_name]["task_style"]!="na1":
                f.write("\\end{multicols}\n")
        f.write("\\newpage\n")
    f.write("\\end{document}\n")
    fsolv.write("\\end{document}\n")
    f.close()
    fsolv.close()
    tex_cmp = open('./tex/cmp_tex.bat', 'w')
    tex_cmp.write('latex "' + test_name + '.tex"\n')
    tex_cmp.write('dvips  "' + test_name + '.dvi"\n')
    tex_cmp.write('ps2pdf "' + test_name + '.ps"\n')
    tex_cmp.write('latex ' + test_name + '_solv.tex\n')
    tex_cmp.write('dvips  ' + test_name + '_solv.dvi\n')
    tex_cmp.write('ps2pdf ' + test_name + '_solv.ps\n')
    tex_cmp.close()
    os.chdir('tex')
    os.system('cmp_tex.bat')
    os.chdir('..')    
    return

def make_exam(*args):
    ntests = int(number_of_tests.get())
    bc=int(open('book_count').read().split()[0])
    with open('book_count', 'w') as f:
     f.write(str(bc+1))
    test_name=result_file_name.get()+'_'+str(bc)
    f = codecs.open("./tex/"+test_name+'.tex', 'w', "utf-8-sig")
    f.writelines(make_test_head(test_name,l2.size()))
    fsolv = codecs.open("./tex/"+test_name+'_solv.tex', 'w', "utf-8-sig")
    fsolv.writelines(make_book_head_solv(test_name,test_name.replace('_','\_')))

    quests=list(l2.get(0, END))
    numbers=list(l3.get(0, END))
    stacked_quests={}
    for i in range(len(quests)):
        if numbers[i] in stacked_quests:
            stacked_quests[numbers[i]].append(quests[i])
        else:
            stacked_quests[numbers[i]]=[quests[i]]
    for iii in range(1, ntests):
        f.writelines(make_exam_page_head(test_name,l2.size(),iii))
        f.write("\n\\vspace{8pt plus 0pt minus 8pt}")
        f.write("\\begin{enumerate}[leftmargin=*,wide, labelwidth=!,labelindent=10pt,nosep]\n")
        #fsolv.write("Вариант: "+str(iii)+"\n")
        fsolv.write("\n\nВариант: "+str(iii)+":  \n\n")
        i=0
        qlist=[int(a) for a in list(stacked_quests.keys())]
        print(qlist)
        for iqi in sorted(qlist):
            qi=str(iqi)
            tkey_name=stacked_quests[qi][random.randint(0,len(stacked_quests[qi]))-1]
            i=i+1
            tname=task_data[tkey_name]
            f.write("\n\\begin{minipage}{\\linewidth}\n\\vskip 4pt\n\\item ")            
            bAnswer=int(answer_type.get())
            if not bAnswer and "task_no_answer" in task_data[tkey_name]:
                f.write('\n'+task_data[tkey_name]["task_no_answer"]+'\n\n')
            task = ParseTask(tname,bAnswer)
            filt_sc=[x.replace('includegraphics[]','includegraphics[scale=0.6]') for x in task[0]]
            f.writelines(filt_sc)
            fsolv.write(str(i)+":"+str(task[1])+" \n\n")
            f.write("\n\\end{minipage}\n")
        fsolv.write("\n")
        f.write("\\end{enumerate}\n")
        f.write("\n\\vfill\n ")            
        f.write("\\end{minipage}} \\\\ \n")
        f.write("\\hline\n")
        f.write("\\end{tabular}\n")
        f.write("\\newpage\n")
    f.write("\\end{document}\n")
    f.close()
    fsolv.write("\\end{document}\n")
    fsolv.close()
    tex_cmp = open('./tex/cmp_tex.bat', 'w')
    tex_cmp.write('latex "' + test_name + '.tex"\n')
    tex_cmp.write('dvips  "' + test_name + '.dvi"\n')
    tex_cmp.write('ps2pdf "' + test_name + '.ps"\n')
    tex_cmp.write('latex ' + test_name + '_solv.tex\n')
    tex_cmp.write('dvips  ' + test_name + '_solv.dvi\n')
    tex_cmp.write('ps2pdf ' + test_name + '_solv.ps\n')
    tex_cmp.close()
    os.chdir('tex')
    os.system('cmp_tex.bat')
    os.chdir('..')
    return


    
def make_test(*args):
    ntests = int(number_of_tests.get())
    bc=int(open('book_count').read().split()[0])
    with open('book_count', 'w') as f:
     f.write(str(bc+1))
    test_name=result_file_name.get()+'_'+str(bc)
    #f = open("./tex/"+test_name+'.tex', 'w')
    f = codecs.open("./tex/"+test_name+'.tex', 'w', "utf-8-sig")
    f.writelines(make_test_head(test_name,l2.size()))
#    fsolv = open("./tex/"+test_name+'_solv.tex', 'w')
    fsolv = codecs.open("./tex/"+test_name+'_solv.tex', 'w', "utf-8-sig")
    fsolv.writelines(make_book_head_solv(test_name,test_name.replace('_','\_')))

    category = moodlexport.Category(test_name)



    for iii in range(1, ntests):
        f.writelines(make_page_head(test_name,l2.size(),iii))
        f.write("\\begin{enumerate}[leftmargin=*,wide, labelwidth=!,labelindent=10pt,nosep]\n")
        #fsolv.write("Вариант: "+str(iii)+"\n")
        fsolv.write("\n\nВариант: "+str(iii)+":  ")
        i=0
        for tkey_name in l2.get(0, END):
            i=i+1
            tname=task_data[tkey_name]
            f.write("\n\\vspace{8pt plus 0pt minus 8pt}\n\n\\begin{minipage}{\\linewidth}\n\\vskip 4pt\n\\item ")            
            bAnswer=int(answer_type.get())
            if not bAnswer and "task_no_answer" in task_data[tkey_name]:
                f.write('\n'+task_data[tkey_name]["task_no_answer"]+'\n\n')
            task = ParseTask(tname,bAnswer)
            f.writelines(task[0])

#            question = moodlexport.Question("multichoice")
#            question.text('\n'.join(task[0]))
#            question.grade(1.0)
#            for ii in range (1,5):
#                question.answer(str(i), ii==int(task[1]))
#            question.addto(category)


            if bAnswer:
                fsolv.write(str(i)+":"+str(task[1])+" ")
            else:
                fsolv.write(str(i)+":"+str(task[1])+"\n\n")
            
            f.write("\n\\end{minipage}\n")
        fsolv.write("\n")
        f.write("\\end{enumerate}\n")
        f.write("\\newpage\n")
    f.write("\\end{document}\n")
    f.close()
    fsolv.write("\\end{document}\n")
    fsolv.close()
    category.save()
    tex_cmp = open('./tex/cmp_tex.bat', 'w')
    tex_cmp.write('latex "' + test_name + '.tex"\n')
    tex_cmp.write('dvips  "' + test_name + '.dvi"\n')
    tex_cmp.write('ps2pdf "' + test_name + '.ps"\n')
    tex_cmp.write('latex ' + test_name + '_solv.tex\n')
    tex_cmp.write('dvips  ' + test_name + '_solv.dvi\n')
    tex_cmp.write('ps2pdf ' + test_name + '_solv.ps\n')
    tex_cmp.close()
    os.chdir('tex')
    os.system('cmp_tex.bat')
    os.chdir('..')
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

l0 = Listbox(mainframe, height=30,width=60)
l0.grid(column=-2+col0, row=0+row0, sticky=(N,W,E,S),rowspan = 15)
s0 = ttk.Scrollbar(mainframe, orient=VERTICAL, command=l0.yview)
s0.grid(column=-1+col0, row=0+row0, sticky=(N,S),rowspan = 15)
l0['yscrollcommand'] = s0.set
l0.bind('<<ListboxSelect>>', select_theme)
l0.activate(2)

l1 = Listbox(mainframe, height=30,width=60)
l1.grid(column=0+col0, row=0+row0, sticky=(N,W,E,S),rowspan = 15)
s1 = ttk.Scrollbar(mainframe, orient=VERTICAL, command=l1.yview)
s1.grid(column=1+col0, row=0+row0, sticky=(N,S),rowspan = 15)
l1['yscrollcommand'] = s1.set
l1.activate(2)

l2 = Listbox(mainframe, height=30,width=60)
l2.grid(column=3+col0, row=0+row0, sticky=(N,W,E,S),rowspan = 15)
l3 = Listbox(mainframe, height=30,width=5)
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
curr_task_num=StringVar()
#tester_style=StringVar()

number_of_tests.set(10)
answer_type.set(1)
curr_task_num.set(1)
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

ttk.Button(mainframe, text="MakeExam", command=make_exam, width = 13).grid(column=2+col0, row=13+row0, sticky=(W,N),columnspan = 1)

ttk.Label(mainframe, text="Номер задачи:").grid(column=2+col0, row=14+row0, sticky=W)
ttk.Entry(mainframe,textvariable=curr_task_num,  width=6).grid(column=2+col0, row=15+row0,  sticky=(W, E), columnspan = 1)

ttk.Button(mainframe, text="==>>", command=add_task_nopp, width = 13).grid(column=2+col0, row=16+row0, sticky=(W,N),columnspan = 1)


ttk.Label(mainframe, text="Тема:").grid(column=-2+col0, row=-1+row0, sticky=W)
ttk.Label(mainframe, text="Задача:").grid(column=0+col0, row=-1+row0, sticky=W)

#for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
jz=open("./tasks/tlist.json","r")
jzz=jz.read()
themdata=json.loads(jzz)
print(themdata)
task_data={}
theme_data={}
for theme in sorted(list(themdata.keys())):
    ttitle=str(theme)
    print(ttitle)
    l0.insert('end',ttitle)
    theme_data[ttitle]=themdata[theme]
root.mainloop()
