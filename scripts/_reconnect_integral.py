# -*- coding: utf-8 -*-
"""
磁重联沿带积分闭合（第一性推进）：沿质子表面→中点扫ΔB(x)，电流片体积积分
2026-10-10
E_rec = ∫ 2·ΔB(x)²/μ0 · dV,  dV = 电流片截面积A × dx,  A=πw²(w=电流片半宽)
ΔB(x)=质子表面反平行场幅度差(4.45e13T@0.84fm) → 中点相消(3.9e11T@0.95fm)
21源相干锁定(侧向反平行)几何, 质子10源J17 + 中子11源(J17+中心), 内部磁矩115.9μN口径
"""
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
sep=1.9e-15
pb=posB.copy(); pb[:,0]+=sep

def dB_at_x(x):
    P=np.array([x,0,0],float)
    Bp=np.zeros(3);Bn=np.zeros(3)
    for i in range(10): Bp+=mag_field(posA[i],mA[i],P)
    for j in range(11): Bn+=mag_field(pb[j],mB[j],P)
    return abs(Bp[1]+Bn[1])   # 净反平行(y向)

print("========== 磁重联沿带积分：ΔB(x) + 电流片体积 ==========")
print(f"扫描 x: 质子表面 {rp*1e15:.2f}fm → 中点 {sep/2*1e15:.2f}fm")
xs = np.linspace(rp, sep/2, 101)
print(f"{'x[fm]':>7} {'ΔB(x)[T]':>12}")
for x in [rp, rp+0.05e-15, rp+0.1e-15, sep/2]:
    print(f"{x*1e15:7.3f} {dB_at_x(x):12.3e}")

print("\nE_rec = ∫ 2ΔB(x)²/μ0 · πw² dx  (电流片半宽w, 截面积πw²):")
for w in [0.2,0.3,0.5,0.7,1.0]:
    A = np.pi*(w*1e-15)**2
    vals=[2*dB_at_x(x)**2/mu0*A for x in xs]
    E = np.trapezoid(vals, xs)
    print(f"  w={w:.1f}fm (A={A:.2e}m²) → E_rec={E/MeV:.4f} MeV  vs 2.2246 = {E/E_target:.2f}×")

print("\n========== 结论 ==========")
print("① ΔB(x) 在质子表面取峰(4.45e13T)、沿轴衰减到中点相消(3.9e11T)")
print("② 释放集中在质子表面薄层；E_rec∝ΔB²·A·厚度")
print("③ 电流片半宽w决定截面，w越大E_rec越大")
