import random
from pyx import *
def MakeGraphFrasprTM(x,ppx):
 varc=open('fraspr_gr_count','r')
 v_cou=int(varc.readline())
 varc.close()
 v_cou+=1
 px=[]
 s=0
 for p in ppx:
  s=s+p
  px.append(s)
 print(x,ppx,px)
 ccc=canvas.canvas()
 sc=2.5
 mx=9
 ccc.stroke(path.line(-sc/3,0, sc, 0),[deco.earrow([deco.filled()])])
 ccc.stroke(path.line(0,-0.1, 0, sc*5/4),[deco.earrow([deco.filled()])])
 for i in range(0,len(x)-1):
  ccc.stroke(path.line(x[i+1]/mx*sc,px[i]*sc, x[i]/mx*sc, px[i]*sc),[deco.earrow([deco.filled()]),style.linewidth(sc/100)])
  ccc.stroke(path.line(0,px[i]*sc, x[i]/mx*sc, px[i]*sc),[style.linestyle.dashed])
  ccc.stroke(path.line(x[i]/mx*sc,0, x[i]/mx*sc, px[i]*sc),[style.linestyle.dashed])
  ccc.text(-0.5,px[i]*sc-0.1, str(int(px[i]*100)/100)) 
  ccc.text(x[i]/mx*sc-0.1,-0.4, str(x[i])) 
 ccc.stroke(path.line(x[0]/mx*sc,0, -sc/4, 0),[deco.earrow([deco.filled()]),style.linewidth(sc/100)])
 i=len(x)-1
 ccc.stroke(path.line(sc,px[i]*sc, x[i]/mx*sc, px[i]*sc),[deco.earrow([deco.filled()]),style.linewidth(sc/100)])
 ccc.stroke(path.line(0,px[i]*sc, x[i]/mx*sc, px[i]*sc),[style.linestyle.dashed])
 ccc.stroke(path.line(x[i]/mx*sc,0, x[i]/mx*sc, px[i]*sc),[style.linestyle.dashed])
 ccc.text(-0.5,px[i]*sc-0.1, str(px[i])) 
 ccc.text(x[i]/mx*sc-0.1,-0.4, str(x[i])) 
 text.set(text.LatexRunner)
 ccc.text(-1.2,sc*5/4-0.1, "$F_X(x)$") 
 #ccc.text(-0.4,sc*5/4-0.15, "X",[text.size.small])
 ccc.text(sc,-sc/15, "$x$") 
 grfile="fraspr"+str(v_cou)+".eps"
 ccc.writeEPSfile("fraspr"+str(v_cou))
 vc = open('fraspr_gr_count', 'w')
 vc.write(str(v_cou))
 vc.close()  
 return grfile
x=[1,2,3,4]
px=[0.3,0.1,0.4,0.2]
#px=[0.3,0.4,0.8,1.0]
#MakeGraphFrasprTM(x,px)