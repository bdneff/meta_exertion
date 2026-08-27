"""
Main analysis. Produces Tables A-D, key rate ratios, sport ranking, mortality
comparison, and the outbreak conditional-severity table. All numbers derive
from data/master_dataset.csv, data/outbreaks.csv and the cited exposure model.
Writes analysis/output/*.csv and prints a full report.

Run: python3 analysis/run_analysis.py
"""
import os, json
import numpy as np
import pandas as pd
from stats_lib import poisson_ci, rate_ratio, pool_log_rates, rate_per_minute_mc, rate_ratio_mc
import exposure_model as EM

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "output"); os.makedirs(OUT, exist_ok=True)
PER = 1_000_000
def bn(t): print("\n"+"="*74+f"\n{t}\n"+"="*74)
def f(x, p=3):
    return "NA" if x is None or (isinstance(x,float) and np.isnan(x)) else f"{x:.{p}g}"

results = {}

# ===========================================================================
bn("PARTICIPANT-MINUTE MODEL (annual strenuous minutes, cited S06)")
# ===========================================================================
print("Military recruit-year -> minutes:  A(formal PT)", EM.MIL_RECRUIT_MIN_PER_YEAR["A"],
      " B(all MVPA)", EM.MIL_RECRUIT_MIN_PER_YEAR["B"])
print("NCAA athlete-year -> minutes:       football", EM.NCAA_MIN_PER_YEAR["football"],
      " generic", EM.NCAA_MIN_PER_YEAR["generic"])
print("NCAA min/AE football", EM.NCAA_MIN_PER_AE["football_all"],
      " Mil min/person-week A", EM.MIL_MIN_PER_PERSONWEEK["A"], " B", EM.MIL_MIN_PER_PERSONWEEK["B"])

# ===========================================================================
bn("TABLE A — PRIMARY: serious acute non-traumatic exertional events / 1e6 participant-minutes")
# ===========================================================================
# Each row: population, events, exposure-count, minutes-per-exposure(lo,ce,hi), grade
tableA = []
def add_minrate(label, count, n_exp, mins, grade, note, denomlabel):
    med, lo, hi, mean = rate_per_minute_mc(count, n_exp, mins[0], mins[2])
    # also central point estimate at central minutes
    pt = count / (n_exp * mins[1]) * PER
    tableA.append(dict(population=label, events=count, exposure=n_exp,
        min_per_exp=f"{mins[0]}-{mins[1]}-{mins[2]}", denom=denomlabel,
        rate_per_1e6min=round(med,4), ci_lo=round(lo,4), ci_hi=round(hi,4),
        point=round(pt,4), quality=grade, note=note))
    return med, lo, hi

# --- NCAA: serious EHI (emergency transport), sanctioned practice/comp only (Yeargin) ---
# denominator = 4,908,478 AE; minutes per AE (total session)
add_minrate("NCAA all-sports: EHI emergency transport", 19, 4_908_478,
            EM.NCAA_MIN_PER_AE["generic"], "B",
            "ISP transports only; EXCLUDES conditioning where deaths/rhabdo occur -> underestimate",
            "NCAA total-session min")
# --- NCAA football: serious EHI transport (9 of 174) ---
add_minrate("NCAA football: EHI emergency transport", 9, 1_122_581,
            EM.NCAA_MIN_PER_AE["football_all"], "B",
            "9 transports/174 EHI; sanctioned practice/comp only", "NCAA total-session min")
# --- Military recruit: serious = heat stroke + rhabdo-hospitalized (2024), per recruit-year ->min ---
# Build participant-minutes from recruit-years for denom B and A separately.
for denom in ["B", "A"]:
    ry = 23150  # 2024 all-service recruit person-years
    mins_year = EM.MIL_RECRUIT_MIN_PER_YEAR[denom]
    serious = 27 + 22   # heat stroke (urgent) + rhabdo hospitalized
    med, lo, hi, mean = rate_per_minute_mc(serious, ry, mins_year[0], mins_year[2])
    pt = serious/(ry*mins_year[1])*PER
    tableA.append(dict(population=f"Military recruit: heat stroke + rhabdo-hosp (denom {denom})",
        events=serious, exposure=ry, min_per_exp=f"{mins_year[0]}-{mins_year[1]}-{mins_year[2]} /yr",
        denom=("all MVPA" if denom=="B" else "formal PT only"),
        rate_per_1e6min=round(med,4), ci_lo=round(lo,4), ci_hi=round(hi,4),
        point=round(pt,4), quality="B", note="2024 MSMR; serious=heat stroke+rhabdo inpatient"))
