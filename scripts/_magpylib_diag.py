# -*- coding: utf-8 -*-
"""Magpylib 大尺寸远场诊断: 确认getB单位 + Sphere外场=点偶极"""
import numpy as np
import magpylib as magpy
mu0 = 1.25663706212e-6
muN = 5.050783699e-27
def dipole_B(pos, m, P):
    rv = P-pos; r = np.linalg.norm(rv)
    if r < 1e-30: return np.zeros(3)
    rh = rv/r
    return (mu0/(4*np.pi*r**3))*(3*np.dot(m,rh)*rh-m)

axis = np.array([0.3,0.8,0.5]); axis/=np.linalg.norm(axis)
m_eff = axis*(115.9*muN)
for D,R in [(1e-3,1e-1),(1e-4,1e-2)]:
    vol=(4/3)*np.pi*(D/2)**3
    mag=axis*(m_eff/vol)
    sph=magpy.magnet.Sphere(magnetization=mag, diameter=D)
    obs=np.array([[R*0.3,R*0.6,R*0.8]])
    Bm=sph.getB(obs)[0]
    Ba=dipole_B(np.array([0,0,0.]),m_eff,obs[0])
    # 尝试两种单位: T 与 mT
    for lab,sc in [("T",1.0),("mT→T",1e-3)]:
        rel=np.linalg.norm(Bm*sc-Ba)/np.linalg.norm(Ba)
        print(f"D={D:.0e} R={R:.0e}: getB假设{lab} 相对差={rel:.3e}")
    print(f"   Bm={Bm}, Ba={Ba}")
