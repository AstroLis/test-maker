import random
import sympy


def make_laplace_pair(omega=sympy.Symbol('omega', real=True),a=sympy.Symbol('a', real=True),index=0):
    t = sympy.Symbol('t', real=True)
    s = sympy.Symbol('s', real=True)
    def L(f):
        return sympy.laplace_transform(f, t, s, noconds=True)
#    omega = sympy.Symbol('omega', real=True)
    exp = sympy.exp
    sin = sympy.sin
    cos = sympy.cos
    functions = [a,
             a*t,
             omega*t**a,
             exp(-a*t),
             exp(a*t),
             sin(omega*t),
             cos(omega*t),
             sin(omega*t+a),
             cos(omega*t-a),
             t**omega*exp(-a*t),
             exp(-a*t)*sin(omega*t),
             exp(-a*t)*cos(omega*t),
             t**omega*exp(a*t),
             exp(a*t)*sin(omega*t),
             exp(a*t)*cos(omega*t)
             ]
    Fs = [L(f) for f in functions]
    return functions[index],Fs[index]


def make_laplace_task(num=3):
    inum=3
    f=None
    F=None
    if num==3:
        ii=[random.randint(0,4),random.randint(5,9),random.randint(10,14)]
    if num==1:
        ii=[random.randint(0,1),random.randint(2,3),random.randint(5,6)]
    if num==2:
        ii=[random.randint(7,8),random.randint(9,10),random.randint(11,14)]
        
    for i in range(inum):
        print(ii[i])
        fi,Fi=make_laplace_pair(random.randint(1,10),random.randint(1,10),ii[i])
        if f==None:
            f=fi
            F=Fi
        else:
            f+=fi
            F+=Fi
    return f,F
        
if __name__ == "__main__":
    for i in range(10):
        print(make_laplace_task(num=3))