# --- Military recruit heat illness (Barnes, OBSERVED person-weeks), all severity ---
for denom in ["B", "A"]:
    mins_pw = EM.MIL_MIN_PER_PERSONWEEK[denom]
    med, lo, hi, mean = rate_per_minute_mc(1210, 3_362_271, mins_pw[0], mins_pw[2])
    pt = 1210/(3_362_271*mins_pw[1])*PER
    tableA.append(dict(population=f"Military recruit (Army BCT): ALL heat illness (denom {denom})",
        events=1210, exposure=3_362_271, min_per_exp=f"{mins_pw[0]}-{mins_pw[1]}-{mins_pw[2]} /p-wk",
        denom=("all MVPA" if denom=="B" else "formal PT only"),
        rate_per_1e6min=round(med,4), ci_lo=round(lo,4), ci_hi=round(hi,4),
        point=round(pt,4), quality="A" if denom=="B" else "A",
        note="Barnes 2019 observed person-weeks; all-severity (mostly heat exhaustion)"))
dfA = pd.DataFrame(tableA)
print(dfA.to_string(index=False))
dfA.to_csv(os.path.join(OUT,"tableA_primary.csv"), index=False)

# ===========================================================================
bn("MORTALITY COMPARISON — clean matched units (per 100,000 person/athlete-YEARS)")
# ===========================================================================
mort = [
    ("NCAA all-sport exertional SCD", 72, 9_106_516, "Petek 2024; 50% of 143 SCD exertional"),
    ("NCAA all-sport heat-illness death", 3, 4_242_519, "Harmon 2015"),
    ("NCAA all-sport SCT/sickling death", 10, 4_242_519, "Harmon 2015"),
    ("NCAA football non-traumatic death (conditioning)", 34, 1_285_095, "Boden 2020; 100% conditioning"),
    ("Military recruit exercise-related death (1977-2001)", 141, 969_231, "Scoville/Borden; OLD regime"),
    ("Military recruit nontraumatic sudden death (1977-2001)", 126, 969_231, "Eckart 2004"),
    ("Military recruit EHI death (1977-2001)", 30, 969_231, "Scoville/Borden"),
    ("Military recruit exertional SCD (1977-2001)", 60, 969_231, "Scoville/Borden"),
]
mrows=[]
for lab,c,e,note in mort:
    r,lo,hi = poisson_ci(c,e,per=100000)
    mrows.append(dict(population=lab, deaths=c, person_years=e,
        rate_per_100k_yr=round(r,3), ci_lo=round(lo,3), ci_hi=round(hi,3), note=note))
dfM = pd.DataFrame(mrows); print(dfM.to_string(index=False))
dfM.to_csv(os.path.join(OUT,"mortality_peryear.csv"), index=False)

# NCAA total exertional death rate (sum of components, per athlete-year, approx)
ncaa_exert_death_rate = 72/9_106_516 + 3/4_242_519 + 10/4_242_519  # per athlete-yr
print(f"\nNCAA all-sport total exertional death (SCD-exertional + heat + sickling) "
      f"~ {ncaa_exert_death_rate*100000:.2f}/100,000 athlete-years")

# ===========================================================================
bn("MORTALITY per PARTICIPANT-MINUTE (converting person-years -> strenuous minutes)")
# ===========================================================================
# Military recruit exercise-related death per minute (OLD regime), denom A & B
mm=[]
for denom in ["A","B"]:
    myr = EM.MIL_RECRUIT_MIN_PER_YEAR[denom]
    med,lo,hi,mean = rate_per_minute_mc(141, 969_231, myr[0], myr[2])
    mm.append(("Mil recruit exercise death OLD ("+denom+")", round(med,4),round(lo,4),round(hi,4)))
