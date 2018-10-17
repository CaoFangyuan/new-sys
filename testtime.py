import datetime
import numpy as np

starttime = datetime.datetime.now()
i = 0
while i<10000:
    q = [1.567,3.234,4.568,7.123]
    a = [0,0,0,0]
    a[0] = q[0]
    a[1] =-q[1]
    a[2] =-q[2]
    a[3] =-q[3]
    i = i+1
end = datetime.datetime.now()
print( str(end-starttime))

start = datetime.datetime.now()
i = 0
while i<10000:
    q = np.array([[1.567],[3.234],[4.568],[7.123]])
    q1 = np.array([[0,-1,-1,-1]])
    a = np.dot(q,q1)
    i = i+1
end = datetime.datetime.now()
print( str(end-start))
