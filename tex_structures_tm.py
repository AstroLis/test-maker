def MakeTable(xyT,xHead,yHead,data,ff=2,yAlign=1):
 tb=''
 tb+=('\\begin{tabular}{|c|')
 for x in xHead:
  tb+=('c|')
 tb+=('} \\hline ')
 if yAlign:
  tb+=(str(xyT))
 for x in xHead:
  if yAlign:
   tb+=('&')
  tb+=(str(x))
  if not yAlign:
   tb+=('&')
 if not yAlign:
  tb+=(str(xyT))
 tb+=('\\\\ \\hline')
 id=0
 for y in yHead:
  if yAlign:
   tb+=(str(y))
  for x in xHead:
#   tb+=('&'+'{:4.2f}'.format(data[id]))
   if yAlign:
    tb+=('&')
   tb+=(str(data[id]))
   if not yAlign:
    tb+=('&')
   id=id+1
  if not yAlign:
   tb+=(str(y))   
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