# NCAA football conditioning death per minute
nyr = EM.NCAA_MIN_PER_YEAR["football"]
med,lo,hi,mean = rate_per_minute_mc(34, 1_285_095, nyr[0], nyr[2])
mm.append(("NCAA football nontraumatic death", round(med,4),round(lo,4),round(hi,4)))
# NCAA all-sport exertional death per minute (generic athlete-year minutes)
gyr = EM.NCAA_MIN_PER_YEAR["generic"]
ncaa_exert_deaths = 72; ncaa_exert_py = 9_106_516  # exertional SCD as the anchor count
med,lo,hi,mean = rate_per_minute_mc(72, 9_106_516, gyr[0], gyr[2])
mm.append(("NCAA all-sport exertional SCD", round(med,4),round(lo,4),round(hi,4)))
for lab,md,lo,hi in mm: print(f"  {lab:42s} {md:>8}  [{lo}, {hi}] /1e6 min")
results["mortality_permin"]=mm

# ===========================================================================
bn("KEY RATE RATIOS (per participant-minute, Monte-Carlo, both duration bands)")
# ===========================================================================
# RR = military recruit / NCAA for the exercise-related DEATH endpoint, per-minute
def rr_permin(c1,n1,m1,c2,n2,m2,label):
    md,lo,hi = rate_ratio_mc(c1,n1,m1[0],m1[2], c2,n2,m2[0],m2[2])
    print(f"  {label:52s} RR {md:6.2f}  [{lo:.2f}, {hi:.2f}]")
    return (label, round(md,2), round(lo,2), round(hi,2))
rr=[]
# Military recruit exercise death (old) vs NCAA football nontraumatic death, per-minute, denom B
rr.append(rr_permin(141,969_231,EM.MIL_RECRUIT_MIN_PER_YEAR["B"],
                    34,1_285_095,EM.NCAA_MIN_PER_YEAR["football"],
                    "Mil recruit death(OLD,B) / NCAA football death /min"))
rr.append(rr_permin(141,969_231,EM.MIL_RECRUIT_MIN_PER_YEAR["A"],
                    34,1_285_095,EM.NCAA_MIN_PER_YEAR["football"],
                    "Mil recruit death(OLD,A) / NCAA football death /min"))
# Military recruit serious morbidity (heat stroke+rhabdo hosp 2024) vs NCAA serious EHI transport, per-min
rr.append(rr_permin(49,23150,EM.MIL_RECRUIT_MIN_PER_YEAR["B"],
                    19,4_908_478,[m/ (1/ (1)) for m in [0]] or EM.NCAA_MIN_PER_AE["generic"],
                    "Mil recruit serious(B) / NCAA EHI transport /min") if False else
          ("skip",0,0,0))
# do NCAA EHI transport minute-denominator properly (AE-based)
md,lo,hi = rate_ratio_mc(49,23150,EM.MIL_RECRUIT_MIN_PER_YEAR["B"][0],EM.MIL_RECRUIT_MIN_PER_YEAR["B"][2],
                         19,4_908_478,EM.NCAA_MIN_PER_AE["generic"][0],EM.NCAA_MIN_PER_AE["generic"][2])
print(f"  {'Mil recruit serious(B) / NCAA EHI transport /min':52s} RR {md:6.2f}  [{lo:.2f}, {hi:.2f}]")
rr.append(("Mil recruit serious(B)/NCAA EHI transport per-min", round(md,2),round(lo,2),round(hi,2)))
md,lo,hi = rate_ratio_mc(49,23150,EM.MIL_RECRUIT_MIN_PER_YEAR["A"][0],EM.MIL_RECRUIT_MIN_PER_YEAR["A"][2],
                         19,4_908_478,EM.NCAA_MIN_PER_AE["generic"][0],EM.NCAA_MIN_PER_AE["generic"][2])
print(f"  {'Mil recruit serious(A) / NCAA EHI transport /min':52s} RR {md:6.2f}  [{lo:.2f}, {hi:.2f}]")
rr.append(("Mil recruit serious(A)/NCAA EHI transport per-min", round(md,2),round(lo,2),round(hi,2)))
results["rate_ratios"]=rr

# ===========================================================================
bn("TABLE B — DIAGNOSIS-SPECIFIC rates (native units, per population)")
# ===========================================================================
df = pd.read_csv(os.path.join(ROOT,"data","master_dataset.csv"))
diag = df[df.endpoint.isin(["EHI_any","rhabdo","heat_stroke","heat_exhaustion",
     "serious_transport","death_nontraumatic","death_exercise","death_EHS",
     "death_sickling","hyponatremia","rhabdo_inpatient","heat_any"])].copy()
