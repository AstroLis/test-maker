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
#   tb+=('&'+'{:4.2f}'.format(data[id]))
   tb+=('&'+str(data[id]))
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
   tb+=('{:g}'.format(x))
  tb+=('\\\\')
 tb+=(' \\end{pmatrix}$$')
 return tb
