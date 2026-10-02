# -*- coding: utf-8 -*-
"""传播型退相干：ψ_i=(A/ρ)·e^(ikρ)·e^(-ρ/ℓc)，ℓc=相干长度≈d=λ/2
交叉项 ∝ e^{-(dA+dB)/ℓc}·cos(kΔ)/(dA·dB)。看 F=-dI/dr 是否恢复指数尾。"""
import numpy as np
c=3e8; f0=1.2799e23; lam=c/f0*1e15; k=2*np.pi/lam; d=lam/2.0
Rc=1.5
g=np.linspace(-Rc,Rc,101); X,Y,Z=np.meshgrid(g,g,g); dv=(g[1]-g[0])**3

def I(r,lc):
    dA=np.sqrt((X+r/2)**2+Y**2+Z**2)+1e-12
    dB=np.sqrt((X-r/2)**2+Y**2+Z**2)+1e-12
    return (np.cos(k*(dA-dB))*np.exp(-(dA+dB)/lc)/(dA*dB)).sum()*dv

rs=np.arange(0.15,2.01,0.05)
for lc in [d, 0.7*d, 1.3*d]:
    I_=np.array([I(r,lc) for r in rs]); F=-np.gradient(I_,rs)
    def sl(r0,r1):
        m=(rs>=r0)&(rs<=r1); return np.polyfit(rs[m],np.log(np.abs(F[m])+1e-12),1)[0]
    z=int(((F[:-1]*F[1:])<0).sum())
    print("ℓc=%.3f fm: ln|F|斜率(0.8-1.9)=%.3f (期望-1/ℓc=%.3f), 过零点=%d"%(lc,sl(0.8,1.9),-1/lc,z))
