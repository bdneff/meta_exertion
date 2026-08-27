"""
Generate the seven required figures into figures/. Log scales used where the
dynamic range demands it (outbreaks are 10^4-10^5x baseline).
"""
import os, numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator

HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
FIG=os.path.join(ROOT,"figures"); os.makedirs(FIG,exist_ok=True)
OUT=os.path.join(HERE,"output")

# palette
C_NCAA="#2b6cb0"; C_MIL="#c05621"; C_OUT="#9b2c2c"; C_GREY="#4a5568"
plt.rcParams.update({"font.size":10,"axes.grid":True,"grid.alpha":0.25,
    "axes.spines.top":False,"axes.spines.right":False,"figure.dpi":130})

# ---------------------------------------------------------------------------
# FIG 1 — Forest: serious exertional-event incidence per 1e6 participant-minutes
# ---------------------------------------------------------------------------
dfA=pd.read_csv(os.path.join(OUT,"tableA_primary.csv"))
fig,ax=plt.subplots(figsize=(9,4.6))
labels=dfA["population"].tolist(); y=np.arange(len(labels))[::-1]
colors=[C_MIL if "Military" in l else C_NCAA for l in labels]
ax.errorbar(dfA["rate_per_1e6min"],y,
    xerr=[dfA["rate_per_1e6min"]-dfA["ci_lo"], dfA["ci_hi"]-dfA["rate_per_1e6min"]],
    fmt="o",ms=7,capsize=3,lw=1.4,ecolor=C_GREY,mfc="white",mec=C_GREY,zorder=3)
for xi,yi,c in zip(dfA["rate_per_1e6min"],y,colors):
    ax.plot(xi,yi,"o",ms=8,color=c,zorder=4)
ax.set_yticks(y); ax.set_yticklabels([l.replace("Military","Mil.").replace("(denom ","(") for l in labels],fontsize=8)
ax.set_xscale("log"); ax.set_xlabel("Serious exertional events per 1,000,000 participant-minutes (log scale)")
ax.set_title("Fig 1. Serious exertional-event incidence per participant-minute\n(NCAA blue, military orange; bars = 95% CI incl. duration uncertainty)",fontsize=10)
plt.tight_layout(); plt.savefig(os.path.join(FIG,"fig1_forest_incidence.png")); plt.close()

# ---------------------------------------------------------------------------
# FIG 2 — Forest of NCAA vs military rate ratios (per minute)
# ---------------------------------------------------------------------------
import json
summ=json.load(open(os.path.join(OUT,"summary.json")))
rr=summ["rate_ratios"]
rr=[r for r in rr if r[0]!="skip"]
fig,ax=plt.subplots(figsize=(9,3.6))
labs=[r[0] for r in rr]; med=[r[1] for r in rr]; lo=[r[2] for r in rr]; hi=[r[3] for r in rr]
y=np.arange(len(labs))[::-1]
ax.errorbar(med,y,xerr=[np.array(med)-np.array(lo),np.array(hi)-np.array(med)],
    fmt="s",ms=7,capsize=3,color=C_MIL,ecolor=C_GREY,lw=1.4)
ax.axvline(1,color=C_GREY,ls="--",lw=1)
ax.set_yticks(y); ax.set_yticklabels(labs,fontsize=8); ax.set_xscale("log")
ax.set_xlabel("Rate ratio  (military recruit ÷ NCAA)  — log scale; RR>1 favors NCAA safer per minute")
ax.set_title("Fig 2. Military-recruit vs NCAA rate ratios per participant-minute",fontsize=10)
plt.tight_layout(); plt.savefig(os.path.join(FIG,"fig2_forest_RR.png")); plt.close()

# ---------------------------------------------------------------------------
# FIG 3 — NCAA sport ranking (EHI per 1e6 min)
# ---------------------------------------------------------------------------
dfS=pd.read_csv(os.path.join(OUT,"sport_ranking.csv")).sort_values("rate_per_1e6min")
fig,ax=plt.subplots(figsize=(8.5,4.2)); y=np.arange(len(dfS))
ax.barh(y,dfS["rate_per_1e6min"],color=C_NCAA,alpha=.85)
ax.errorbar(dfS["rate_per_1e6min"],y,xerr=[dfS["rate_per_1e6min"]-dfS["ci_lo"],dfS["ci_hi"]-dfS["rate_per_1e6min"]],
    fmt="none",ecolor=C_GREY,capsize=3,lw=1)
ax.set_yticks(y); ax.set_yticklabels(dfS["sport"],fontsize=9)
ax.set_xlabel("Exertional heat illness per 1,000,000 participant-minutes")
ax.set_title("Fig 3. NCAA sport ranking — EHI per participant-minute\n(football is the outlier; lacrosse is NOT)",fontsize=10)
plt.tight_layout(); plt.savefig(os.path.join(FIG,"fig3_sport_ranking.png")); plt.close()

# ---------------------------------------------------------------------------
# FIG 4 — Military program ranking (heat illness, native per-100k or per-10k pw)
# ---------------------------------------------------------------------------
prog=[("Army BCT Fort Benning (heat, /10k p-wk)",6.8),
      ("Army BCT all sites (heat, /10k p-wk)",3.6),
      ("Army BCT Fort Jackson",4.5),("Army BCT Fort Sill",1.8),
      ("Army BCT Fort Leonard Wood",1.7)]
