# -*- coding: utf-8 -*-
"""验证 sep≈1.99fm 处氘核重叠场能差闭合的数值可靠性(高分辨率)
口径全独立: 源磁矩115.9μN(磁自能反推), τ_b=0.5(磁自能闭环), sep=1.989(氘核实验距离)
"""
import numpy as np
mu0=1.25663706212e-6; muN=5.050783699e-27; MeV=1.602176634e-13
E_target=2.2246; tau_b=0.5
rp=0.84e-15
R0,hh,axH=0.4238,0.2520,0.6758; sq=np.sqrt(2)
J17=np.array([(R0,0,-hh),(0,R0,-hh),(-R0,0,-hh),(0,-R0,-hh),
 (R0/sq,R0/sq,hh),(-R0/sq,R0/sq,hh),(-R0/sq,-R0/sq,hh),(R0/sq,-R0/sq,hh),
 (0,0,axH),(0,0,-axH)],float)
posA=J17*rp; posB=np.vstack([J17*rp,np.array([0.,0,0])])
mup=115.9*muN; mA=np.tile([0,mup/10,0],(10,1)); mB=np.tile([0,-mup/11,0],(11,1))
def E_int_at(sep):
    pb=posB.copy(); pb[:,0]+=sep
    def dip(P,pos,m):
        rv=P-pos; r=np.maximum(np.linalg.norm(rv,axis=1),1e-30); rh=rv/r[:,None]
        md=np.einsum('ij,j->i',rh,m)
        return (mu0/(4*np.pi*r[:,None]**3))*(3*md[:,None]*rh-m[None,:])
    for res in [0.04,0.033]:
        d=res*1e-15; xs=np.arange(-2e-15,sep+2e-15,d); L=2.2e-15
        ys=np.arange(-L,L,d); zs=np.arange(-L,L,d); E=0.0
        for z in zs:
            Y,X=np.meshgrid(ys,xs); P=np.column_stack([X.ravel(),Y.ravel(),np.full_like(X.ravel(),z)])
            core=(np.linalg.norm(P,axis=1)<rp)|(np.linalg.norm(P-np.array([sep,0,0]),axis=1)<rp)
            P=P[~core]
            Bp=sum(dip(P,posA[i],mA[i]) for i in range(10))
            Bn=sum(dip(P,pb[j],mB[j]) for j in range(11))
            E+=np.sum((Bp*Bn).sum(axis=1))/mu0*(d**3)
        yield res,E/MeV
print("验证 sep=1.989fm (0.04 vs 0.033fm 分辨率收敛)")
for sep in [1.90,1.989,2.00]:
    print(f"\nsep={sep:.3f} fm:")
    for res,E in E_int_at(sep*1e-15):
        print(f"  分辨率{res}fm: E_int={E:.4f} MeV, τ_b×|E|={abs(tau_b*E):.4f} MeV (vs2.2246={abs(tau_b*E)/E_target:.4f}×)")
