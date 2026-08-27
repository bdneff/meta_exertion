# Acute Exertional Medical Events in NCAA Athletes vs. U.S. Military Trainees
## Systematic Review & Quantitative Synthesis — Results and Conclusions

*Companion documents:* `METHODS.md` (pre-registered methods), `sources/source_ledger.md`
(every figure traced to a primary source), `data/*.csv` (machine-readable dataset),
`analysis/*.py` (reproducible code), `figures/*.png` (visualizations).

---

## Executive summary

**The headline finding is a reframing.** Compared per unit of *actual strenuous
training time*, the enormous apparent gap between military recruits and NCAA
athletes largely collapses. Raw per-person-year comparisons make military basic
training look ~13× more dangerous than NCAA athletics for exertional death; but a
recruit accumulates roughly **3–4× more strenuous-training minutes per year** than
a collegiate athlete, so once you normalize to participant-minutes the ratio falls
to between **~1× and ~5×**, and under the most defensible "all strenuous activity"
denominator the two populations are **statistically indistinguishable** for serious
exertional events (rate ratio 0.86–1.44; Table D, Fig 6).

Three robust conclusions survive every sensitivity assumption:

1. **Serious exertional events are rare in both populations** and, per training-minute,
   of the *same order of magnitude* (~0.03–0.14 serious events per 1,000,000
   participant-minutes). Neither population is dramatically safer than the other
   once exposure is measured correctly.
2. **Within the NCAA, football is a genuine exertional-illness outlier; lacrosse is
   not.** Football's per-minute EHI rate (~1.05/10⁶ min) is 2–13× every other sport.
   Men's and women's lacrosse rank at or near the *bottom* — their reputation comes
   from a single publicized 2024 outbreak, not baseline risk.
3. **Publicized "hell week" hospital clusters are extreme outliers, not baseline.**
   Outbreak hospitalization rates run **10³–10⁵× above** either population's baseline
   (Fig 5). They are selected-on-outcome and must never be read as population incidence.

All estimates are graded A (direct) to D (weak). The cleanest comparison
(mortality, in matched person-year units) is Grade A; the per-minute conversions
are Grade B–C because they require cited but uncertain duration assumptions, which
we propagate by Monte Carlo rather than hide.

---

## 1. The central methodological result: why the denominator changes the answer

The two surveillance systems measure fundamentally different denominators —
NCAA uses **athlete-exposures** (one athlete, one session), the military uses
**person-years** — and neither is training-minutes. Our core contribution is to
convert both, with propagated uncertainty, to **events per 1,000,000
participant-minutes of strenuous physical training**.

The load-bearing empirical facts (all cited, `S06`):

| Quantity | Value | Source |
|---|---|---|
| Army BCT measured MVPA | 168 moderate + 14 vigorous ≈ **182 min/day** | Alemany 2022 |
| Army IET measured MVPA | **~172 min/day** (1,202 min/wk) | McAdam 2018 |
| Army formal PT session | **45–60 min, 5–6×/wk** | TC 3-22.20 |
| NCAA football practice (measured) | **142 ± 16 min** (total session, incl. idle) | DeMartini 2011 |
| Recruit strenuous min / recruit-year | **~57,000** (all MVPA) or **~15,000** (formal PT only) | derived, S06 |
| NCAA athlete strenuous min / athlete-year | **~16,000–21,000** (total session) | derived, S06 |

A recruit trains **nearly full-time** during their course; an NCAA athlete trains
**part-time and seasonally**. That single fact — not any difference in intrinsic
danger — drives most of the raw per-person gap.

**Two unavoidable caveats, both flagged throughout:**
- Military MVPA excludes idle time; NCAA session minutes include it (no NCAA sport
  has published %-above-threshold data). So NCAA per-minute rates are, if anything,
  *under*-stated relative to military — biasing NCAA toward *looking safer*. Our
  NCAA-is-comparable-or-higher conclusions are therefore **conservative**.
- Doctrine/schedule-based military denominators are badly biased low: the USMC POI
  lists 46.3 miles of run/hike but recruits actually cover **657.6 miles** (~14×;
  Kloss 2024). We use **measured** activity, never schedules.

