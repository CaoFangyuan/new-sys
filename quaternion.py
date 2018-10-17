import math
import numpy as np
def quatern_conj_program(q_initial):
    a_new = [0,0,0,0]
    a_new[0] = q_initial[0]
    a_new[1] = -q_initial[1]
    a_new[2] = -q_initial[2]
    a_new[3] = -q_initial[3]
    return a_new

def quaternprod(q1,q2):
    q_new = [0,0,0,0]
    q_new[0] = q1[0]*q2[0]-q1[1]*q2[1]-q1[2]*q2[2]-q1[3]*q2[3]
    q_new[1] = q1[0]*q2[1]+q1[1]*q2[0]+q1[2]*q2[3]-q1[3]*q2[2] 
    q_new[2] = q1[0]*q2[2]+q1[2]*q2[0]+q1[3]*q2[1]-q1[1]*q2[3] 
    q_new[3] = q1[0]*q2[3]+q1[3]*q2[0]+q1[1]*q2[2]-q1[2]*q2[1]
    return q_new

def quaternionToMatrix(q):
    p00 = q[0]*q[0]
    p01 = q[0]*q[1]
    p02 = q[0]*q[2]
    p03 = q[0]*q[3]
    p11 = q[1]*q[1]
    q12 = q[1]*q[2]
    q13 = q[1]*q[3]
    q22 = q[2]*q[2]
    q23 = q[2]*q[3]
    q33 = q[3]*q[3]
    M = array([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
    M = asmatrix(M)
    M[0,0] = p00+p11-p22-p33
    M[0,1] = 2*(p12-p03)
    M[0,2] = 2*(p13+p02)
    M[1,0] = 2+(p12+p03)
    M[1,1] = p00-p11+p22-p33
    M[1,2] = 2*(p23-p01)
    M[2,0] = 2*(p13-p02)
    M[2,1] = 2*(p23+p01)
    M[2,2] = p00-p11-p22+p33
    return M
