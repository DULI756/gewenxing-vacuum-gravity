# -*- coding: utf-8 -*-
"""Magpylib 5.2.3 官方 Dipole 点偶极源 交叉校验 (L5.2) 单位已确认: getB→T, moment→A·m²"""
import numpy as np
import magpylib as magpy
mu0 = 1.25663706212e-6
muN = 5.050783699e-27
print("Magpylib", magpy.__version__, "| getB单位=T, moment单位=A·m²")

def dipole_B(pos, m, P):
    rv = P-pos; r = np.linalg.norm(rv)
    if r < 1e-30: return np.zeros(3)
    rh = rv/r
    return (mu0/(4*np.pi*r**3))*(3*np.dot(m,rh)*rh-m)

axis = np.array([0.3,0.8,0.5]); axis/=np.linalg.norm(axis)
m_eff = axis*(115.9*muN)
dip = magpy.misc.Dipole(moment=m_eff)
print("moment:", m_eff, "A·m² (方向", axis, ")")

pos=np.array([0.,0.,0.])
R=1e-6
obs=np.array([[R*0.3,R*0.6,R*0.8],[R*0.9,R*0.1,R*0.2],[R*-0.4,R*0.7,R*0.3],[R*0.0,R*0.0,R*1.0]])
Bm=dip.getB(obs)          # T (官方)
Ba=np.array([dipole_B(pos,m_eff,P) for P in obs])
for i in range(4):
    rel=np.linalg.norm(Bm[i]-Ba[i])/np.linalg.norm(Ba[i])
    print(f"点{i}: Magpylib={Bm[i]}T 手写={Ba[i]}T 相对差={rel:.2e}")
print("最大相对差:", max(np.linalg.norm(Bm[i]-Ba[i])/np.linalg.norm(Ba[i]) for i in range(4)))
