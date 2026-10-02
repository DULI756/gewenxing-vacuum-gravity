# -*- coding: utf-8 -*-
"""10源整体合成场包络检验：|ψ(ρ)|²=<|Σ_i e^{ik|x-ri|}/|x-ri||²>_角平均，去掉1/ρ²球面扩散，
看剩余包络 E(ρ)=<|ψ|²>·ρ² 是否指数(斜率-1/d)。"""
import numpy as np
np.random.seed(11)
c=3e8; f0=1.2799e23; lam=c/f0*1e15; k=2*np.pi/lam; d=lam/2.0
R0,h,axH=0.8757,0.5838,1.3427
pos=[]
for a in [0,90,180,270]:   r=a*np.pi/180; pos.append((R0*np.cos(r),R0*np.sin(r), h))
for a in [45,135,225,315]: r=a*np.pi/180; pos.append((R0*np.cos(r),R0*np.sin(r),-h))
pos.append((0,0,axH)); pos.append((0,0,-axH))
pos=np.array(pos); N=10

rhos=np.arange(1.6,4.01,0.15)
nd=4000
out=[]
for rho in rhos:
    u=np.random.randn(nd,3); u/=np.linalg.norm(u,axis=1,keepdims=True)
    rv=rho*u
    dd=np.linalg.norm(rv[:,None,:]-pos[None,:,:],axis=2)   # (nd,10)
    psi=(np.exp(1j*k*dd)/dd).sum(axis=1)                   # (nd,) 合成场
    I2=np.abs(psi)**2
    env=np.mean(I2)*rho*rho                               # 去掉1/ρ²后的包络
    out.append((rho,env))
    print("ρ=%.2f  E=%.4f  lnE=%.3f"%(rho,env,np.log(env)))

rs=np.array([o[0] for o in out]); E=np.array([o[1] for o in out])
m=(rs>=1.8)&(rs<=3.6); sl=np.polyfit(rs[m],np.log(E[m]),1)[0]
print("\n[判据] ln E(1.8-3.6fm) 斜率=%.3f, 期望 -1/d=%.3f"%(sl,-1/d))
print("→ 若≈%.3f 则10源整体合成场包络确为 e^(-r/d)"%(-1/d))
import json
json.dump({"r":rs.tolist(),"E":E.tolist(),"slope":sl,"expected":-1/d},open(r"C:\Users\Administrator\Doubao\chats\2026-10-01\new-chat\_cluster_field.json","w"))
