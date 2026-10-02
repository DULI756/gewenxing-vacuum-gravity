# 波源理论 · 完整成果包（Wave-Source Theory · Full Package）

**作者**：葛文星（Wenxing Ge）
**日期**：2026-10-02
**许可证**：CC BY-NC-ND 4.0（署名-非商业-禁止演绎，如需其他授权请联系作者）
**说明**：本包收录"波源理论"当前阶段的推导文档、复现脚本与知识库章节摘要。内容为作者独立研究，**未经同行评审**；文档中对未闭合环节均明确标注为开放项。

## 目录结构

```
质子10波源动态图.html        交互可视化：10 波源（四方反棱柱 8 + 上下轴 2）同频同相球面波、能量层/间歇层、硬核+指数尾电荷壳层、频率滑块（0.2–20×）
v4/
  波源理论_v4_质量反推与QCD衔接.md
  波源理论_v4_径向力尾与相干积分_推导.md    ← e^(−r/d) 来源检验：几何相干积分 vs 介质 Beer–Lambert 吸收
v5/
  波源理论_v5_质子电荷分布与形状因子_双组分_推导.{md,docx}   ← 10源硬核+指数尾壳层，对电子散射 RMS 1.7%
v6/
  波源理论_v6_奇异重子质量结构项_反解与超线性约束_推导.{md,docx}  ← Λ/Σ/Ξ/Ω 结构项，负结论（N_s 欠定）
scripts/
  _overlap_factor.py     几何重叠因子：半径→相干度→有效指数
  _two_source_force.py   两源相干积分：点源振荡判据
  _two_source_force2.py  退相干包络版
  _two_source_force3.py  传播型退相干版
  _shell_source.py       球对称壳源：振荡消失、单调短程
  _cluster_field.py      10源整体合成场包络（1/ρ² 扩散）
  _fit_structure_law.py  v6 结构律拟合
知识库章节摘要/
  ch16-wavesource-charge-formfactor.md   质子电荷形状因子双组分
  ch17-strange-baryon-structure.md       奇异重子质量结构项
  ch18-force-tail-coherence.md           径向力尾 e^(−r/d) 来源
```

## 核心框架（摘要）
- 波源连续爆发、不灭、万物永恒（P1/P2/P3 公设）。
- 质量 = m_c + μN；质子 10 源 / 中子 11 源；u=3、d=4。
- 引力耦合发散型驻波场，k=S/m 普适，G=Ck²。
- 微观核力含指数尾 e^(−r/d)，d=负压层宽度=λ/2。

## 当前开放项（诚实标注）
1. **e^(−r/d) 来源**：几何相干积分（1源/2源/10源）均不产生指数尾；唯一自洽来源是间歇真空层的 Beer–Lambert 指数吸收（d=吸收长度=λ/2）。闭合条件：证明 α=1/d 且 d=λ/2 自洽。
2. **奇异重子 N_s**：现框架内无简单超线性结构律能复现四奇异重子，结构项形式欠定。
3. **电荷形状因子**：硬核权重仅 0.10、壳参数 a 来源待解释。
4. 波源数-夸克映射、轴/环自旋比等为假设，非推导。

## 复现
脚本依赖 numpy；在 `scripts/` 下直接运行：
```
python _overlap_factor.py      # 重叠因子
python _two_source_force.py    # 两源点源判据
python _shell_source.py        # 壳源判据
python _cluster_field.py       # 10源合成场
python _fit_structure_law.py   # v6 结构律
```
