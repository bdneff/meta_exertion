# Methods — Systematic Review & Quantitative Synthesis of Acute Exertional Medical Events in NCAA Athletes vs U.S. Military Trainees

## 1. Objective and question
Estimate the incidence of **serious acute non-traumatic exertional medical
events** (requiring hospitalization or urgent emergency transport) per unit of
**actual strenuous-training exposure** in NCAA athletes and U.S. military
trainees, normalized to **events per 1,000,000 participant-minutes of strenuous
physical training**, and determine which populations have the highest risk. The
question is directional-neutral: we let the data decide, not the media.

## 2. Design
Systematic review with structured quantitative synthesis and, where
statistically defensible, random-effects meta-analytic pooling. Because the two
populations are measured in fundamentally different exposure units
(athlete-exposures vs person-years), the core methodological work is a
transparent, uncertainty-propagating conversion of both to participant-minutes.

## 3. Populations (pre-specified strata)
- **NCAA:** all sports combined; football; men's lacrosse; women's lacrosse;
  combined lacrosse; wrestling; soccer (M/W); cross-country; track & field;
  basketball (M/W); swimming; rowing; plus any emergent outlier sport.
  Phases: preseason, in-season practice, competition, offseason/S&C, first days
  back from break, acclimatization, "extreme conditioning" punishment sessions.
- **Military:** Army Basic Combat Training (BCT); Marine Corps Recruit Training;
  Navy Recruit Training (RTC Great Lakes); Air Force Basic Military Training
  (BMT); an aggregated **initial-entry/basic-training** category; specialized
  courses — Navy BUD/S, Ranger School, OCS/ROTC, service academies — analyzed
  separately. Active-component general population kept separate from recruits.

## 4. Endpoints
- **Primary:** serious acute non-traumatic exertional event requiring inpatient
  hospitalization OR urgent emergency transport. Sub-classified where possible
  into (a) inpatient hospitalization, (b) ED/EMS without confirmed admission,
  (c) combined when inseparable.
- **Secondary:** all exertional heat illness; exertional rhabdomyolysis; heat
  stroke; heat exhaustion; EMS transport; hospitalization; exertional death;
  catastrophic non-traumatic events. Sudden cardiac arrest/death reported
  separately (exertion-associated but distinct etiology).
- **Excluded from primary:** traumatic injuries (fractures, ACL, concussion,
  collisions).

## 5. Search
Sources: NCAA-ISP/Datalys publications, NCAA Sport Science Institute, NCCSIR
annual reports, PubMed/PMC, Google Scholar; DHA/Armed Forces Health Surveillance
Division MSMR, Army Public Health Center, military-medicine journals, official
training schedules/doctrine, and documented outbreak investigations. Terms
included exertional (heat) illness/heat stroke/heat exhaustion, (exertional)
rhabdomyolysis, exercise-associated collapse/sickling/hyponatremia, nontraumatic
catastrophic injury, conditioning death, recruit/basic/initial-entry training,
BUD/S, and sport/phase qualifiers. References followed backward and forward. News
used only to *locate* incidents, then traced to medical/official primary sources.

## 6. Data extraction & master dataset
A machine-readable master table (`data/master_dataset.csv`) captures, per row:
source ID, year(s), institution/service, population, sport/program, sex,
division, phase, participants, athlete/recruit exposures, person-days/-weeks/
-years, estimated participant-minutes, event type, diagnosis-specific counts,
hospitalizations, ED visits, transports, fatalities, workout description &
duration, environment, source's original rate, denominator type (observed vs
reconstructed), assumptions, quality grade, notes. Separate tables:
population surveillance, outbreaks/clusters, exposure-duration estimates.

## 7. Denominator normalization (core method)
Rates are converted to **events per 1,000,000 participant-minutes of strenuous
training**. We never treat athlete-exposures, recruit-weeks, and person-years as
interchangeable.

**NCAA:** participant-minutes = athlete-exposures × mean strenuous minutes per
exposure, using empirical practice/competition-duration literature per sport and
phase (practice and competition handled separately when durations differ).
- *NCAA denominator A* — full observed practice/conditioning duration.
- *NCAA denominator B* — high-exertion portion only (fraction of session at
  substantial exertion), where data allow.

**Military:** participant-minutes = person-time × minutes/day of strenuous
activity, estimated from doctrine (FM 7-22), measured activity studies
(accelerometry/HR/DLW), and official schedules — NOT all calendar minutes.
- *Military denominator A* — formal PT periods only (conservative → high risk
  per minute).
- *Military denominator B* — all strenuous activity (PT + rucking + field +
  obstacle/confidence courses + combatives).

Every reconstruction is labeled and every duration traces to a cited source. No
durations are invented.

## 8. Uncertainty propagation & sensitivity
For any rate needing an estimated duration, uncertainty in minutes/exposure is
propagated by Monte Carlo (uniform over the cited plausible range) jointly with
Poisson uncertainty in the event count (Gamma(count+0.5) posterior). Rate ratios
are computed by the same Monte Carlo so the CI reflects both duration and count
error. Pre-specified duration grids (e.g. football 90/120/150/180 min; military
formal-PT-only / 2 / 4 / 6 h/day) drive a sensitivity table showing how each key
conclusion moves. A conclusion is reported as robust only if it holds across the
grid.

## 9. Statistical methods
- Single rates: exact (Garwood) Poisson 95% CI.
- Rate ratios: exact conditional-Poisson (binomial) 95% CI, plus Monte-Carlo CI
  when exposures are reconstructed.
- Pooling: random-effects DerSimonian-Laird on the log-rate scale, reported with
  I², Q, τ², events, exposure, k studies, and prediction intervals (k≥3). For
  rare events we stay on the Poisson/log scale, never a normal approximation to
  raw rates. Pooling is performed only within sufficiently homogeneous strata; a
  pooled estimate is not manufactured merely because the project is a
  "meta-analysis." Where pooling is inappropriate, a structured quantitative
  synthesis is reported instead.

## 10. Outbreak analysis (separate)
Team/unit clusters are analyzed as **conditional severity**, never as population
incidence. For each: participants exposed, ill, hospitalized; workout & minutes;
prior-training/return-from-break status; environment. We report
attack rate = hospitalized / exposed, and R = hospitalizations /
(participants × workout-minutes) × 10⁶, with the explicit caveat that these are
selected-on-outcome and not comparable to baseline incidence.

## 11. Evidence grading
- **A — Direct:** observed events, observed comparable denominator.
- **B — Strong reconstruction:** observed events, denominator converted with
  high-quality empirical duration data.
- **C — Moderate reconstruction:** one denominator component from reasonable
  assumptions.
- **D — Weak:** major denominator or endpoint uncertainty.
C/D estimates are shown with wide intervals and ≤2 significant figures.

## 12. Bias & ascertainment (addressed in Discussion)
NCAA-ISP is a non-universal convenience sample; catastrophic registries capture
severe better than mild; military surveillance has near-universal healthcare
capture but coding limits; hospitalization thresholds differ; AE and person-time
differ fundamentally; media over-represents clusters; rhabdo reporting varies;
military administrative capture may exceed collegiate; out-of-team conditioning
is undercounted.

## 13. Reproducibility
All calculations are programmatic (`analysis/`), every derived number gives
numerator, denominator, unit conversion, duration-assumption source, equation,
and value. The master dataset is CSV; the source ledger links each row to a
publication/table. Unestablished values are `NA`, never guessed.