fig,ax=plt.subplots(figsize=(8,3.4))
labs=[p[0] for p in prog]; vals=[p[1] for p in prog]; y=np.arange(len(labs))
ax.barh(y,vals,color=C_MIL,alpha=.85)
ax.set_yticks(y); ax.set_yticklabels(labs,fontsize=8)
ax.set_xlabel("Heat illness per 10,000 BCT person-weeks (Barnes 2019, observed)")
ax.set_title("Fig 4. Military recruit heat-illness rate by BCT installation",fontsize=10)
ax.invert_yaxis()
plt.tight_layout(); plt.savefig(os.path.join(FIG,"fig4_military_ranking.png")); plt.close()

# ---------------------------------------------------------------------------
# FIG 5 — log-scale: baseline population rates vs outbreak conditional severity
# ---------------------------------------------------------------------------
dfC=pd.read_csv(os.path.join(OUT,"tableC_outbreaks.csv"))
dfC=dfC[dfC["hosp_per_1e6min"]!="NA"].copy(); dfC["hosp_per_1e6min"]=dfC["hosp_per_1e6min"].astype(float)
fig,ax=plt.subplots(figsize=(9,4.2))
# baseline band
base_vals=dfA["rate_per_1e6min"].values
ax.axhspan(base_vals.min(),base_vals.max(),color=C_NCAA,alpha=.12,label="baseline population rates (Table A)")
for xi,(_,r) in enumerate(dfC.iterrows()):
    ax.scatter(xi,r["hosp_per_1e6min"],s=60,color=C_OUT,zorder=3)
    ax.annotate(r["id"],(xi,r["hosp_per_1e6min"]),fontsize=7,xytext=(0,6),textcoords="offset points",ha="center")
ax.set_yscale("log"); ax.set_ylabel("Hospitalizations per 1,000,000 participant-minutes (log)")
ax.set_xticks(range(len(dfC))); ax.set_xticklabels(dfC["inst"],rotation=30,ha="right",fontsize=7)
ax.set_title("Fig 5. Outbreak conditional severity vs baseline (log scale)\noutbreaks sit 10^3-10^5x above baseline — NOT population incidence",fontsize=10)
ax.legend(fontsize=8,loc="upper right")
plt.tight_layout(); plt.savefig(os.path.join(FIG,"fig5_outbreak_logscale.png")); plt.close()

# ---------------------------------------------------------------------------
# FIG 6 — sensitivity: RR vs assumed minutes
# ---------------------------------------------------------------------------
dfD=pd.read_csv(os.path.join(OUT,"tableD_sensitivity.csv"))
fig,ax=plt.subplots(figsize=(7.5,4))
for denom,mk,c in [("formal PT","o",C_MIL),("all MVPA","s",C_NCAA)]:
    sub=dfD[dfD.mil_denom==denom]
    ax.plot(sub["ncaa_min_per_AE"],sub["RR_mil_over_ncaa"],mk+"-",color=c,label=f"military denom: {denom}")
ax.axhline(1,color=C_GREY,ls="--",lw=1)
ax.set_xlabel("Assumed NCAA minutes per athlete-exposure"); ax.set_ylabel("RR (military recruit ÷ NCAA), serious events per minute")
ax.set_title("Fig 6. Sensitivity of the military:NCAA rate ratio to exposure-minute assumptions",fontsize=10)
ax.legend(fontsize=9)
plt.tight_layout(); plt.savefig(os.path.join(FIG,"fig6_sensitivity.png")); plt.close()

# ---------------------------------------------------------------------------
# FIG 7 — temporal trends (military recruit rhabdo + heat; NCAA policy eras)
# ---------------------------------------------------------------------------
fig,ax=plt.subplots(figsize=(8.5,4))
yrs=[2020,2021,2022,2023,2024,2025]
rhabdo=[np.nan,np.nan,379.2,421.0,410.4,219.0]  # recruit rhabdo /100k
heatstroke=[np.nan,np.nan,117.0,391.3,116.6,127.1]  # recruit HS /100k (2023 artifact)
ax.plot(yrs,rhabdo,"o-",color=C_MIL,label="Mil recruit rhabdomyolysis /100k p-yr")
ax.plot(yrs,heatstroke,"s--",color="#dd6b20",label="Mil recruit heat stroke /100k p-yr")
ax.annotate("2023 heat = denominator\nartifact (exclude)",(2023,391.3),fontsize=7,
    xytext=(2020.6,360),textcoords="data",arrowprops=dict(arrowstyle="->",color=C_GREY))
ax.set_xlabel("Year"); ax.set_ylabel("Incidence per 100,000 recruit person-years")
ax.set_title("Fig 7. Military recruit exertional-event temporal trend (MSMR)",fontsize=10)
ax.legend(fontsize=8)
plt.tight_layout(); plt.savefig(os.path.join(FIG,"fig7_temporal.png")); plt.close()

print("figures written:", sorted(os.listdir(FIG)))
