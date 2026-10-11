# -*- coding: utf-8 -*-
"""
引入高频动态：脉冲占空比修正磁自能场重叠交叉项
2026-10-10
波源=脉冲型磁场源(f0=1.60353e23Hz, 能量层τ_b=0.5/间歇层τ_i=0.5)
时间平均场能 = τ_b × 峰值场能(能量层活跃, 间歇层零压)
E_int_pulse = τ_b × E_int_static(交叉项重叠场能差)
"""
# 静态交叉项(0.06fm分辨率实测, 见_reconnect_overlap_energy.py)
E_static = -5.5953   # MeV, 反平行释放(负=降低)
E_target = 2.2246    # MeV 氘核结合能实验值
tau_b = 0.5          # 能量层占空比(对称, 拍板值)

print("========== 高频动态占空比修正 ==========")
print(f"静态交叉项 E_int = {E_static} MeV (反平行, 0.06fm)")
print(f"时间平均 E_int_pulse = τ_b × E_int = {tau_b}×({E_static}) = {tau_b*E_static:.4f} MeV")
print(f"|E_int_pulse| = {abs(tau_b*E_static):.4f} MeV  vs 2.2246 = {abs(tau_b*E_static)/E_target:.3f}×")
print(f"剩余差: {abs(tau_b*E_static)-E_target:.4f} MeV ({abs(tau_b*E_static)/E_target-1:.1%})")

# 要精确闭合需要什么
print("\n========== 精确闭合反解 ==========")
print(f"若 τ_b=0.5, 需源磁矩系数 = sqrt({E_target}/|{tau_b*E_static}|) = sqrt({E_target/abs(tau_b*E_static):.4f}) = {(E_target/abs(tau_b*E_static))**0.5:.4f}")
print(f"若源磁矩不变, 需 τ_b = {E_target/abs(E_static):.4f}")
print(f"τ_b=0.397(非对称) 或 源磁矩×0.796 (115.9→92.3μN)")

print("\n========== 高频动态物理 ==========")
print("① 结合能释放=每秒f0次脉冲重叠, 时间平均=τ_b×峰值")
print("② 两核子须相干锁定(同相)才有效重叠, 间歇层零压不贡献")
print("③ 占空比0.5把静态−5.6→−2.8MeV, 距2.2246差26%")
print("④ 剩余差来自: 源磁矩口径(115.9μN)/sep/收敛/相干细节")
