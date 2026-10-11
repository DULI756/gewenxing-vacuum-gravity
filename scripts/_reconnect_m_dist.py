# -*- coding: utf-8 -*-
"""
磁矩随距离衰减(核心公式一致)对重叠交叉项的影响
2026-10-10
A直接版:  m_eff(r)=m0·(d/r)·e^(-r/d)
B表面归一: m_eff(r)=m0·(r_p/r)·e^(-(r-r_p)/d), 表面=m0
E_int = ∫(B_p·B_n)/μ0 dV, B∝m_eff(|P-源|)/r³
"""
import numpy as np
mu0 = 1.25663706212e-6
muN = 5.050783699e-27
MeV = 1.602176634e-13
E_target = 2.2246*MeV
rp = 0.84e-15
d  = 0.935e-15        # c/2f0 外层场区
sep = 1.9e-15
R0,hh,axH = 0.4238,0.2520,0.6758
sq=np.sqrt(2)
J17 = np.array([
 (R0,0,-hh),(0,R0,-hh),(-R0,0,-hh),(0,-R0,-hh),
 (R0/sq,R0/sq,hh),(-R0/sq,R0/sq,hh),(-R0/sq,-R0/sq,hh),(R0/sq,-R0/sq,hh),
 (0,0,axH),(0,0,-axH)], dtype=float)
posA=J17*rp
posB=np.vstack([J17*rp,np.array([0.,0,0])])
m0=115.9*muN
mA0=m0/10*np.array([0,1,0],float)
mB0=-m0/11*np.array([0,1,0],float)
pb=posB.copy(); pb[:,0]+=sep

def dipole_B(pos,m,P):
    rv=P-pos; r=np.linalg.norm(rv)
    if r<1e-30: return np.zeros(3)
    rh=rv/r
    return (mu0/(4*np.pi*r**3))*(3*np.dot(m,rh)*rh-m)

def gA(r):  # 直接核心公式 m0(d/r)e^(-r/d), 相对源
    if r<1e-20: return 0.0
    return (d/r)*np.exp(-r/d)
def gB(r):  # 表面归一化
    if r<1e-20: return 0.0
    return (rp/r)*np.exp(-(r-rp)/d)

def E_int(gmode):
    E=0.0
    res=0.06e-15
    xmin,xmax=-2e-15, sep+2e-15
    L=2.2e-15
    xs=np.arange(xmin,xmax,res); ys=np.arange(-L,L,res); zs=np.arange(-L,L,res)
    n=0
    for x in xs:
        for y in ys:
            for z in zs:
                P=np.array([x,y,z])
                if np.linalg.norm(P)<rp or np.linalg.norm(P-np.array([sep,0,0]))<rp: continue
                Bp=np.zeros(3);Bn=np.zeros(3)
                for i in range(10):
                    rr=np.linalg.norm(P-posA[i])
                    m=mA0*(gA(rr) if gmode=='A' else gB(rr))
                    Bp+=dipole_B(posA[i],m,P)
                for j in range(11):
                    rr=np.linalg.norm(P-pb[j])
                    m=mB0*(gA(rr) if gmode=='A' else gB(rr))
                    Bn+=dipole_B(pb[j],m,P)
                E+=(Bp@Bn)/mu0*(res**3)
                n+=1
    return E/MeV,n

for gm in ['A','B']:
    E,n = E_int(gm)
    print(f"磁矩衰减模式{gm}: E_int={E:+.4f} MeV, |E|={abs(E):.4f} vs 2.2246={abs(E)/E_target:.3f}×, 网格{n}")