---

## 2. Table A — Primary comparison (serious events per 1,000,000 participant-minutes)

Serious = requiring hospitalization or urgent emergency transport.
Point estimate at central minutes; 95% CI includes duration + Poisson uncertainty
(Monte Carlo). Full table: `analysis/output/tableA_primary.csv`; Fig 1.

| Population | Events | Denominator basis | Serious events / 10⁶ min (95% CI) | Grade |
|---|---|---|---|---|
| NCAA all-sports — EHI emergency transport | 19 | 4.91M AE × session-min | **0.033 (0.019–0.055)** | B |
| NCAA football — EHI emergency transport | 9 | 1.12M AE × session-min | **0.056 (0.026–0.104)** | B |
| Military recruit — heat stroke + rhabdo-hosp (all-MVPA denom) | 49 | 23,150 recruit-yr × MVPA min | **0.041 (0.029–0.057)** | B |
| Military recruit — heat stroke + rhabdo-hosp (formal-PT denom) | 49 | 23,150 recruit-yr × PT min | **0.140 (0.096–0.205)** | B |
| Military recruit (Army BCT) — *all* heat illness (all-MVPA) | 1,210 | 3.36M person-wk (observed) × MVPA | **0.36 (0.30–0.44)** | A |
| Military recruit (Army BCT) — *all* heat illness (formal-PT) | 1,210 | 3.36M person-wk (observed) × PT | **1.23 (1.00–1.59)** | A |

**Reading:** For the *serious* endpoint, NCAA (0.033–0.056) and military recruits
(0.041 under all-MVPA) overlap. The military rate exceeds NCAA only when you count
*formal PT minutes alone* (0.140) — i.e., when you credit the military with far
fewer minutes than they actually train. The one Grade-A observed-denominator row
(Barnes BCT) is *all* heat illness (mostly mild heat exhaustion), not serious, and
is not diagnosis-matched to the NCAA serious row.

---

## 3. Mortality — the cleanest comparison (matched person-year units, Grade A)

Deaths are reported in the *same* units by both literatures (per 100,000
person/athlete-years), so no minute conversion is needed. `analysis/output/mortality_peryear.csv`.

| Population | Deaths | Person-years | Rate /100,000 yr (95% CI) |
|---|---|---|---|
| NCAA all-sport exertional SCD | 72 | 9.11M | 0.79 (0.62–1.00) |
| NCAA all-sport heat-illness death | 3 | 4.24M | 0.07 (0.02–0.21) |
| NCAA all-sport sickling death | 10 | 4.24M | 0.24 (0.11–0.43) |
| **NCAA all-sport total exertional death** | — | — | **~1.1** |
| NCAA football non-traumatic death (100% in conditioning) | 34 | 1.29M | 2.65 (1.83–3.70) |
| **Military recruit exercise-related death (1977–2001)** | 141 | 969k | **14.5 (12.2–17.2)** |
| Military recruit non-traumatic sudden death (1977–2001) | 126 | 969k | 13.0 (10.8–15.5) |
| Military recruit EHI death (1977–2001) | 30 | 969k | 3.10 (2.09–4.42) |

**Per person-year, military recruit exertional death (~14.5) is ~5× NCAA football
(2.65) and ~13× NCAA all-sport (~1.1).** But two corrections are essential:
- This military figure is the **1977–2001 regime** (pre-universal-SCT-screening,
  pre-precautions). The modern regime is far safer: USAF BMT 2008–2020 = **1.08 per
  100,000 trainees** (Butler 2023), ≈7× lower.
- Converted to **per training-minute** (recruits train ~3.5× more min/yr), the
  military:NCAA-football death ratio falls to **RR 2.4 (all-MVPA denom)** or 8.1
  (formal-PT denom) — see §4.

Per participant-minute (Monte Carlo): military recruit exercise death (old regime,
all-MVPA) **0.0028/10⁶ min** vs NCAA football conditioning death **0.0012/10⁶ min**
vs NCAA all-sport exertional SCD **0.0005/10⁶ min**.

---

## 4. Key rate ratios (per participant-minute)

