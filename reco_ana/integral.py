import numpy as np
from scipy import integrate


def integrand(x, y):
    return -1 + x**2*y**2

x_lower = -1  
x_upper = 1 
y_lower = -1  
y_upper = 1 

result, error = integrate.dblquad(integrand, y_lower, y_upper, lambda y: x_lower, lambda y: x_upper)

print(f"result:{result}")
print(f"error:{error}")
