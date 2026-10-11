# -*- coding: utf-8 -*-
import numpy as np
mu0=1.25663706212e-6; muN=5.050783699e-27; MeV=1.602176634e-13
rp=0.84e-15; sep=1.989e-15
def dip(P,pos,m):
    rv=P-pos; r=np.maximum(np.linalg.norm(rv,axis=1),1e-30); rh=rv/r[:,None]
    md=np.einsum('ij,j->i',rh,m)
    return (mu0/(4*np.pi*r[:,None]**3))*(3*md[:,None]*rh-m[None,:])
def E_dip(res=0.033):
    d=res*1e-15; xs=np.arange(-2e-15,sep+2e-15,d); L=2.2e-15
    ys=np.arange(-L,L,d); zs=np.arange(-L,L,d); E=0.0
    m=115.9*muN
    for z in zs:
        Y,X=np.meshgrid(ys,xs); P=np.column_stack([X.ravel(),Y.ravel(),np.full_like(X.ravel(),z)])
        core=(np.linalg.norm(P,axis=1)<rp)|(np.linalg.norm(P-np.array([sep,0,0]),axis=1)<rp)
        P=P[~core]
        Bp=dip(P,np.array([0.,0,0]),np.array([0.,m,0]))
        Bn=dip(P,np.array([sep,0.,0]),np.array([0.,-m,0]))
        E+=np.sum((Bp*Bn).sum(axis=1))/mu0*(d**3)
    return E/MeV
print("单偶极 E_int =", E_dip(), "MeV")
with open(r"D:\波源\verification\_dip_only_out.txt","w",encoding="utf-8") as f:
    f.write(str(E_dip()))
