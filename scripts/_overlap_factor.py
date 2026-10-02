# -*- coding: utf-8 -*-
"""几何重叠因子：半径 ρ → 对相干度 C_p(ρ) → 有效指数 p(ρ)
10 源 = 四方反棱柱 8 顶点（上下面 45° 扭曲）+ 上下轴 2 源，同频同相球面波。
E_coherent = a^2 · N · (1 + (N-1)·C_p),  C_p = <cos(k(|r-r_i|-|r-r_j|))>_{i≠j, 方向平均}
p(ρ) = d(lnE)/d(lnN) = 1 + N·C_p/(1+(N-1)·C_p)   (C_p 随 N 不变时)
"""
import numpy as np

np.random.seed(7)
c = 3.0e8
f0 = 1.2799e23            # Hz（v3 自洽解下调 ~20% 后的值）
lam = c/f0*1e15           # 波长, fm
k = 2*np.pi/lam           # 波数, 1/fm

# --- 10 源物理位置（动画常量 PXFM≈34.26 换算）---
R0, h, axH = 0.8757, 0.5838, 1.3427   # fm
deg = np.pi/180.0
pos = []
for a in [0,90,180,270]:   r=a*deg; pos.append((R0*np.cos(r), R0*np.sin(r),  h))
for a in [45,135,225,315]: r=a*deg; pos.append((R0*np.cos(r), R0*np.sin(r), -h))
pos.append((0,0, axH)); pos.append((0,0,-axH))
pos = np.array(pos); N = 10

def coherent_Cp(rho, ndir=12000):
    """在半径 rho 的球壳上、方向平均的对相干度（对角归一）。
    C_p∈[0,1]；=1 全相干(→p=2)，=0 全非相干(→p=1)。"""
    u = np.random.randn(ndir,3); u /= np.linalg.norm(u,axis=1,keepdims=True)
    rv = rho*u
    d  = np.linalg.norm(rv[:,None,:]-pos[None,:,:],axis=2)   # (ndir,10)
    phases = k*d
    diff   = phases[:,:,None]-phases[:,None,:]                # (ndir,10,10)
    cosd   = np.cos(diff)
    off    = ~np.eye(N,dtype=bool)
    return cosd[:,off].mean()

def eff_exp(Cp):
    return 1.0 + (N*Cp)/(1.0+(N-1)*Cp)

print(f"f0={f0:.4e} Hz,  λ={lam:.4f} fm,  k={k:.4f} fm^-1,  N={N}")
print("   ρ[fm]   C_p     p")
rows=[]
for rho in [0.0,0.15,0.3,0.5,0.67,0.84,1.0,1.3,1.6,2.0,2.6,3.2,4.0]:
    Cp_ = coherent_Cp(rho)
    p   = eff_exp(Cp_)
    rows.append((rho,Cp_,p))
    print(f"{rho:6.2f}  {Cp_:6.3f}  {p:6.3f}")

# 核心数值摘要
import json
out=[{"rho":r,"Cp":c,"p":p} for r,c,p in rows]
with open(r"C:\Users\Administrator\Doubao\chats\2026-10-01\new-chat\_overlap_data.json","w",encoding="utf-8") as f:
    json.dump(out,f)
print("\n内(ρ→0) p_max=%.3f ; 表面(ρ≈1fm) p=%.3f ; 外(ρ≥3fm) p→%.3f"%(rows[0][2], dict([(r,p) for r,_,p in rows])[1.0], dict([(r,p) for r,_,p in rows])[3.2]))
