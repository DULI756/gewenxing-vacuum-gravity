# -*- coding: utf-8 -*-
"""质子 10 波源 · 空间结构 = 四方反棱柱(8) + 上下轴(2) · 自旋与发散波干涉（v3 示意，v4 版）
空间结构（加入 v3 的说明）：
  - 中间 8 源 = 正立方体的上、下两正方形面相对扭曲 45°（四方反棱柱顶点），绕轴自旋（慢）
  - 上下各 1 源 = 位于反棱柱轴线的两端，作为自旋轴；自旋速度比中间扭曲立方体快
  - 波源发散的是波（球面波前连续向外扩张），非点
降低波密度：减少场点、波前数量与采样。
输出 GIF。
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d.art3d import Line3DCollection

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

OMEGA = 2 * np.pi
LAM = 1.06
K = 2 * np.pi / LAM

A = 0.40          # 反棱柱外接半径（正方形面外接圆半径）
H = 0.40          # 反棱柱半高（上下正方形面 z 坐标）
Z_AX = 0.60       # 上下轴波源 z 坐标（轴端）
OM_M = 0.55       # 中间 8 源（扭曲立方体）自旋角速度（慢）
OM_AX = 1.7       # 上下轴源自旋角速度（快，> OM_M）

# 源基角（度）
BASE_B = np.radians([0, 90, 180, 270])     # 下面 4 源
BASE_T = np.radians([45, 135, 225, 315])   # 上面 4 源（相对下面扭曲 45°）


def gen_src(t):
    """返回 10 源位置：下4、上4、轴下、轴上"""
    rm = OM_M * t
    p = []
    for b in BASE_B:
        p.append([A * np.cos(b + rm), A * np.sin(b + rm), -H])
    for b in BASE_T:
        p.append([A * np.cos(b + rm), A * np.sin(b + rm), +H])
    p.append([0.0, 0.0, -Z_AX])
    p.append([0.0, 0.0, +Z_AX])
    return np.array(p)


# 场点（降低密度）
rng = np.random.default_rng(7)
rr = rng.random(1600) ** (1 / 3) * 1.10
th = rng.random(1600) * 2 * np.pi
ph = np.arccos(2 * rng.random(1600) - 1)
X = rr * np.sin(ph) * np.cos(th)
Y = rr * np.cos(ph)
Z = rr * np.sin(ph) * np.sin(th)


def field(t, src):
    v = np.zeros_like(X)
    for s in src:
        d = np.sqrt((X - s[0]) ** 2 + (Y - s[1]) ** 2 + (Z - s[2]) ** 2)
        v += np.cos(K * d - OMEGA * t) / (1 + d * d * 0.4)
    return v / 10


fig = plt.figure(figsize=(9, 7.6), dpi=110)
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#0b1020')
fig.patch.set_facecolor('#0d1220')

u = np.linspace(0, 2 * np.pi, 48)
vv = np.linspace(0, np.pi, 24)


def shell_lines(r, color, alpha):
    cx = r * np.outer(np.cos(u), np.sin(vv))
    cy = r * np.outer(np.sin(u), np.sin(vv))
    cz = r * np.outer(np.ones_like(u), np.cos(vv))
    ax.plot_wireframe(cx, cy, cz, color=color, alpha=alpha, linewidth=0.6)


shell_lines(0.67, '#6fe0a0', 0.5)   # 能量层 / 腔半径
shell_lines(0.93, '#ff9d9d', 0.45)   # 真空层 / 发散型驻波层边界

# 干涉粒子场
cmap = LinearSegmentedColormap.from_list(
    'wav', ['#060a1c', '#10203a', '#ffb84d', '#fff6d0'])
sc = ax.scatter(X, Y, Z, c=field(0, gen_src(0)), cmap=cmap,
                norm=plt.Normalize(-1, 1), s=2.5, alpha=0.9)

# 波源本体（柔和光晕）
src0 = gen_src(0)
core = ax.scatter(src0[:, 0], src0[:, 1], src0[:, 2], color='#ffd97a',
                  s=150, alpha=0.20, edgecolors='none')

# 中间 8 源（反棱柱）连线骨架，体现扭曲立方体
edge8 = []
for i in range(4):
    edge8.append([i, (i + 1) % 4])          # 下4 成环
    edge8.append([4 + i, 4 + (i + 1) % 4])  # 上4 成环
    edge8.append([i, 4 + i])                # 下-上 竖直（因 45° 扭曲，实为斜棱）
    edge8.append([i, 4 + (i + 1) % 4])      # 下-上 斜棱（扭棱）
segs0 = [[(src0[e[0], 0], src0[e[0], 1], src0[e[0], 2]),
          (src0[e[1], 0], src0[e[1], 1], src0[e[1], 2])] for e in edge8]
lc = Line3DCollection(segs0, color='#7fb2ff', alpha=0.5, lw=1.0)
ax.add_collection3d(lc)

# 每源向外扩张的球面波前（同心壳，表示发散的是波）——降低密度
MW = 3
PW = 12
wf_dir = []
for m in range(MW):
    a = np.linspace(0, 2 * np.pi, PW, endpoint=False)
    b = np.linspace(0, np.pi, PW // 2 + 2)
    for aa in a:
        for bb in b[1:-1]:
            wf_dir.append((np.cos(aa) * np.sin(bb), np.cos(bb), np.sin(aa) * np.sin(bb)))
wf_dir = np.array(wf_dir)
wf = ax.scatter([], [], [], c='#ffb84d', s=6, alpha=0.55, edgecolors='none')

# 上下轴源自旋指示光点（快转）
spin = ax.scatter([], [], [], c='#ffe08a', s=12, alpha=0.9, edgecolors='none')

cb = fig.colorbar(sc, ax=ax, fraction=0.028, pad=0.02)
cb.set_label('波峰(能量层) / 波谷(真空0压层)', color='#9fb0c8', fontsize=9)
cb.ax.tick_params(colors='#9fb0c8')

ax.set_xlim(-1.25, 1.25); ax.set_ylim(-1.25, 1.25); ax.set_zlim(-1.25, 1.25)
ax.set_axis_off()
ax.set_title('质子 10 波源：四方反棱柱(8, 上下面45°扭曲) + 上下轴(2, 自旋更快) · 发散波干涉',
             color='#ffffff', fontsize=11.5)

fps = 14
frames = 60
azim0 = 20.0


def update(i):
    t = i / fps
    src = gen_src(t)
    sc.set_array(field(t, src))
    core._offsets3d = (src[:, 0], src[:, 1], src[:, 2])

    # 反棱柱骨架线
    segs = [[(src[e[0], 0], src[e[0], 1], src[e[0], 2]),
             (src[e[1], 0], src[e[1], 1], src[e[1], 2])] for e in edge8]
    lc.set_segments(segs)

    # 波前（发散的是波）
    pxs, pys, pzs = [], [], []
    for n in range(10):
        for m in range(MW):
            frac = (t + m / MW) % 1.0
            r = 0.08 + frac * 0.98
            for q in wf_dir:
                pxs.append(src[n, 0] + q[0] * r)
                pys.append(src[n, 1] + q[1] * r)
                pzs.append(src[n, 2] + q[2] * r)
    wf._offsets3d = (pxs, pys, pzs)

    # 上下轴源快自旋指示：绕轴小半径光点
    ra = OM_AX * t
    sx_, sy_, sz_ = [], [], []
    g = 0.12
    for k in range(2):
        sx_.append(g * np.cos(ra + k * np.pi))
        sy_.append(g * np.sin(ra + k * np.pi))
        sz_.append(-Z_AX if k == 0 else Z_AX)
    spin._offsets3d = (sx_, sy_, sz_)

    ax.view_init(elev=26, azim=azim0 + 360 * i / frames)
    return [sc, core, lc, wf, spin]


ani = FuncAnimation(fig, update, frames=frames, interval=1000 / fps, blit=False)
ani.save(r'D:\波源\质子10波源反棱柱自旋_v4.gif', writer=PillowWriter(fps=fps))
print('saved ok')
