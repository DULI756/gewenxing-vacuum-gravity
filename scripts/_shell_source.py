# -*- coding: utf-8 -*-
"""球对称壳源（非点源）快速版：检验两源重叠积分是否仍振荡 / 是否恢复 e^(-r/d)。"""
import numpy as np
c=3e8; f0=1.2799e23; lam=c/f0*1e15; k=2*np.pi/lam; d=lam/2.0
Rc=2.0
g=np.linspace(-Rc,Rc,41); X,Y,Z=np.meshgrid(g,g,g); dv=(g[1]-g[0])**3
P=np.stack([X.ravel(),Y.ravel(),Z.ravel()],axis=1)   # (Np,3)

def I(r,a,Ns=80):
    u=np.random.default_rng(int(r*1000)).normal(size=(Ns,3)); u/=np.linalg.norm(u,axis=1,keepdims=True)
    R1=np.array([-r/2,0,0])[None,:]+a*u
    R2=np.array([+r/2,0,0])[None,:]+a*u
    dS=np.linalg.norm(P[:,None,:]-R1[None,:,:],axis=2)+1e-9
    dT=np.linalg.norm(P[:,None,:]-R2[None,:,:],axis=2)+1e-9
    val=np.cos(k*(dS-dT))/(dS*dT)
    return val.sum()*dv

rs=np.arange(0.3,2.01,0.1)
for a in [0.25,0.5,0.8]:
    Is=np.array([I(r,a) for r in rs]); F=-np.gradient(Is,rs)
    z=int(((F[:-1]*F[1:])<0).sum())
    m=(rs>=0.8)&(rs<=1.8); sl=np.polyfit(rs[m],np.log(np.abs(F[m])+1e-12),1)[0]
    print("壳 a=%.2f: 过零点=%d, ln|F|斜率(0.8-1.8)=%.2f (期望-1/d=%.2f)"%(a,z,sl,-1/d))
