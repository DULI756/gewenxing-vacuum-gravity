# -*- coding: utf-8 -*-
"""两源相干积分 → 径向力尾：验证 e^(-r/d) 是否由几何/干涉自发产生
模型：两源 ±r/2 同频同相球面波 ψ=A/ρ·e^(ikρ)。
相互作用能 = 交叉相干项积分：I(r)=∫ cos(k·(|x-rA|-|x-rB|))/(|x-rA||x-rB|) dV（腔内 Rc）
力 F(r) = -dI/dr。
检验：若 F ~ e^(-r/d)，则 ln|F| 随 r 应为斜率 -1/d 的直线；否则不是指数。
"""
import numpy as np
np.random.seed(3)

c=3e8; f0=1.2799e23; lam=c/f0*1e15; k=2*np.pi/lam   # fm^-1
d=lam/2.0                                            # 负压层宽 = 脉冲半宽, fm
Rc=1.5                                               # 腔半径, fm
print(f"λ={lam:.4f} fm, k={k:.4f} fm^-1, d=λ/2={d:.4f} fm, Rc={Rc} fm")

g=np.linspace(-Rc,Rc,101)
X,Y,Z=np.meshgrid(g,g,g)
dv=(g[1]-g[0])**3

def I(r):
    dA=np.sqrt((X+r/2)**2+Y**2+Z**2)+1e-12
    dB=np.sqrt((X-r/2)**2+Y**2+Z**2)+1e-12
    return np.cos(k*(dA-dB))/(dA*dB)*dv

rs=np.arange(0.15,2.01,0.05)
Is=np.array([I(r).sum() for r in rs])
F=-np.gradient(Is,rs)                       # 力 ∝ -dI/dr
env=np.exp(-rs/d)                            # 目标指数尾(参考线)

# 判据：ln|F| 是否线性(斜率 -1/d)
mask=(rs>=0.4)&(rs<=1.6)
slope,poly=np.polyfit(rs[mask],np.log(np.abs(F[mask])+1e-12),1)
print("\n[判据] ln|F| 线性拟合(0.4-1.6fm): 斜率=%.3f, 期望-1/d=%.3f"%(slope,-1.0/d))
print("→ 若斜率≈%.3f 且拟合好则为指数尾；否则为振荡(非指数)"%(-1.0/d))

import json
out={"lambda_fm":lam,"k_fm":k,"d_fm":d,"Rc_fm":Rc,
     "r":rs.tolist(),"F":F.tolist(),"lnF":np.log(np.abs(F)+1e-12).tolist(),
     "exp_env":env.tolist(),
     "slope_fit":slope,"expected_slope":-1.0/d,
     "zero_crossings":int(((F[:-1]*F[1:])<0).sum())}
with open(r"C:\Users\Administrator\Doubao\chats\2026-10-01\new-chat\_two_source_force.json","w",encoding="utf-8") as f:
    json.dump(out,f,ensure_ascii=False)

# 摘要
print("\n过零点次数(振荡特征):",int(((F[:-1]*F[1:])<0).sum()))
print("F(0.4)=%.4f  F(0.8)=%.4f  F(1.2)=%.4f  F(1.6)=%.4f"%(F[np.argmin(abs(rs-0.4))],F[np.argmin(abs(rs-0.8))],F[np.argmin(abs(rs-1.2))],F[np.argmin(abs(rs-1.6))]))
