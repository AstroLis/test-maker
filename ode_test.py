import sympy
from sympy import Function, dsolve, Derivative, checkodesol

from sympy.abc import x

y = Function('y')

# Solve the ODE

eq=Derivative(y(x), x, x)-4*Derivative(y(x), x) - 21 * y(x) + sympy.log(x)

print('eq:',eq)

result = dsolve(eq)

print('solution:',result)



#result = dsolve(Derivative(y(x), x, x) + 9*y(x), y(x))

#print(result)
#Eq(y(x), C1*sin(3*x) + C2*cos(3*x))

# Check that the solution is correct

#print(checkodesol(Derivative(y(x), x, x) + 9*y(x), result))
#(True, 0)