colB = diag[["population","diagnosis","events","denom_value","denom_unit","orig_rate","orig_rate_unit","quality"]]
print(colB.to_string(index=False))
colB.to_csv(os.path.join(OUT,"tableB_diagnosis.csv"), index=False)

# ===========================================================================
bn("SPORT RANKING — NCAA EHI per participant-minute (per 1e6, central minutes)")
# ===========================================================================
sportmap = {"football":("football_all",1_122_581,174),
            "men's basketball":("basketball",292_683,12),
            "women's soccer":("soccer",266_667,8),
            "men's soccer":("soccer",193_548,6),
            "women's outdoor track":("generic",101_695,6),
            "men's wrestling":("generic",103_448,3),
            "men's cross-country":("generic",62_500,3),
            "women's lacrosse":("lacrosse",142_857,1)}
srows=[]
for sport,(mk,ae,cnt) in sportmap.items():
    mins=EM.NCAA_MIN_PER_AE.get(mk,EM.NCAA_MIN_PER_AE["generic"])
    med,lo,hi,mean = rate_per_minute_mc(cnt,ae,mins[0],mins[2])
    srows.append(dict(sport=sport,EHI=cnt,AE=ae,min_per_AE=f"{mins[0]}-{mins[2]}",
        rate_per_1e6min=round(med,4),ci_lo=round(lo,4),ci_hi=round(hi,4)))
dfS=pd.DataFrame(srows).sort_values("rate_per_1e6min",ascending=False)
print(dfS.to_string(index=False)); dfS.to_csv(os.path.join(OUT,"sport_ranking.csv"),index=False)

# ===========================================================================
bn("TABLE C — OUTBREAK conditional severity (attack rate + per-minute)")
# ===========================================================================
ob = pd.read_csv(os.path.join(ROOT,"data","outbreaks.csv"))
oc=[]
for _,r in ob.iterrows():
    exposed=r["exposed"]; hosp=r["hospitalized_inpatient"]; mins=r["workout_minutes"]
    ar = (hosp/exposed) if (pd.notna(exposed) and pd.notna(hosp) and exposed>0) else np.nan
    Rmin = (hosp/(exposed*mins)*PER) if (pd.notna(exposed) and pd.notna(hosp) and pd.notna(mins) and exposed>0 and mins>0) else np.nan
    oc.append(dict(id=r["outbreak_id"],inst=r["institution"],sport=r["sport_program"],
        exposed=exposed,cases=r["cases"],hosp=hosp,workout_min=mins,
        attack_rate_hosp=round(ar,3) if pd.notna(ar) else "NA",
        hosp_per_1e6min=round(Rmin,1) if pd.notna(Rmin) else "NA"))
dfC=pd.DataFrame(oc); print(dfC.to_string(index=False)); dfC.to_csv(os.path.join(OUT,"tableC_outbreaks.csv"),index=False)
print("\nNOTE: outbreak rates are SELECTED-ON-OUTCOME conditional severity, NOT population incidence.")

# ===========================================================================
bn("TABLE D — SENSITIVITY: NCAA:military serious-event RR across minute assumptions")
# ===========================================================================
# Vary NCAA min/AE (90/120/150) and military denom (A formal vs B all MVPA)
sens=[]
for ncaa_min in [90,120,150]:
    for denom,mil_lab in [("A","formal PT"),("B","all MVPA")]:
        myr=EM.MIL_RECRUIT_MIN_PER_YEAR[denom][1]
        ncaa_rate = 19/(4_908_478*ncaa_min)*PER
        mil_rate  = 49/(23150*myr)*PER
        sens.append(dict(ncaa_min_per_AE=ncaa_min, mil_denom=mil_lab,
            NCAA_serious_per1e6=round(ncaa_rate,4), Mil_serious_per1e6=round(mil_rate,4),
            RR_mil_over_ncaa=round(mil_rate/ncaa_rate,2)))
dfD=pd.DataFrame(sens); print(dfD.to_string(index=False)); dfD.to_csv(os.path.join(OUT,"tableD_sensitivity.csv"),index=False)

# save machine-readable summary
with open(os.path.join(OUT,"summary.json"),"w") as fh:
    json.dump({"rate_ratios":rr,"mortality_permin":mm,
               "ncaa_exert_death_per100k_yr":round(ncaa_exert_death_rate*100000,3)}, fh, indent=2)
bn("DONE — outputs in analysis/output/")
print(os.listdir(OUT))
