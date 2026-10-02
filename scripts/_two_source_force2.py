# -*- coding: utf-8 -*-
"""干净版：I(r) 直接重算；加相位退相干包络 e^(-r/d) 后看是否恢复指数尾"""
import numpy as np
c=3e8; f0=1.2799e23; lam=c/f0*1e15; k=2*np.pi/lam; d=lam/2.0
Rc=1.5
g=np.linspace(-Rc,Rc,101); X,Y,Z=np.meshgrid(g,g,g); dv=(g[1]-g[0])**3

def I(r,decoh=False):
    dA=np.sqrt((X+r/2)**2+Y**2+Z**2)+1e-12
    dB=np.sqrt((X-r/2)**2+Y**2+Z**2)+1e-12
    val=np.cos(k*(dA-dB))/(dA*dB)
    if decoh: val=val*np.exp(-r/d)
    return val.sum()*dv

rs=np.arange(0.15,2.01,0.05)
I_naive=np.array([I(r) for r in rs]); F_naive=-np.gradient(I_naive,rs)
I_decoh=np.array([I(r,True) for r in rs]); F_decoh=-np.gradient(I_decoh,rs)

def slope_seg(rs,F,r0,r1):
    m=(rs>=r0)&(rs<=r1); return np.polyfit(rs[m],np.log(np.abs(F[m])+1e-12),1)[0]

print("naive:   ln|F|斜率(0.4-1.6)=%.3f, 过零点=%d"%(slope_seg(rs,F_naive,0.4,1.6),int(((F_naive[:-1]*F_naive[1:])<0).sum())))
print("退相干:  ln|F|斜率(0.8-1.9)=%.3f, 期望-1/d=%.3f, 过零点=%d"%(
      slope_seg(rs,F_decoh,0.8,1.9),-1/d,int(((F_decoh[:-1]*F_decoh[1:])<0).sum())))
# 也看近区(0.4-1.0)
print("退相干近区(0.4-1.0)斜率=%.3f"%slope_seg(rs,F_decoh,0.4,1.0))

import json
json.dump({"r":rs.tolist(),"F_naive":F_naive.tolist(),"F_decoh":F_decoh.tolist(),
           "exp_env":np.exp(-rs/d).tolist(),"d":d},
          open(r"C:\Users\Administrator\Doubao\chats\2026-10-01\new-chat\_two_source_force2.json","w"),ensure_ascii=False)
