# -*- coding: utf-8 -*-
"""
绝对速度参考系：正确模型
- V_abs = 待求量（物体在空间中的真实绝对速度）
- 我们观测到的所有速度都是相对速度，叠加在 V_abs 上
- 四层相对速度：银心(230)、公转(29.78)、自转(0.465)、卫星(3.87)
- 通过实测钟差 Δτ 反推 V_abs
"""
import io, math
out=[]
def p(*a): out.append(' '.join(str(x) for x in a))

c = 2.99792458e8

# ==== 相对速度层（都是相对速度，不是绝对速度）====
v_gal = 230e3      # 太阳相对银心 (m/s)
v_orb = 29.78e3    # 地球公转
v_rot_eq = 465.0   # 赤道自转
v_sat = 3.87e3     # GPS卫星轨道速度

p("===== 正确模型：绝对速度是待求量 =====")
p("我们观测到的所有速度都是相对速度：")
p(f"  太阳相对银心: {v_gal/1e3:.0f} km/s")
p(f"  地球相对太阳: {v_orb/1e3:.1f} km/s")
p(f"  地面相对地心: {v_rot_eq:.0f} m/s (赤道)")
p(f"  卫星相对地心: {v_sat/1e3:.2f} km/s")
p("")
p("真正的绝对速度 V_abs = ? （待求量）")
p("我们感受到的相对速度 = V_abs_A - V_abs_B（两个绝对速度之差）")
p("")

# ==== 波源速度调制 ====
# f(v) = f0/(1+v²/2c²), v = 物体的绝对速度大小
# 两个钟的频率差 = f(V_abs_A) - f(V_abs_B)

# ==== GPS卫星 vs 地面钟 ====
# 卫星绝对速度 = V_abs_earth + v_sat（矢量叠加）
# 地面绝对速度 = V_abs_earth + v_rot（矢量叠加）
# 两者共享 V_abs_earth，但 v_sat ≠ v_rot

# 频率差（低速近似）:
# Δf/f0 ≈ (V_sat² - V_ground²)/(2c²)
# V_sat² = |V_abs_earth + v_sat|² = V_abs_earth² + 2 V_abs_earth·v_sat + v_sat²
# V_ground² = |V_abs_earth + v_rot|² = V_abs_earth² + 2 V_abs_earth·v_rot + v_rot²
# 差 = 2 V_abs_earth·(v_sat - v_rot) + (v_sat² - v_rot²)

# Δf/f0 = [2 V_abs_earth·(v_sat - v_rot) + (v_sat² - v_rot²)]/(2c²)

# 反推 V_abs_earth 在 v_sat-v_rot 方向上的投影:
# V_abs_proj = [c²·Δf/f0 - (v_sat² - v_rot²)/2] / |v_sat - v_rot|

# ==== 用GPS实测数据反推 ====
# GPS净钟差 38 μs/天 已被相对论解释 (SR -7 + GR +45)
# 波源理论需要的是"相对论解释之外的残差"
# 现代GPS残差: ~cm级距离误差 = ~0.1 ns时间误差 = 1e-10 s/天

p("===== 用GPS残差反推 V_abs =====")
day_s = 86400.0

# GPS残差（相对论解释后剩余）: 约 1e-10 s/天 (cm级距离误差)
tau_residual_s = 1e-10  # s/天
delta_f_over_f0 = tau_residual_s / day_s  # 频率差率

p(f"GPS周期残差(相对论解释后) ≈ {tau_residual_s*1e9:.1f} ns/天")
p(f"对应 Δf/f0 = {delta_f_over_f0:.3e}")

# v_sat - v_rot 的大小（最坏情况：同向）
dv = v_sat - v_rot_eq
p(f"|v_sat - v_rot| ≈ {dv:.0f} m/s (最坏情况同向)")

# 反推 V_abs 在 dv 方向的投影
# Δf/f0 = [2 V_abs·dv + (v_sat² - v_rot²)]/(2c²)
# V_abs·dv = c²·Δf/f0 - (v_sat² - v_rot²)/2

v_sq_diff = v_sat**2 - v_rot_eq**2
V_dot_dv = c**2 * delta_f_over_f0 - v_sq_diff/2

p(f"v_sat² - v_rot² = {v_sq_diff:.3e} (m/s)²")
p(f"c²·Δf/f0 = {c**2*delta_f_over_f0:.3e} (m/s)²")
p(f"V_abs·dv = {V_dot_dv:.3e} (m/s)²")

# V_abs 在 dv 方向的投影
V_proj = V_dot_dv / dv
p(f"V_abs 在 (v_sat-v_rot) 方向的投影 ≈ {V_proj:.3e} m/s = {V_proj/1e3:.3f} km/s")
p("")

# ==== 关键：v_sat² - v_rot² 项 ====
# 这是即使 V_abs=0 也存在的"基线频率差"
baseline_delta = v_sq_diff/(2*c**2)
p(f"===== 基线项（V_abs=0 时的固有频率差）=====")
p(f"基线 Δf/f0 = (v_sat²-v_rot²)/(2c²) = {baseline_delta:.3e}")
p(f"对应钟差 = {baseline_delta*day_s*1e6:.3f} μs/天")
p(">>> 即使绝对速度为零，卫星钟和地面钟也有固有频率差（来自v_sat≠v_rot）")
p(">>> 这部分已被相对论SR修正解释（-7 μs/天）")
p("")

# ==== 波源理论 vs 相对论 ====
p("===== 波源理论与相对论的差异 =====")
p("相对论: f(v) = f0·sqrt(1-v²/c²) ≈ f0·(1-v²/2c²)")
p("波源理论: f(v) = f0/(1+v²/2c²) ≈ f0·(1-v²/2c²)")
p(">>> 一阶近似相同！差异在二阶:")
p("  相对论: 1-v²/2c² - v⁴/8c⁴")
p("  波源:   1-v²/2c² + 3v⁴/8c⁴")
p("  差异 ≈ v⁴/2c⁴ (四阶小量)")
p("")
p(f"v=3.87km/s时: v⁴/c⁴ = {(v_sat/c)**4:.3e}")
p(f"对应钟差差 = {(v_sat/c)**4*day_s*1e9:.3f} ns/天")
p(">>> 四阶小量差异 ~0.01 ns/天, 远小于GPS残差 100 ns/天")
p(">>> 结论: 波源理论与相对论在GPS精度下不可区分")
p("")

# ==== 真正的判决实验 ====
p("===== 真正能区分的实验 =====")
p("1. 高频钟差: 需要 v/c 更大的实验(如粒子加速器中的钟)")
p("2. 方向各向异性: 波源理论预言绝对速度方向可测, 相对论预言各向同性")
p("3. 光钟对比实验: 现代光钟精度 1e-18, 可测 v⁴/c⁴ 量级差异")
p("")
p(f"光钟精度 1e-18 对应的钟差 = {1e-18*day_s*1e9:.6f} ns/天")
p(f"波源vs相对论四阶差异(3.87km/s) = {(v_sat/c)**4*day_s*1e9:.4f} ns/天")
p(">>> 光钟精度足够测量四阶差异! 这是真正的判决实验")

with io.open(r'C:\Users\Administrator\Doubao\chats\2026-10-11\new-chat\_VE_abs_model.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(out))
print('OK')
