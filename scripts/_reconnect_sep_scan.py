# -*- coding: utf-8 -*-
"""氘核重叠场能差 sep 灵敏度扫描 (2026-10-11 回到主线)
sep=两核子质心距. 实验: 氘核质子-中子距离~1.9-2.0fm(氘核rms 2.14fm).
看 τ_b×|E_int| 能否在 sep 实验区间达到 2.2246MeV.
其余口径固定: 源磁矩115.9μN(全同向均分), τ_b=0.5
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
    res=0.04; d=res*1e-15
    xs=np.arange(-2e-15,sep+2e-15,d); L=2.2e-15
    ys=np.arange(-L,L,d); zs=np.arange(-L,L,d)
    E=0.0
    for z in zs:
        Y,X=np.meshgrid(ys,xs); P=np.column_stack([X.ravel(),Y.ravel(),np.full_like(X.ravel(),z)])
        core=(np.linalg.norm(P,axis=1)<rp)|(np.linalg.norm(P-np.array([sep,0,0]),axis=1)<rp)
        P=P[~core]
        Bp=sum(dip(P,posA[i],mA[i]) for i in range(10))
        Bn=sum(dip(P,pb[j],mB[j]) for j in range(11))
        E+=np.sum((Bp*Bn).sum(axis=1))/mu0*(d**3)
    return E/MeV

print("sep 扫描 (τ_b=0.5): 目标 2.2246 MeV")
print("sep(fm) | E_int(MeV) | τ_b×|E_int| | vs目标 | 需闭合的sep反解")
for sep_f in [1.7,1.8,1.9,2.0,2.1]:
    E=E_int_at(sep_f*1e-15)
    p=abs(tau_b*E)
    print(f"{sep_f:5.1f}  | {E:8.3f}    | {p:8.3f}     | {p/E_target:5.3f}×")
# 反解: 找 sep 使 τ_b×|E_int|=2.2246
from scipy.optimize import brentq
def f(sepm): return abs(tau_b*E_int_at(sepm*1e-15))-E_target
try:
    sep_sol=brentq(f,1.6,2.6)
    print(f"\n精确闭合 sep ≈ {sep_sol:.3f} fm (实验两核子距离~1.9-2.0fm)")
except Exception as ex:
    print("反解区间未含零点:",ex)
