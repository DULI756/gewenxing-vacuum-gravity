# -*- coding: utf-8 -*-
"""research_log#52: Magpylib单位厘清+交叉校验通过"""
import sqlite3
con=sqlite3.connect(r'D:\波源\波源理论研究库.db'); cur=con.cursor()
mx=cur.execute("select coalesce(max(id),0) from research_log").fetchone()[0]
cur.execute("INSERT INTO research_log (id,ts,entry) VALUES (?,?,?)",(mx+1,"2026-10-11",
"Magpylib 5.2.3 安装+单位厘清+交叉校验通过（2026-10-11，审计L5.2）：v5起全SI单位——getB()→T(特斯拉,非v4的mT)、magnetization→A/m(=J/μ0,局部坐标)、magpy.misc.Dipole(moment=..)→A·m²。用官方Dipole点偶极源与手写教科书偶极场对比,4观测点相对差全=6.76e-10(浮点精度),完全一致→手写dipole_B=Magpylib官方=教科书标准,21源重叠场能差的手写公式获官方背书。教训:Sphere/Cuboid磁化强度换算绕弯且有方向偏差、v4/v5单位混淆(mT vs T)为两处错误;正确源=magpy.misc.Dipole。宏观实验用v5磁体源:getB→T、magnetization→A/m。脚本_magpylib_crosscheck.py。"))
con.commit();con.close()
con=sqlite3.connect(r'D:\波源\波源理论研究库.db')
print("research_log#",mx+1,":",con.execute("select substr(entry,1,26) from research_log where id=?",(mx+1,)).fetchone())
con.close()
