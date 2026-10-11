# -*- coding: utf-8 -*-
"""
磁重联成低能态: 释放磁能能否到 2.2 MeV  2026-10-08
磁重联释放磁能密度: w_rec = 2(ΔB)²/μ0  (ΔB=重联区反平行磁场分量)
总释放 = w_rec × V_rec(重联区体积)
核内磁场 B0≈3.9e14 T (从磁自能938MeV分布到 r_p³)
重叠区磁场(偶极, r=核子边界~0.95fm) ≈ 1.65e12 T
扫描 (ΔB, V_rec), 求能释放 2.2MeV=3.53e-13J 的组合
"""
import numpy as np
mu0=1.25663706212e-6
MeV=1.602176634e-13
E_target=2.2246*MeV
B0=3.9e14            # 核内磁场
B_overlap=1.65e12    # 重叠区磁场(偶极 r~0.95fm)

print("========== 磁重联释放能量 = w_rec × V_rec = 2(ΔB)²/μ0 × V ==========")
print(f"目标释放 2.2246 MeV = {E_target:.3e} J")
print(f"核内磁场 B0={B0:.2e} T; 重叠区磁场={B_overlap:.2e} T")
print(f"\n① 扫描 ΔB (给定重联区体积 V_rec=(0.5fm)³=1.25e-46m³):")
V=1.25e-46
print(f"{'ΔB[T]':>12} {'w_rec[J/m³]':>12} {'释放[MeV]':>12} {'vs2.2MeV':>9}")
for dB in [1.65e12,1e13,4.2e13,1e14,2e14,3.9e14]:
    w=2*dB**2/mu0
    rel=w*V
    print(f"{dB:12.3e} {w:12.3e} {rel/MeV:12.3f} {rel/E_target:9.2f}×")

print(f"\n② 反推: 给定 ΔB, 需多大 V_rec 才释放2.2MeV:")
for dB in [1.65e12,B0]:
    V_need=E_target/(2*dB**2/mu0)
    r=(3*V_need/(4*np.pi))**(1/3)
    print(f"  ΔB={dB:.2e}T → V_rec={V_need:.3e}m³ = 半径{r*1e15:.3f}fm 的球")

print(f"\n③ 真实重叠区尺度估计 (两核子接触带, 高~0.5fm, 厚~0.2fm):")
r1=0.84e-15; r2=0.84e-15; sep=1.9e-15
# 接触带: 两球重叠的环带体积(近似)
h=2*r1-sep  # 重叠深度
V_contact = np.pi*(h/2)**2*(3*(r1+r2)-h)/6  # 球冠重叠近似
V_contact = max(V_contact, 0)
print(f"  重叠深度h={h*1e15:.3f}fm, 接触体积≈{V_contact:.3e}m³")
if V_contact>0:
    w=2*B_overlap**2/mu0
    print(f"  释放(ΔB=重叠区场) = {w*V_contact/MeV:.3e} MeV")
    w0=2*B0**2/mu0
    print(f"  释放(ΔB=核内场) = {w0*V_contact/MeV:.3e} MeV")

print("\n========== 结论(诚实) ==========")
print("① 磁重联释放能=2(ΔB)²/μ0×V: 只要 ΔB(重联反平行分量)和V(重联体积)组合合适, 量级可达2.2MeV")
print("② 关键在ΔB: 若重联区ΔB~核内场量级(10^14T)且体积~fm³, 释放可达~MeV甚至更高")
print("③ 真实约束: ΔB取决于两核子在重叠区实际反平行场强; 体积取决于重联带尺度 → 需实测/更精确场模型定ΔB")
