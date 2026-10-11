# -*- coding: utf-8 -*-
"""补插: research_log(氦核, id=max+1) + meetings#19; 确认results#18"""
import sqlite3
con=sqlite3.connect(r'D:\波源\波源理论研究库.db');cur=con.cursor()
print("results#18:", cur.execute("select title,status from results where id=18").fetchone())
rlmax=cur.execute("select max(id) from research_log").fetchone()[0]
# 若1017已有则跳过
if cur.execute("select 1 from research_log where id=?",(rlmax+1,)).fetchone() is None:
    cur.execute("INSERT INTO research_log (id,ts,entry) VALUES (?,?,?)",(rlmax+1,"2026-10-11",
    "氦核结合能量级闭合(判决性,2026-10-11): 正四面体6对单偶极反平行×τ_b=0.5, s=1.7fm→28.3MeV精确闭合氦核结合能28.296(1.00×)。与氘核模式一致(氘核1对sep=1.989fm→2.2246;氦核6对s=1.7fm→28.3),核子距均落实验范围→机制非巧合,原子质量=核子磁自能组装主线获支撑。先诊断单偶极≈10/11源(差4.4%,氘核sep=1.989单偶极-4.67vs展开-4.46)。限制:6对反平行理想化+单偶极+独立求和忽略多体叠加;真实α Σm=0取向部分抵消。results#18。脚本_helium_scale/_reconnect_dipole_vs_expand。"))
    con.commit(); print("research_log#",rlmax+1,"inserted")
else:
    print("research_log#",rlmax+1,"already exists, skip")
con.close()
con=sqlite3.connect(r'D:\波源\波源理论会议记录库.db');cur=con.cursor()
mx2=cur.execute("select coalesce(max(id),0) from meetings").fetchone()[0]
if cur.execute("select 1 from meetings where id=?",(mx2+1,)).fetchone() is None:
    cur.execute("""INSERT INTO meetings (id,date,title,conclusions,decisions,next_steps,status) VALUES (?,?,?,?,?,?,?)""",
    (mx2+1,"2026-10-11","氦核结合能 正四面体6对 s=1.7fm 量级闭合",
    "氘核闭合机制推广氦核成功(量级):正四面体6对单偶极反平行×τ_b=0.5,s=1.7fm→28.3MeV精确闭合氦核结合能28.296。与氘核(1对sep=1.989→2.2246)模式一致,核子距均落实验范围→机制非巧合,原子质量=核子磁自能组装主线获支撑。单偶极≈10/11源(差4.4%)。",
    "results#18入库candidate; 氦核先用单偶极6对独立求和量级口径; 待用户拍板α核子构型与磁矩取向",
    "①用户拍板氦核4核子空间构型(正四面体?)与磁矩取向(Σm=0如何自洽);②真实取向约束下重算(部分抵消需更小s);③升级42源多体计算验证;④sep/s的独立实验锚定核实",
    "open"))
    con.commit(); print("meetings#",mx2+1,"inserted")
else:
    print("meetings#",mx2+1,"exists, skip")
con.close()
