# -*- coding: utf-8 -*-
"""
绝对速度参考系：从速查表速度调制公式推导 V_E 反推公式 + 数值模拟
主线：f_v = f0/(1+v^2/2c^2)  -->  钟差率 DeltaTau/T  -->  反推 V_E
"""
import io, math
import sympy as sp

out = []
def p(*a): out.append(' '.join(str(x) for x in a))

# ============ 一、符号推导 ============
p("===== 一、符号推导：从速度调制导出 V_E =====")
f0, c, V, vt, vz = sp.symbols('f0 c V v_轨 v_自转', positive=True)
T, dtau = sp.symbols('T Δτ', positive=True)

# 速度调制（速查表）：f(v) = f0/(1+v^2/2c^2)
f_v = f0 / (1 + V**2/(2*c**2))
p("速度调制: f(v) = f0/(1+v²/2c²)")

# 两钟频率比
fa = f0/(1 + (V+vt)**2/(2*c**2))   # 绝对速度+轨道
fb = f0/(1 + (V+vz)**2/(2*c**2))   # 绝对速度+自转
ratio = sp.simplify(fa/fb)
p("频率比 fa/fb =", sp.simplify(ratio))

# 一阶近似: fa/fb ≈ 1 + [(V+vz)²-(V+vt)²]/2c²
approx = sp.expand(((V+vz)**2 - (V+vt)**2)/(2*c**2))
p("一阶: fa/fb ≈ 1 + [(V+vz)²-(V+vt)²]/2c² = 1 +", sp.expand(approx))

# 钟差率: Δτ/T = (fa-fb)/fa ≈ (fa/fb - 1) ≈ [(V+vz)²-(V+vt)²]/2c²
dtaur_T = sp.expand(((V+vz)**2 - (V+vt)**2)/(2*c**2))
p("Δτ/T = [(V+vz)²-(V+vt)²]/2c² =", sp.expand(dtaur_T))

# 展开: (V+vz)²-(V+vt)² = 2V(vz-vt) + (vz²-vt²)
diff = sp.expand((V+vz)**2 - (V+vt)**2)
p("展开: (V+vz)²-(V+vt)² =", diff)

# 解出 V:
# 2c²·Δτ/T = 2V(vz-vt) + (vz²-vt²)
# 2V(vz-vt) = 2c²·Δτ/T - (vz²-vt²)
V_expr = sp.solve(sp.Eq(2*c**2*dtau/T, 2*V*(vz-vt) + (vz**2-vt**2)), V)[0]
p("V_E =", sp.factor(V_expr))
p("速查表公式: V_E = [2c²/T·Δτ − (v轨²−v自转²)]/[2(v轨−v自转)]")
p(">>> 推导结果与速查表对比: 分母符号相反(vz-vt vs v轨-v自转), 取决于 v_自转/v_轨 定义次序; 结构完全一致")

# 用 v轨 > v自转 的正规化: 令 vt=v轨, vz=v自转 再解
V2 = sp.solve(sp.Eq(2*c**2*dtau/T, 2*V*(vt-vz) + (vt**2-vz**2)), V)[0]
p("若 Δτ 定义为 (f轨-f自转) 方向: V_E =", sp.factor(V2))
p(">>> 这正是速查表形式: V_E=[2c²Δτ/T−(v轨²−v自转²)]/[2(v轨−v自转)] ✓✓✓")

# ============ 二、数值模拟 ============
p("")
p("===== 二、数值模拟 =====")
cnum = 2.99792458e8
v_orb = 2.978e4      # 地球轨道速度 m/s
v_rot = 4.65e2       # 赤道自转线速度 m/s
day = 86400.0
year = 365.25*day

p(f"v轨 = {v_orb:.4e} m/s, v自转 = {v_rot:.4e} m/s, v轨-v自转 = {v_orb-v_rot:.4e} m/s")

# 1) 零钟差基线
V0 = -(v_orb**2 - v_rot**2)/(2*(v_orb-v_rot))
p(f"\n[1] Δτ=0 时: V_E = -(v轨²-v自转²)/2(v轨-v自转) = -(v轨+v自转)/2 = {V0:.1f} m/s = {V0/1e3:.2f} km/s")

# 2) 正向：给定 V_E，预言钟差率
for V_E_km in [0, 370, 369.82, 1000]:
    V_E = V_E_km*1e3
    dt_T = (2*V_E*(v_orb-v_rot) + (v_orb**2-v_rot**2))/(2*cnum**2)
    dt_day = dt_T*day
    p(f"\n[2] V_E={V_E_km} km/s: Δτ/T = {dt_T:.3e}  →  Δτ = {dt_day:.3e} s/天 = {dt_day*1e6:.3f} μs/天")
    if dt_day*1e6 > 0:
        p(f"    相对GPS净钟差38μs/天的倍数: {dt_day*1e6/38:.1f}×")

# 3) 反向：用真实数据反推 V_E
p("\n[3] 用真实钟差数据反推 V_E:")
# GPS 净钟差 +38 μs/day（相对论解释：-7 SR +45 GR）
dt_GPS = 38e-6
dt_T_GPS = dt_GPS/day
VE_gps = (2*cnum**2*dt_T_GPS - (v_orb**2-v_rot**2))/(2*(v_orb-v_rot))
p(f"GPS净钟差38μs/天（若全部归因绝对速度）: V_E = {VE_gps:.1f} m/s = {VE_gps/1e3:.2f} km/s")
# GPS 运动学项单独 -7 μs/day
dt_SR = -7e-6
dt_T_SR = dt_SR/day
VE_sr = (2*cnum**2*dt_T_SR - (v_orb**2-v_rot**2))/(2*(v_orb-v_rot))
p(f"GPS狭义相对论项-7μs/天（若归因绝对速度）: V_E = {VE_sr:.1f} m/s = {VE_sr/1e3:.2f} km/s")

# 4) 现代光钟精度可测性
p("\n[4] 可测性对比（光钟频率不确定度 ~1e-18）:")
p(f"    预言(370km/s) Δτ/T = {1.26e-7:.3e}  vs  光钟可测下限 ~{1e-18:.0e}")
p(f"    差距 {1.26e-7/1e-18:.0e} 倍 → 若绝对速度效应按此公式存在, 光钟早已观测到 ~1e-7 的季节性/方向性漂移")
p(f"    实测：光钟季节性漂移 ~1e-15 量级(引力势轨道偏心), 未观测到 1e-7 级 → 现有钟数据对绝对速度假设构成强约束")

with io.open(r'C:\Users\Administrator\Doubao\chats\2026-10-11\new-chat\_VE_derive_sim.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(out))
print('OK')
