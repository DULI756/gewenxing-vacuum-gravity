# -*- coding: utf-8 -*-
"""诊断: 氘核 sep=1.989 单偶极 vs 10/11源J17展开, 决定氦核第一版口径
单偶极口径: 每核子一个115.9μN偶极于质心 (vs 10源均分全同向=总115.9μN)
"""
import numpy as np
mu0=1.25663706212e-6; muN=5.050783699e-27; MeV=1.602176634e-13
rp=0.84e-15; sep=1.989e-15
R0,hh,axH=0.4238,0.2520,0.6758; sq=np.sqrt(2)
J17=np.array([(R0,0,-hh),(0,R0,-hh),(-R0,0,-hh),(0,-R0,-hh),
 (R0/sq,R0/sq,hh),(-R0/sq,R0/sq,hh),(-R0/sq,-R0/sq,hh),(R0/sq,-R0/sq,hh),
 (0,0,axH),(0,0,-axH)],float)
def dip(P,pos,m):
    rv=P-pos; r=np.maximum(np.linalg.norm(rv,axis=1),1e-30); rh=rv/r[:,None]
    md=np.einsum('ij,j->i',rh,m)
    return (mu0/(4*np.pi*r[:,None]**3))*(3*md[:,None]*rh-m[None,:])

def E_int(calc,res=0.033):
    d=res*1e-15; xs=np.arange(-2e-15,sep+2e-15,d); L=2.2e-15
    ys=np.arange(-L,L,d); zs=np.arange(-L,L,d); E=0.0
    for z in zs:
        Y,X=np.meshgrid(ys,xs); P=np.column_stack([X.ravel(),Y.ravel(),np.full_like(X.ravel(),z)])
        core=(np.linalg.norm(P,axis=1)<rp)|(np.linalg.norm(P-np.array([sep,0,0]),axis=1)<rp)
        P=P[~core]; Bp,Bn=calc(P)
        E+=np.sum((Bp*Bn).sum(axis=1))/mu0*(d**3)
    return E/MeV

# 单偶极: 质子+115.9μN于原点, 中子-115.9μN于(sep,0,0)
def calc_dip(P):
    return dip(P,np.array([0.,0,0]),np.array([0.,115.9*5.050783699e-27,0])),\
           dip(P,np.array([sep,0.,0]),np.array([0.,-115.9*5.050783699e-27,0]))
# 10/11源展开
posA=J17*rp; posB=np.vstack([J17*rp,np.array([0.,0,0])]); pb=posB.copy(); pb[:,0]+=sep
mup=115.9*5.050783699e-27
mA=np.tile([0,mup/10,0],(10,1)); mB=np.tile([0,-mup/11,0],(11,1))
def calc_expand(P):
    Bp=sum(dip(P,posA[i],mA[i]) for i in range(10))
    Bn=sum(dip(P,pb[j],mB[j]) for j in range(11))
    return Bp,Bn
print("氘核 sep=1.989fm, E_int=∫Bp·Bn/μ0 dV")
print(f"  单偶极(115.9μN质心): {E_int(calc_dip):.4f} MeV")
print(f"  10/11源J17展开:     {E_int(calc_expand):.4f} MeV (参考_verify=已闭合)")
