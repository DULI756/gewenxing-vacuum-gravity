# -*- coding: utf-8 -*-
"""磁重联ΔB口径对比：偶极远场(中点) vs 接触面(核内场区) 2026-10-10"""
import numpy as np
mu0 = 1.25663706212e-6
muN = 5.050783699e-27
MeV = 1.602176634e-13
E_target = 2.2246*MeV
rp = 0.84e-15
R0,hh,axH = 0.4238,0.2520,0.6758
sq=np.sqrt(2)
J17 = np.array([
 (R0,0,-hh),(0,R0,-hh),(-R0,0,-hh),(0,-R0,-hh),
 (R0/sq,R0/sq,hh),(-R0/sq,R0/sq,hh),(-R0/sq,-R0/sq,hh),(R0/sq,-R0/sq,hh),
 (0,0,axH),(0,0,-axH)], dtype=float)
def mag_field(pos,m,P):
    rv=P-pos; r=np.linalg.norm(rv)
    if r<1e-20: return np.zeros(3)
    rh=rv/r
    return (mu0/(4*np.pi*r**3))*(3*np.dot(m,rh)*rh-m)
def lock(n,axis,tot):
    return np.array([tot/n*np.array(axis,float) for _ in range(n)])
posA=J17*rp
posB=np.vstack([J17*rp,np.array([0.,0,0])])
mup_in=115.9*muN; mun_in=115.9*muN
mA=lock(10,[0,1,0],mup_in); mB=lock(11,[0,1,0],-mun_in)

print("口径A 偶极远场(中点x=sep/2): ΔB~10^11-10^12T, 释放~10^-3MeV ✗")
print("口径B 接触面(x=质子表面, 距中子sep-rp): ΔB=?")
sep=1.9e-15
pb=posB.copy(); pb[:,0]+=sep
for P,xlab in [([rp,0,0],f"质子表面x={rp*1e15:.2f}fm"),
               ([rp+0.1e-15,0,0],"接触带内侧x=r_p+0.1fm"),
               ([sep/2,0,0],f"中点x={sep/2*1e15:.2f}fm")]:
    P=np.array(P)
    Bp=np.zeros(3);Bn=np.zeros(3)
    for i in range(10): Bp+=mag_field(posA[i],mA[i],P)
    for j in range(11): Bn+=mag_field(pb[j],mB[j],P)
    Bp_mag=np.linalg.norm(Bp); Bn_mag=np.linalg.norm(Bn)
    dB=abs(Bp[1]+Bn[1])            # y向净反平行
    dB_anti=abs(Bp_mag-Bn_mag)     # 反平行幅度差
    print(f"  {xlab}: |Bp|={Bp_mag:.2e}, |Bn|={Bn_mag:.2e}, y净反平行dB={dB:.2e}, 幅度差dB_anti={dB_anti:.2e}")

# 用核内场口径：ΔB取接触带实际场强，扫描需要的V
print("\n口径C 核内场口径(接触带场强~核内B0): 需多小V才2.2MeV?")
B0=3.901e14
for dB in [B0, 2e14, 1e14, 5e13]:
    V=E_target/(2*dB**2/mu0)
    r=(3*V/(4*np.pi))**(1/3)
    print(f"  ΔB={dB:.2e}T → V={V:.3e}m³ → 等效半径{r*1e15:.3f}fm")
print(f"  核内场自能密度 w=B0²/2μ0 = {B0**2/(2*mu0):.3e} J/m³")
