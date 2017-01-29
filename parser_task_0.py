import json,random,parser
def ParseTask(TName):
    z=open(TName)
    data=json.load(z)
    print(data)
    print(data['param'])
    print(data['param']['A1'])
    A1=eval(parser.expr( data['param']['A1'] ).compile())
    A2=eval(parser.expr( data['param']['A2'] ).compile())
    print(A1,A2)
    print(eval(parser.expr( data['zadacha'] ).compile()))
    print()
    if(random.randint(1,4)==1):
        print(data['vopros']['v1'])
    else:
        print(data['vopros']['v2'])
    print(eval(parser.expr( data['otvet']['o1'] ).compile()))
    print(eval(parser.expr( data['otvet']['o2'] ).compile()))
    print(eval(parser.expr( data['otvet']['o3'] ).compile()))
    print(eval(parser.expr( data['otvet']['o4'] ).compile()))
ParseTask("zadacha.json")

