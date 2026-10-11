# -*- coding: utf-8 -*-
"""results#18 + research_log#53: 氘核重叠场能差数值收敛确认(修正列名)"""
import sqlite3
con=sqlite3.connect(r'D:\波源\波源理论研究库.db');cur=con.cursor()
mx=cur.execute("select coalesce(max(id),0) from results").fetchone()[0]
cur.execute("""INSERT INTO results (id,title,statement,formula,evidence,status,tags) VALUES (?,?,?,?,?,?,?)""",
(mx+1,"氘核结合能=两核子磁自能场重叠交叉项(高频动态修正)",
"氘核结合能第一性机制: 两核子(质子10源+中子11源)核外磁自能场重叠交叉项, 反平行释放",
"E_int=∫(B_p·B_n)/μ0 dV; E_pulse=τ_b·E_int",
"向量化0.033fm→E_int=−5.5572MeV(0.06fm原−5.5953,变0.7%→已收敛); Magpylib Dipole对照0.05fm→−5.5118一致; τ_b=0.5→−2.78MeV距2.2246差25.1%",
"candidate","氘核/结合能/磁重连/重叠场能"))
con.commit()
cur.execute("INSERT INTO research_log (id,ts,entry) VALUES (?,?,?)",(mx+1000,"2026-10-11",
"氘核重叠场能差数值收敛确认(回到主线第一步,2026-10-11):向量化重算0.033fm→E_int=−5.5572MeV(0.06fm原−5.5953,仅变0.7%→数值已收敛),Magpylib Dipole对照0.05fm→−5.5118一致。收敛值E_int≈−5.56MeV,τ_b=0.5→−2.78MeV距2.2246差25.1%。确认卡点非数值而物理口径(源磁矩115.9μN/sep=1.9fm/τ_b=0.5组合)。results#18。脚本_reconnect_overlap_vec.py。"))
con.commit();con.close()
con=sqlite3.connect(r'D:\波源\波源理论研究库.db')
print("results#",mx+1,":",con.execute("select id,title,status from results where id=?",(mx+1,)).fetchone())
con.close()
