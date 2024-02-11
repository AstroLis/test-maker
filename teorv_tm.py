import numpy as np


def MarkovMatrix(n):
    m=np.zeros((n,n))
    for i in range(n):
        for j in range(n-1):
            m[i,j]=np.random.randint(1,10//n+1)
        m[i,n-1]=10-np.sum(m[i,:])
    return m/10

mm=MarkovMatrix(3)
print(mm)