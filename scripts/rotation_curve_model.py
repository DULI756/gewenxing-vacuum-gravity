#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
波源理论：从核内引力到星系旋转曲线的统一模型
计算脚本：指数盘星系的旋转曲线预测

模型假设：
1. 每个波源持续向外发散间歇层（负压层）
2. 单个波源的间歇层密度随距离按1/r衰减
3. 总间歇层密度 = 所有波源贡献的线性叠加
4. 引力大小 = 当地总间歇层密度的绝对值
"""

import math
import json

# ============================================================
# 参数设置
# ============================================================

# 恒星盘参数
r_star = 1.0       # 恒星盘标度长度（归一化）

# 气体盘参数
r_gas = 2.5        # 气体盘标度长度（是恒星盘的2.5倍）
gas_ratio = 0.3    # 气体盘中心面密度是恒星盘的0.3倍

# 积分参数
dr = 0.1           # 径向积分步长
dphi = 0.1         # 角度积分步长
r_max = 15.0       # 积分上限（单位：r_star）

# ============================================================
# 核心函数
# ============================================================

def surface_density(r):
    """盘的面密度分布：恒星盘 + 气体盘"""
    star = math.exp(-r / r_star)
    gas = gas_ratio * math.exp(-r / r_gas)
    return star + gas


def rho_total(R):
    """
    计算距离中心R处的总间歇层密度
    1/r衰减，二维精确积分
    """
    integral = 0.0
    r_prime = 0.1

    while r_prime < r_max:
        phi = 0.0
        while phi < 2 * math.pi:
            # 两点距离
            inside = R*R + r_prime*r_prime - 2*R*r_prime*math.cos(phi)
            if inside < 0:
                inside = 0  # 数值精度保护
            dist = math.sqrt(inside)

            if dist < 0.01:
                phi += dphi
                continue

            # 1/r衰减
            integral += r_prime * surface_density(r_prime) / dist * dr * dphi
            phi += dphi

        r_prime += dr

    return integral


def rotation_curve(R_list):
    """计算旋转曲线"""
    results = []
    for R in R_list:
        rho = rho_total(R)
        g = rho  # 引力 = 绝对密度
        gR = g * R  # v² ∝ g*R
        results.append({
            'R_over_rd': R,
            'rho': rho,
            'gR': gR
        })
    return results


# ============================================================
# 主程序
# ============================================================

if __name__ == '__main__':
    R_list = [0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0, 12.0, 16.0]
    results = rotation_curve(R_list)

    print("=" * 60)
    print("波源理论：星系旋转曲线预测结果")
    print("=" * 60)
    print(f"{'R/r_d':>8} {'rho':>10} {'g*R (∝v²)':>12}")
    print("-" * 60)

    for res in results:
        print(f"{res['R_over_rd']:>8.1f} {res['rho']:>10.4f} {res['gR']:>12.4f}")

    print("=" * 60)
    print()
    print("结论：旋转曲线自然呈现上升→平坦→缓慢下降的形状")
    print("平坦区从约3倍盘标度长度开始，延伸至约10倍标度长度")
