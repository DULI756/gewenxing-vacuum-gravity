# -*- coding: utf-8 -*-
"""
两核子发散磁自能场重叠场能差第一性积分
2026-10-10
总场自能差 = ∫|B_p+B_n|^2/2μ0 dV − (∫B_p^2/2μ0 + ∫B_n^2/2μ0) = ∫(B_p·B_n)/μ0 dV
反平行取向(侧向): B_p·B_n<0 → 场能降低 → 释放=结合能
第一性源场: 质子10源J17 + 中子11源(J17+中心), 核外偶极场, sep=1.9fm(氘核)
源磁矩口径: 磁自能导出(内部源) 质子10源各+11.59μN, 中子11源各-10.536μN
"""
import numpy as np
mu0 = 1.25663706212e-6
muN = 5.050783699e-27
MeV = 1.602176634e-13
E_target = 2.2246*MeV
rp = 0.84e-15
sep = 1.9e-15
R0,hh,axH = 0.4238,0.2520,0.6758
sq=np.sqrt(2)
J17 = np.array([
 (R0,0,-hh),(0,R0,-hh),(-R0,0,-hh),(0,-R0,-hh),
 (R0/sq,R0/sq,hh),(-R0/sq,R0/sq,hh),(-R0/sq,-R0/sq,hh),(R0/sq,-R0/sq,hh),
 (0,0,axH),(0,0,-axH)], dtype=float)
def dipole_B(pos,m,P):
    rv=P-pos; r=np.linalg.norm(rv)
    if r<1e-30: return np.zeros(3)
    rh=rv/r
    return (mu0/(4*np.pi*r**3))*(3*np.dot(m,rh)*rh-m)
posA=J17*rp
posB=np.vstack([J17*rp,np.array([0.,0,0])])
mup=115.9*muN
mA=np.array([mup/10*np.array([0,1,0],float) for _ in range(10)])
mB=np.array([-mup/11*np.array([0,1,0],float) for _ in range(11)])
pb=posB.copy(); pb[:,0]+=sep

# 核外重叠区体积积分 (跳过两核子核内)
def B_all(P):
    Bp=np.zeros(3);Bn=np.zeros(3)
    for i in range(10): Bp+=dipole_B(posA[i],mA[i],P)
    for j in range(11): Bn+=dipole_B(pb[j],mB[j],P)
    return Bp,Bn
def in_core(P):
    return np.linalg.norm(P-np.array([0,0,0]))<rp or np.linalg.norm(P-np.array([sep,0,0]))<rp

xmin,xmax=-2e-15, sep+2e-15
L=2.2e-15
for res in [0.06,0.04]:
    d=res*1e-15
    xs=np.arange(xmin,xmax,d); ys=np.arange(-L,L,d); zs=np.arange(-L,L,d)
    E=0.0
    for x in xs:
        for y in ys:
            for z in zs:
                P=np.array([x,y,z])
                if in_core(P): continue
                Bp,Bn=B_all(P)
                E+=(Bp@Bn)/mu0*(d**3)
    print(f"分辨率{res}fm: E_int=∫Bp·Bn/μ0 dV = {E/MeV:.4f} MeV  vs 2.2246 = {E/E_target:.3f}×")

print("\n========== 结论 ==========")
print("反平行→Bp·Bn<0→E_int负(释放)。若|E_int|≈2.2246MeV即第一性闭合。")
print("注意: 偶极场核外, 源处截断(r<rp跳过核内)。源磁矩口径为磁自能导出值。")
