# -*- coding: utf-8 -*-
import numpy as np
mu=1.29333
mL, mS, mX, mO = 1115.683, 1192.642, 1314.86, 1672.45
meas=np.array([mL,mS,mX,mO]); names=['Λ','Σ','Ξ','Ω']

def Nt(s): return np.array([7+s, 7+s, 4+2*s, 3*s])      # 总源数
def Is(s): return np.array([0,1,0.5,0])                 # isospin
def Ns(s): return np.array([s, s, 2*s, 3*s])            # s型源数

def fit(p,s):
    X=np.column_stack([Ns(s)**p, Is(s)])
    y=meas-925.34-mu*Nt(s)
    coef,_,_,_=np.linalg.lstsq(X,y,rcond=None)
    predm=925.34+X@coef+mu*Nt(s)
    rms=np.sqrt(np.mean((predm-meas)**2))
    return coef,predm,rms

# 扫描 p 与 s
print("m_c = 925.34 + a·N_s^p + c·I ;  N_s=每个重子含s型源数")
for s in [4,5,6]:
    best=min((fit(p,s) for p in [0.5,0.8,1.0,1.2,1.5,2.0,2.5]),key=lambda z:z[2])
    print("s=%d: 最优p=... RMS=%.2f"%(s,best[2]))
print()
print("逐律逐点偏差 (MeV):")
for p in [1.0,2.0]:
    print(" p=%.1f:"%p, end=" ")
    for s in [5]:
        coef,predm,rms=fit(p,s)
        print("(a=%.3f,c=%.2f,RMS=%.2f) "%(coef[0],coef[1],rms)+" ".join("%+5.1f"%v for v in predm-meas))
# 最优全局
print()
best=min(( (rms,p,s,coef,predm) for p in [0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.4,2.8,3.0] for s in range(3,10) for coef,predm,rms in [fit(p,s)] ), key=lambda z:z[0])
rms,p,s,coef,predm=best
print("全局最优: p=%.2f s=%d a=%.4f c=%.2f RMS=%.2f MeV"%(p,s,coef[0],coef[1],rms))
print("逐点: "+" ".join("%s %+.2f"%(names[i],predm[i]-meas[i]) for i in range(4)))
