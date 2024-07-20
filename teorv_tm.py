import numpy as np


def MarkovMatrix(n):
    m=np.zeros((n,n))
    for i in range(n):
        for j in range(n-1):
            m[i,j]=np.random.randint(1,10//n+1)
        m[i,n-1]=10-np.sum(m[i,:])
    return m/10


def MarkovMatrixIntens(n):
    m=np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            m[i,j]=np.random.randint(1,10)
        m[i,i]=0
    return m

def MarkovIntens2Prob(m):
    a=np.zeros((m.shape[0]+1,m.shape[1]))
    a[0,0]=-(m[0,1]+m[0,2])
    a[0,1]=m[1,0]
    a[0,2]=m[2,0]
    a[1,0]=m[0,1]
    a[1,1]=-(m[1,0]+m[1,2])
    a[1,2]=m[2,1]
    a[2,0]=m[0,2]
    a[2,1]=m[1,2]
    a[2,2]=-(m[2,0]+m[2,1])
    a[3,:]=np.ones(m.shape[0])
    v=np.zeros(m.shape[0]+1)
    v[m.shape[0]]=1
    res=np.linalg.lstsq(a,v)
    print(res)
    print(res[0])
    return res[0]

def MarkovIntens2Prob2x2(m):
    a=np.zeros((m.shape[0]+1,m.shape[1]))
    a[0,0]=-(m[0,1])
    a[0,1]=m[1,0]
    a[1,0]=m[0,1]
    a[1,1]=-(m[1,0])
    a[2,:]=np.ones(m.shape[0])
    v=np.zeros(m.shape[0]+1)
    v[m.shape[0]]=1
    res=np.linalg.lstsq(a,v)
    print(res)
    print(res[0])
    return(res[0])


#mm=MarkovMatrix(3)
#print(mm)

mm=MarkovMatrixIntens(3)
print(mm)
MarkovIntens2Prob(mm)
mm[2,:]=np.zeros(3)
mm[:,2]=np.zeros(3)
print(mm)
MarkovIntens2Prob(mm)
MarkovIntens2Prob2x2(mm[:2,:2])