`analysis/output/summary.json`; Fig 2. RR > 1 means the military rate is higher
(NCAA safer per minute).

| Comparison | RR (95% CI) | Interpretation |
|---|---|---|
| Mil recruit death (old, all-MVPA) ÷ NCAA football death | **2.4 (1.3–4.1)** | military ~2× per active minute |
| Mil recruit death (old, formal-PT) ÷ NCAA football death | 8.1 (4.4–14.5) | if only PT minutes counted |
| Mil recruit serious morbidity (all-MVPA) ÷ NCAA EHI transport | **1.3 (0.7–2.4)** | indistinguishable |
| Mil recruit serious morbidity (formal-PT) ÷ NCAA EHI transport | 4.3 (2.3–8.4) | if only PT minutes counted |

The confidence intervals cross or approach 1 under the all-MVPA denominator —
the honest statement is that **per active training-minute the two populations are
within a small factor of each other, and which is "higher" depends on the
denominator definition, not on a clear biological difference.**

---

## 5. Table D — Sensitivity (the conclusion does not hinge on one assumption)

`analysis/output/tableD_sensitivity.csv`; Fig 6. Serious-event RR (military ÷ NCAA)
across the pre-specified duration grid:

| NCAA min/AE | Military denom = formal PT | Military denom = all MVPA |
|---|---|---|
| 90 | 3.24 | **0.86** |
| 120 | 4.32 | **1.15** |
| 150 | 5.40 | **1.44** |

**The entire disagreement in the literature is contained in this 6-cell table.**
If you count only formal PT for the military (crediting them the fewest minutes),
military looks 3–5× worse. If you count all measured strenuous activity, the two are
equal (0.86–1.44). No single number is "the" answer; the defensible statement is the
range and its driver.

---

## 6. NCAA sport ranking — is football/lacrosse really the outlier?

`analysis/output/sport_ranking.csv`; Fig 3. EHI per 1,000,000 participant-minutes:

| Rank | Sport | EHI/10⁶ min (95% CI) |
|---|---|---|
| 1 | **Football** | **1.05 (0.83–1.36)** |
| 2 | Women's outdoor track | 0.51 (0.20–1.09) |
| 3 | Men's cross-country | 0.43 (0.11–1.14) |
| 4 | Men's basketball | 0.40 (0.21–0.67) |
| 5 | Men's soccer | 0.34 (0.13–0.80) |
| 6 | Women's soccer | 0.33 (0.14–0.72) |
| 7 | Men's wrestling | 0.26 (0.07–0.69) |
| 8 | **Women's lacrosse** | **0.08 (0.01–0.34)** |

**Football is the unambiguous NCAA exertional-illness outlier** — driven by preseason
(football preseason practice IRR 5.8 vs other periods; hottest-state preseason
practice reaches 92/100,000 AE). By *catastrophic/fatal* exertional events (NCCSIR),
the ranking shifts: **men's basketball has the highest fatal exertional rate (6.34/100,000
athlete-seasons)** — mostly sudden cardiac death — followed by football (3.10),
swimming (2.55), wrestling (2.39). **Lacrosse ranks near the bottom on every metric;
its media prominence is entirely attributable to the 2024 Tufts outbreak (§7), not
to baseline risk.**

---

## 7. Table C — Outbreaks: conditional severity, NOT population incidence

`analysis/output/tableC_outbreaks.csv`; Fig 5. These events were *selected because an
outbreak occurred*; the rates below answer "given that an extreme-conditioning outbreak
happened, how severe was it?" — never "how common is this?"

| Incident | Exposed | Hospitalized | Attack rate | Hosp / 10⁶ workout-min |
|---|---|---|---|---|
| Tufts men's lacrosse 2024 (~250 burpees, 75 min) | 61 | 9 | 0.148 | **1,967** |
| Texas Woman's volleyball 2016 (75 triceps push-ups) | 18 | 8 | 0.444 | — (min NA) |
| Iowa football 2011 (100 back squats) | — | 13 | — | — |
| McMinnville HS football 2010 (shrinking-interval dips) | 43 | 12 | 0.279 | **12,685** |
| Army ROTC "Murph"-type ECP | 44 | 11 | 0.250 | — |
| Navy BUD/S Class 352 Hell Week 2022 | ~35 | 7 (+1 death) | ~0.20 | ~33 |

