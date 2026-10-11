# -*- coding: utf-8 -*-
"""氦核第一版量级检查: 正四面体6对, 每对单偶极反平行重叠, τ_b=0.5
问: 使 τ_b×Σ6对|E_int(s)| = 氦核结合能28.296MeV 的核子间距s是否落在α粒子合理范围
α: rms charge radius 1.68fm; 核子间距实验/理论~1.4-1.7fm(紧密)
"""
import numpy as np
mu0=1.25663706212e-6; muN=5.050783699e-27; MeV=1.602176634e-13
rp=0.84e-15; tau_b=0.5
E_He4=28.296; E_D=2.2246

def dip(P,pos,m):
    rv=P-pos; r=np.maximum(np.linalg.norm(rv,axis=1),1e-30); rh=rv/r[:,None]
    md=np.einsum('ij,j->i',rh,m)
    return (mu0/(4*np.pi*r[:,None]**3))*(3*md[:,None]*rh-m[None,:])
def E_pair(s):  # 单偶极反平行, 两球心距s, 跳过核内
    d=0.05*1e-15; xs=np.arange(-2e-15,s+2e-15,d); L=2.2e-15
    ys=np.arange(-L,L,d); zs=np.arange(-L,L,d); E=0.0; m=115.9*muN
    for z in zs:
        Y,X=np.meshgrid(ys,xs); P=np.column_stack([X.ravel(),Y.ravel(),np.full_like(X.ravel(),z)])
        core=(np.linalg.norm(P,axis=1)<rp)|(np.linalg.norm(P-np.array([s,0,0]),axis=1)<rp)
        P=P[~core]
        Bp=dip(P,np.array([0.,0,0]),np.array([0.,m,0]))
        Bn=dip(P,np.array([s,0.,0]),np.array([0.,-m,0]))
        E+=np.sum((Bp*Bn).sum(axis=1))/mu0*(d**3)
    return E/MeV

print("氦核结合能目标 28.296 MeV (4核子/6对, τ_b=0.5, 单偶极反平行)")
print("简化: 6对独立求和 (忽略多体场叠加, 量级检查)")
for s in [1.3,1.4,1.5,1.6,1.7,1.8,1.9]:
    e=E_pair(s*1e-15)
    E6=6*abs(e)*tau_b
    print(f"  s={s:.1f}fm: 单对|E|={abs(e):6.2f} → 6对×τ_b={E6:7.1f} MeV (vs28.3={E6/E_He4:.2f}×)")
print("\n说明: 6对反平行为最大释放理想化; 真实Σm=0取向会部分抵消→需更小s。")
print("氘核单对 sep=1.989 → |E_int|=4.67(单偶极口径, 前面实测)")
