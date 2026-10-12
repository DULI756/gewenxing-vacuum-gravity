# -*- coding: utf-8 -*-
"""
绝对速度参考系：四层矢量合成模型
层1: 银河系本动 -> 已包含在CMB偶极中
层2: 太阳系绕银心 -> 已包含在CMB偶极中
层3: CMB偶极 v_cmb=369.82 km/s (l=264.0°, b=48.3°)
层4: 地球公转 v_orb=29.78 km/s (黄道面)
层5: 地球自转 v_rot=465 m/s (赤道面)
层6: GPS卫星 v_sat=3.87 km/s (倾角55°, 半长轴26560km)

关键: 波源速度调制 f(v)=f0/(1+v²/2c²), v=|绝对速度|
卫星钟 vs 地面钟的频率差 = 周期性调制(非恒定漂移)
"""
import io, math
import numpy as np

out=[]
def p(*a): out.append(' '.join(str(x) for x in a))

c = 2.99792458e8

# ==== 真实数据 ====
v_cmb_mag = 369.82e3    # m/s, CMB偶极 (Planck 2018)
l_cmb = math.radians(264.0)   # 银经
b_cmb = math.radians(48.3)    # 银纬
v_orb_mag = 29.78e3    # 地球公转
v_rot_eq = 465.0       # 赤道自转
v_sat_mag = 3.87e3     # GPS轨道速度
i_sat = math.radians(55)  # GPS轨道倾角

# ==== 坐标系统 ====
# 用球坐标转直角: x=东, y=北, z=天顶(本地地平)
# CMB方向在本地的投影需要考虑, 这里简化: 用黄道/赤道坐标
# 关键: 矢量点积 v_cmb · v_motion 决定效应大小

# CMB方向单位矢量 (黄道坐标近似: l=264°, b=48° 转黄道)
# 简化: 用赤道坐标近似 (l=264°, b=48° 接近 RA~11h, Dec~-7°)
# 这里用通用矢量分析, 不纠结精确坐标变换
# v_cmb 方向固定, v_orb/v_rot/v_sat 方向随时间旋转

p("===== 四层绝对速度矢量模型 =====")
p(f"层3: CMB偶极 v_cmb = {v_cmb_mag/1e3:.2f} km/s (l=264.0°, b=48.3°)")
p(f"层4: 地球公转 v_orb = {v_orb_mag/1e3:.2f} km/s (黄道面, 年周期)")
p(f"层5: 地球自转 v_rot = {v_rot_eq:.0f} m/s (赤道, 日周期)")
p(f"层6: GPS卫星 v_sat = {v_sat_mag/1e3:.2f} km/s (倾角55°, 11.97h周期)")
p("")

# ==== 关键物理: 长时间平均效应 ====
# v_cmb · v_sat: v_sat方向在轨道平面内旋转, 时间平均 = 0
# v_cmb · v_rot: v_rot方向在赤道面内旋转, 时间平均 = 0
# 但瞬时效应 = v_cmb · v_motion (周期性振荡)
p("===== 关键: 时间平均效应为0, 瞬时振荡振幅 =====")

# 瞬时最大点积 (v_motion 与 v_cmb 同向时)
# 卫星钟: v_sat_total = v_cmb + v_orb + v_sat
# 地面钟: v_ground_total = v_cmb + v_orb + v_rot

# v_orb 是两者共享的(地球公转), 在差中抵消!
# Δv² = |v_cmb+v_orb+v_sat|² - |v_cmb+v_orb+v_rot|²
#     = 2(v_cmb+v_orb)·(v_sat-v_rot) + |v_sat|² - |v_rot|²

# v_orb 与 v_cmb 的点积: v_orb 方向随季节变, 年平均为0
# 但 v_cmb·v_sat 和 v_cmb·v_rot 是主要项

# 最大瞬时点积 (v_sat 与 v_cmb 投影同向)
# v_sat 在 v_cmb 方向的最大投影 = v_sat (卫星轨道面与v_cmb方向夹角决定)
# 简化: 最大 = v_cmb * v_sat (最坏情况)
max_dot_sat = v_cmb_mag * v_sat_mag
max_dot_rot = v_cmb_mag * v_rot_eq

p(f"最大瞬时 v_cmb·v_sat = {max_dot_sat:.3e} (m/s)²")
p(f"最大瞬时 v_cmb·v_rot = {max_dot_rot:.3e} (m/s)²")

# 频率差: Δf/f0 ≈ (V_sat² - V_ground²)/(2c²)
# 最大差 = 2(v_cmb+v_orb)·(v_sat-v_rot)/(2c²) ≈ v_cmb·(v_sat-v_rot)/c²
max_delta = v_cmb_mag * (v_sat_mag - v_rot_eq) / c**2
p(f"\n最大瞬时频率差 Δf/f0 ≈ {max_delta:.3e}")

# 每天钟差振幅
day_s = 86400.0
max_clock_diff_us = max_delta * day_s * 1e6
p(f"最大瞬时钟差振幅 ≈ {max_clock_diff_us:.2f} μs/天 = {max_clock_diff_us/1e3:.3f} ms/天")

# 与GPS实测对比
p(f"\nGPS实测恒定漂移 = 38 μs/天 (已被SR -7 + GR +45解释)")
p(f"波源预言瞬时振荡振幅 = {max_clock_diff_us:.1f} μs/天")
p(f"比值 = {max_clock_diff_us/38:.1f}×")

# ==== 时间平均 ====
# v_sat 方向在轨道面内均匀旋转: <v_cmb·v_sat> = 0
# v_rot 方向在赤道面内均匀旋转: <v_cmb·v_rot> = 0
# 所以长时间平均 Δf/f0 = 0 (无恒定漂移, 只有振荡)
p(f"\n===== 长时间平均 =====")
p(f"v_cmb·v_sat 时间平均 = 0 (卫星轨道面内旋转)")
p(f"v_cmb·v_rot 时间平均 = 0 (地球自转)")
p(f">>> 波源理论预言: 无恒定钟差漂移, 只有周期性振荡")
p(f">>> GPS实测: 恒定漂移38μs/天(已解释) + 周期性残差~ns量级")
p(f">>> 波源振荡振幅 ~{max_clock_diff_us:.0f}μs vs GPS残差 ~ns: 差 {max_clock_diff_us/0.001:.0f}×")

# ==== 季节调制 ====
# v_orb 方向随季节变化(年周期), v_cmb·v_orb 产生年调制
# 但 v_orb 是地面钟和卫星钟共享的, 在差中抵消
# 所以季节调制不直接出现在钟差里

# ==== 关键结论 ====
p(f"\n===== 结论 =====")
p(f"1. 波源绝对速度效应 = 周期性振荡(12h/24h/年), 非恒定漂移")
p(f"2. 最大振幅 ~{max_clock_diff_us:.1f} μs/天 = {max_clock_diff_us/1e3:.2f} ms/天")
p(f"3. GPS实测周期性残差 ~ns量级, 与波源预言差 {max_clock_diff_us/0.001:.0f}×")
p(f"4. 但: 波源效应是'额外残差', GPS 38μs漂移已被相对论解释")
p(f"   若波源存在, GPS数据应显示~ms级振荡, 实测无 -> 强约束")
p(f"5. 例外: 若波源速度调制 f(v)=f0/(1+v²/2c²) 中的v不是'绝对速度大小'")
p(f"   而是'相对波源参考系的速度', 则上述分析不适用 -- 需要重新定义v的物理含义")

with io.open(r'C:\Users\Administrator\Doubao\chats\2026-10-11\new-chat\_VE_vector_sim.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(out))
print('OK')