**Outbreak hospitalization rates (1,967–12,685 per 10⁶ workout-minutes) are 10³–10⁵×
the baseline population rates in Table A (0.03–0.4).** Common signature across the
collegiate clusters: return from a break + a novel/altered workout + eccentric or
upper-body-dominant exercise + a punitive or externally-ranked motivational frame.
Notably, **higher baseline fitness was not protective** in the ROTC cluster.

**Category difference (do not pool):** collegiate clusters are single-team,
single-workout, point-source events; the only systematically enumerated *military*
clusters (Fort Benning) are cross-unit, environmental, hot-day events — in 5 years
there was only one instance of 3 heat-stroke casualties within a single company.

---

## 8. Evidence quality, biases, and what we could not establish

- **Grade A:** mortality comparisons in person-year units; Barnes BCT heat illness
  (observed person-weeks); Yeargin NCAA EHI counts.
- **Grade B:** per-minute conversions using measured activity; MSMR recruit rates
  (derived person-years, cross-validated to <1%).
- **Grade C/D:** NCAA rhabdomyolysis (no denominator exists anywhere — only a census
  of 57 athletes / 9 outbreaks / 51 hospitalized since 2007); BUD/S (news + partial
  investigation); any single-count sport row.

**Ascertainment asymmetries (all bias toward making NCAA look safer):**
- NCAA-ISP is a **convenience sample** (~2–7% of teams/sport) and **structurally
  excludes strength-and-conditioning sessions** — where ~86.6% of NCAA nontraumatic
  football *deaths* occur. The highest-risk NCAA context is outside the surveillance
  frame entirely.
- The ISP under-captures the severe tail by its authors' own admission (1 heat stroke
  in-sample while NCCSIR recorded >15 at non-sample schools).
- Ascertainment intensity alone swings the NCAA football preseason EHI rate ~4×
  (0.365/1,000 AE routine ISP vs 1.52/1,000 AE dedicated study).
- Military surveillance is a near-census with mandatory reportable events — more
  complete capture, especially for field-treated cases.
- Media searches massively over-represent dramatic clusters.

**Data we could not establish (marked NA, never guessed):** any NCAA rhabdomyolysis
incidence rate; NCAA %-time-above-intensity-threshold (blocks a true intensity-matched
denominator); recruit-specific heat inpatient/outpatient split; a modern (post-2001)
all-service recruit mortality series; multi-class BUD/S incidence with denominators.

**Temporal note (Fig 7):** the MSMR 2023 recruit *heat* rates are a denominator
artifact (implied 8,432 recruit-years vs ~23,000 in adjacent years) and are excluded
from trends. The MSMR unit changed from per-1,000 to per-100,000 person-years at the
2022 data year — a 100× trap we handled explicitly. NCAA sickling deaths fell ~88%
after the 2010 SCT-screening bylaw (a clean policy effect); the 2003 acclimatization
bylaw had no measurable effect on heat-stroke deaths.

---

## 9. The ten questions, answered in plain English

**1. Does the average NCAA athlete have a higher or lower serious exertional-event
rate per exercise-minute than a military recruit?**
About the **same order of magnitude**. Per minute of *all* measured strenuous
activity, the rate ratio (military ÷ NCAA) for serious events is **~0.9–1.4** —
statistically indistinguishable. Only if you count military *formal PT minutes alone*
does the military rate rise to ~3–5× NCAA. Directly observed rates put both near
**0.03–0.06 serious events per 1,000,000 participant-minutes**.

**2. Does NCAA football preseason have a higher rate than Army/basic training? By what
factor?**
For *exertional death*, no — basic training (old regime) is ~2–8× higher *per minute*
(and only ~2.4× under the all-activity denominator; modern military is far lower still).
For *non-fatal EHI*, football preseason is intense (up to 92 EHI/100,000 AE in hot
states) and per-minute is comparable to recruit heat illness. Net: **football preseason
and basic training are in the same band; basic training edges higher for the most
serious (fatal) events, by a factor that shrinks from ~5× to ~2× once you count all
the minutes recruits actually train.**

