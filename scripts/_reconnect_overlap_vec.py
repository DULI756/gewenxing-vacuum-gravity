# -*- coding: utf-8 -*-
"""氘核重叠场能差 向量化收敛测试 (2026-10-11 回到主线第一步)
E_int = ∫(B_p·B_n)/μ0 dV  反平行, 核外重叠区
目的: 验证 −5.60MeV(0.06fm) 是否数值收敛, 用 Magpylib Dipole 交叉核对
"""
import numpy as np
import magpylib as magpy
mu0 = 1.25663706212e-6
muN = 5.050783699e-27
MeV = 1.602176634e-13
E_target = 2.2246
rp = 0.84e-15
sep = 1.9e-15
R0,hh,axH = 0.4238,0.2520,0.6758
sq=np.sqrt(2)
J17 = np.array([
 (R0,0,-hh),(0,R0,-hh),(-R0,0,-hh),(0,-R0,-hh),
 (R0/sq,R0/sq,hh),(-R0/sq,R0/sq,hh),(-R0/sq,-R0/sq,hh),(R0/sq,-R0/sq,hh),
 (0,0,axH),(0,0,-axH)], dtype=float)
posA = J17*rp
posB = np.vstack([J17*rp, np.array([0.,0,0])])
mup = 115.9*muN
mA = np.tile([0,mup/10,0],(10,1))
mB = np.tile([0,-mup/11,0],(11,1))
pb = posB.copy(); pb[:,0]+=sep

def dipole_B_vec(P):  # P:(N,3) → (N,3) 手写, 全源叠加
    Bp=np.zeros_like(P); Bn=np.zeros_like(P)
    for i in range(10):
        rv=P-posA[i]; r=np.linalg.norm(rv,axis=1); r=np.maximum(r,1e-30)
        rh=rv/r[:,None]; md=np.einsum('ij,j->i',rh,mA[i])
        Bp+=(mu0/(4*np.pi*r[:,None]**3))*(3*md[:,None]*rh-mA[i][None,:])
    for j in range(11):
        rv=P-pb[j]; r=np.linalg.norm(rv,axis=1); r=np.maximum(r,1e-30)
        rh=rv/r[:,None]; md=np.einsum('ij,j->i',rh,mB[j])
        Bn+=(mu0/(4*np.pi*r[:,None]**3))*(3*md[:,None]*rh-mB[j][None,:])
    return Bp,Bn

def B_all_mag(P):  # Magpylib Dipole 对照
    dipA=[magpy.misc.Dipole(moment=mA[i],position=posA[i]) for i in range(10)]
    dipB=[magpy.misc.Dipole(moment=mB[j],position=pb[j]) for j in range(11)]
    BA=magpy.getB(dipA,P); BB=magpy.getB(dipB,P)
    return BA.sum(axis=0), BB.sum(axis=0)

print("分辨率收敛测试: E_int = ∫Bp·Bn/μ0 dV (反平行, 核外)")
for res in [0.08,0.06,0.05,0.04,0.033]:
    d=res*1e-15
    xs=np.arange(-2e-15,sep+2e-15,d); L=2.2e-15
    ys=np.arange(-L,L,d); zs=np.arange(-L,L,d)
    E=0.0; cnt=0
    for z in zs:
        # xy 平面网格 (向量化)
        Y,X=np.meshgrid(ys,xs); Z=np.full_like(X,z)
        P=np.column_stack([X.ravel(),Y.ravel(),Z.ravel()])
        core=(np.linalg.norm(P,axis=1)<rp)|(np.linalg.norm(P-np.array([sep,0,0]),axis=1)<rp)
        P=P[~core]
        Bp,Bn=dipole_B_vec(P)
        E+=np.sum((Bp*Bn).sum(axis=1))/mu0*(d**3)
    print(f"  分辨率{res:.3f}fm: E_int = {E/MeV:.4f} MeV  ({(E/MeV)/E_target:.3f}×目标)")
print("\n(负=反平行释放)")

# Magpylib Dipole 对照(0.05fm一次)
res=0.05; d=res*1e-15
xs=np.arange(-2e-15,sep+2e-15,d); L=2.2e-15
ys=np.arange(-L,L,d); zs=np.arange(-L,L,d)
Em=0.0
for z in zs:
    Y,X=np.meshgrid(ys,xs); Z=np.full_like(X,z)
    P=np.column_stack([X.ravel(),Y.ravel(),Z.ravel()])
    core=(np.linalg.norm(P,axis=1)<rp)|(np.linalg.norm(P-np.array([sep,0,0]),axis=1)<rp)
    P=P[~core]
    BA,BB=B_all_mag(P)
    Em+=np.sum((BA*BB).sum(axis=1))/mu0*(d**3)
print(f"\nMagpylib Dipole 对照 (0.05fm): E_int = {Em/MeV:.4f} MeV")
print("手写与Magpylib应一致(相对差~1e-9, 前面已验Dipole公式)")