**3. Does NCAA men's lacrosse have a higher rate?** No. Men's lacrosse recorded **zero**
EHI events in 4.9M athlete-exposures (Yeargin) and ranks at the bottom of the
catastrophic-event tables. Its risk profile is **low**; the 2024 Tufts cluster is an
outbreak, not a baseline.

**4. Does NCAA women's lacrosse have a higher rate?** No — women's lacrosse ranks
**last** among sports with any EHI (0.08/10⁶ min; 1 event in 287,622 AE). The only
collegiate lacrosse rhabdomyolysis in the NCCSIR record is a single female
weight-lifting cluster.

**5. Which NCAA sports have the highest exertional-event rates?** For heat illness:
**football** (clear #1), then women's outdoor track, men's cross-country, basketball,
soccer. For fatal/catastrophic exertional events: **men's basketball** (sudden cardiac
death), then football, swimming, wrestling. Football and basketball — **not lacrosse**
— are the true outliers.

**6. Which military training programs have the highest rates?** The **Marine Corps**
(rhabdomyolysis 85–99/100,000 p-yr, ~7× Navy/Air Force; longest course) and, for heat
illness, **Army BCT at Fort Benning** (6.8/10,000 person-weeks, ~4× the coolest sites).
Recruits overall run 6–13× the active-component rate. Among specialized courses,
**BUD/S** is the extreme (see #7).

**7. How does BUD/S compare with NCAA football preseason?** They are not the same kind
of thing. BUD/S Hell Week produces **outbreak-level casualty rates by design** —
Class 352 (2022) had ~7 of ~35 remaining candidates hospitalized (attack rate ~0.20)
plus one death, comparable to a *collegiate rhabdomyolysis outbreak* (Tufts 0.148),
and **orders of magnitude above** football preseason's baseline. BUD/S should be
compared to NCAA "hell week" clusters, not to normal football preseason. (Grade C —
BUD/S data are news + partial investigation.)

**8. Are highly publicized NCAA "hell week" hospital clusters representative of baseline
NCAA risk?** **No.** They are rare extreme outliers: outbreak hospitalization rates run
**1,000–13,000 per 10⁶ workout-minutes vs 0.03–0.4 at baseline** — a 10³–10⁵× gap.
They are selected because an outbreak occurred and cannot be read as population incidence.

**9. Are extreme-conditioning outbreaks more common in collegiate sports than in military
training, or merely more visible?** Mostly **more visible**. Only 2 of 12 collegiate
clusters reached peer review; the rest are news/litigation/press-release. Military
clusters are routinely surveilled (MSMR) but are a *different phenomenon* (cross-unit,
environmental). The apparent collegiate predominance is largely a **publication/media
artifact**, not established higher incidence — though the recurring collegiate pattern
(post-break novel punitive workouts) is a real, preventable hazard.

**10. What comparison can be stated with the greatest confidence?** The **mortality
comparison in matched person-year units** (Grade A, no minute conversion): military
recruit exertional death **~14.5/100,000 recruit-years (1977–2001)** vs NCAA football
non-traumatic death **2.65/100,000 player-years** vs NCAA all-sport exertional death
**~1.1/100,000 athlete-years**. Equally confident, and the paper's central message:
**once exposure is normalized to actual training-minutes, the gap between the two
populations is far smaller than raw comparisons imply — on the order of 1–5×, not
10–100×.**

---

## 10. Reproducibility

Every derived number gives numerator, denominator, unit, duration-assumption source,
and equation in `analysis/` and `sources/source_ledger.md`. Re-run:

```
pip install numpy scipy pandas matplotlib statsmodels
python3 analysis/run_analysis.py     # tables -> analysis/output/
python3 analysis/make_figures.py     # figures -> figures/
```

Datasets: `data/master_dataset.csv` (surveillance), `data/outbreaks.csv` (clusters),
`data/exposure_durations.csv` (minute conversions). Unestablished values are `NA`.
