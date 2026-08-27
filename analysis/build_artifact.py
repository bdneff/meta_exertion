"""Build the self-contained HTML artifact with embedded figures."""
import base64, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG=os.path.join(ROOT,"figures")
def img(name):
    b=base64.b64encode(open(os.path.join(FIG,name+".png"),"rb").read()).decode()
    return f"data:image/png;base64,{b}"

F1,F2,F3,F4,F5,F6,F7=(img("fig1_forest_incidence"),img("fig2_forest_RR"),
    img("fig3_sport_ranking"),img("fig4_military_ranking"),img("fig5_outbreak_logscale"),
    img("fig6_sensitivity"),img("fig7_temporal"))

HTML=f"""<title>Per-Minute Exertional Risk</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,600;0,700;1,400&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{{
  --paper:#f7f6f3; --surface:#ffffff; --ink:#1a1d24; --muted:#5a6070;
  --line:#e2e0d8; --line-strong:#c9c6ba;
  --ncaa:#2b6cb0; --ncaa-deep:#1a4971; --ncaa-soft:#e5eef7;
  --mil:#c05621; --mil-deep:#8a3d12; --mil-soft:#f6e9df;
  --equal:#2f855a; --equal-soft:#e4f0e9;
  --shadow:0 1px 2px rgba(26,29,36,.06),0 8px 24px rgba(26,29,36,.05);
}}
:root:not([data-theme="light"]) {{}}
@media (prefers-color-scheme: dark){{
  :root:not([data-theme="light"]){{
    --paper:#14161c; --surface:#1c1f28; --ink:#eceef3; --muted:#9aa1b2;
    --line:#2b2f3a; --line-strong:#3a3f4d;
    --ncaa:#6aa5df; --ncaa-deep:#9cc3ec; --ncaa-soft:#1e2a3a;
    --mil:#e08a54; --mil-deep:#f0a877; --mil-soft:#33231a;
    --equal:#68b98c; --equal-soft:#1c2c24;
    --shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px rgba(0,0,0,.35);
  }}
}}
:root[data-theme="dark"]{{
  --paper:#14161c; --surface:#1c1f28; --ink:#eceef3; --muted:#9aa1b2;
  --line:#2b2f3a; --line-strong:#3a3f4d;
  --ncaa:#6aa5df; --ncaa-deep:#9cc3ec; --ncaa-soft:#1e2a3a;
  --mil:#e08a54; --mil-deep:#f0a877; --mil-soft:#33231a;
  --equal:#68b98c; --equal-soft:#1c2c24;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px rgba(0,0,0,.35);
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);
  font-family:"IBM Plex Sans",system-ui,sans-serif;line-height:1.6;
  -webkit-font-smoothing:antialiased}}
.wrap{{max-width:940px;margin:0 auto;padding:0 24px}}
.measure{{max-width:66ch}}
h1,h2,h3{{font-family:"Spectral",Georgia,serif;text-wrap:balance;line-height:1.15}}
.eyebrow{{font-family:"IBM Plex Mono",monospace;font-size:.72rem;letter-spacing:.16em;
  text-transform:uppercase;color:var(--mil-deep);margin:0 0 14px}}
/* hero */
header{{border-bottom:1px solid var(--line);background:
  linear-gradient(180deg,var(--surface),var(--paper))}}
.hero{{padding:64px 0 46px}}
.hero h1{{font-size:clamp(2.1rem,5vw,3.4rem);font-weight:700;margin:0 0 20px;letter-spacing:-.01em}}
.hero h1 em{{font-style:italic;color:var(--ncaa-deep)}}
.lede{{font-size:1.2rem;color:var(--muted);max-width:60ch;margin:0}}
.lede strong{{color:var(--ink);font-weight:600}}
/* verdict band */
.verdict{{display:flex;flex-wrap:wrap;gap:2px;margin:34px 0 0;border-radius:12px;overflow:hidden;
  box-shadow:var(--shadow)}}
.vcell{{flex:1 1 200px;padding:20px 22px;background:var(--surface)}}
.vcell .n{{font-family:"IBM Plex Mono",monospace;font-size:1.9rem;font-weight:500;display:block;letter-spacing:-.02em}}
.vcell .k{{font-size:.82rem;color:var(--muted);margin-top:4px;display:block}}
.vcell.a .n{{color:var(--ncaa-deep)}} .vcell.b .n{{color:var(--mil-deep)}} .vcell.c .n{{color:var(--equal)}}
/* sections */
section{{padding:52px 0}}
section+section{{border-top:1px solid var(--line)}}
h2{{font-size:1.75rem;font-weight:600;margin:0 0 8px;letter-spacing:-.01em}}
.sub{{color:var(--muted);margin:0 0 26px;font-size:1.02rem}}
p{{margin:0 0 16px}}
.key{{background:var(--ncaa-soft);border-left:3px solid var(--ncaa);padding:16px 20px;
  border-radius:0 8px 8px 0;margin:22px 0}}
.key.mil{{background:var(--mil-soft);border-left-color:var(--mil)}}
.key.eq{{background:var(--equal-soft);border-left-color:var(--equal)}}
.key p{{margin:0}}
/* tables */
.tw{{overflow-x:auto;margin:22px 0;border:1px solid var(--line);border-radius:10px;box-shadow:var(--shadow)}}
table{{border-collapse:collapse;width:100%;font-size:.9rem;background:var(--surface)}}
caption{{caption-side:top;text-align:left;font-size:.8rem;color:var(--muted);padding:12px 16px;font-family:"IBM Plex Mono",monospace}}
th,td{{padding:10px 14px;text-align:left;border-bottom:1px solid var(--line)}}
thead th{{background:var(--paper);font-weight:600;font-size:.78rem;letter-spacing:.03em;
  text-transform:uppercase;color:var(--muted);white-space:nowrap}}
tbody tr:last-child td{{border-bottom:none}}
td.num,th.num{{font-family:"IBM Plex Mono",monospace;font-variant-numeric:tabular-nums;text-align:right;white-space:nowrap}}
.tag{{display:inline-block;font-family:"IBM Plex Mono",monospace;font-size:.7rem;padding:1px 7px;border-radius:20px;font-weight:500}}
.tag.ncaa{{background:var(--ncaa-soft);color:var(--ncaa-deep)}}
.tag.mil{{background:var(--mil-soft);color:var(--mil-deep)}}
.tag.g{{background:var(--paper);color:var(--muted);border:1px solid var(--line-strong)}}
tr.mil td:first-child{{box-shadow:inset 3px 0 var(--mil)}}
tr.ncaa td:first-child{{box-shadow:inset 3px 0 var(--ncaa)}}
/* figure */
figure{{margin:26px 0;background:var(--surface);border:1px solid var(--line);border-radius:10px;
  padding:16px;box-shadow:var(--shadow)}}
figure img{{width:100%;height:auto;display:block;border-radius:4px}}
figcaption{{font-size:.82rem;color:var(--muted);margin-top:12px;font-family:"IBM Plex Sans",sans-serif}}
/* sensitivity grid highlight */
.grid6{{display:grid;grid-template-columns:auto repeat(2,1fr);gap:2px;background:var(--line);
  border-radius:10px;overflow:hidden;margin:22px 0;box-shadow:var(--shadow);font-family:"IBM Plex Mono",monospace}}
.grid6 div{{background:var(--surface);padding:14px 16px;font-size:.9rem;font-variant-numeric:tabular-nums}}
.grid6 .h{{background:var(--paper);font-weight:600;font-size:.74rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);font-family:"IBM Plex Sans",sans-serif}}
.grid6 .hi{{background:var(--equal-soft);color:var(--equal);font-weight:600}}
.grid6 .lo{{background:var(--mil-soft);color:var(--mil-deep);font-weight:600}}
/* Q&A */
.qa{{border-top:1px solid var(--line);padding:22px 0}}
.qa:first-of-type{{border-top:none}}
.qa .q{{font-family:"Spectral",serif;font-weight:600;font-size:1.12rem;margin:0 0 8px;display:flex;gap:12px}}
.qa .q .no{{font-family:"IBM Plex Mono",monospace;color:var(--mil-deep);font-size:.95rem;flex:none;padding-top:2px}}
.qa .a{{margin:0 0 0 34px;color:var(--ink)}}
.qa .a b{{color:var(--ncaa-deep)}}
/* footer */
footer{{border-top:1px solid var(--line);padding:40px 0 60px;color:var(--muted);font-size:.86rem}}
footer code{{font-family:"IBM Plex Mono",monospace;background:var(--surface);padding:2px 6px;border-radius:4px;border:1px solid var(--line)}}
.grades{{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0}}
.grade{{font-family:"IBM Plex Mono",monospace;font-size:.78rem;padding:6px 12px;border-radius:8px;background:var(--surface);border:1px solid var(--line)}}
.grade b{{color:var(--ink)}}
@media (max-width:560px){{.hero{{padding:44px 0 32px}} .qa .a{{margin-left:0}} .vcell .n{{font-size:1.5rem}}}}
</style>

<header><div class="wrap hero">
  <p class="eyebrow">Systematic review &amp; quantitative synthesis</p>
  <h1>NCAA athletes and military recruits get hurt at <em>similar rates per minute</em> of hard training</h1>
  <p class="lede">Raw comparisons make basic training look an order of magnitude more dangerous than
  college sport. But recruits train roughly <strong>3–4× more minutes per year</strong>. Normalize to
  actual training-minutes and the gap collapses to a factor of one to five — and under the most
  defensible denominator, the two are <strong>statistically indistinguishable</strong>.</p>
  <div class="verdict">
    <div class="vcell c"><span class="n">0.9–1.4×</span><span class="k">Military ÷ NCAA serious-event rate ratio, per minute of all strenuous activity — CI spans 1</span></div>
    <div class="vcell a"><span class="n">Football</span><span class="k">The one true NCAA exertional-illness outlier — not lacrosse</span></div>
    <div class="vcell b"><span class="n">10³–10⁵×</span><span class="k">How far "hell week" outbreak clusters sit above either baseline</span></div>
  </div>
</div></header>

<main class="wrap">

<section>
  <h2>The denominator is the whole argument</h2>
  <p class="sub">Two surveillance systems, two incompatible yardsticks.</p>
  <div class="measure">
  <p>NCAA injury surveillance counts <strong>athlete-exposures</strong> — one athlete in one practice or
  game. U.S. military surveillance counts <strong>person-years</strong>. Neither is training-minutes, and
  comparing them directly is the mistake that produces every scary headline. This review converts both,
  with propagated uncertainty, to <strong>events per 1,000,000 participant-minutes of strenuous
  training</strong>.</p>
  <p>The pivotal fact is exposure intensity, not danger. A recruit trains nearly full-time for the length
  of their course; a collegiate athlete trains part-time and seasonally. Measured accelerometry puts an
  Army recruit at ~180 minutes of moderate-to-vigorous activity <em>per day</em>; a football practice
  averages 142 minutes total, most of it standing. So a recruit-year holds ~57,000 strenuous minutes
  against ~16,000–21,000 for an athlete-year.</p>
  </div>
  <div class="key eq"><p><strong>Consequence:</strong> a per-person-year death ratio of ~13× (military
  vs NCAA all-sport) becomes ~2–5× per training-minute — and for non-fatal serious events, ~1×. The
  minutes, not the medicine, drove the apparent gap.</p></div>
  <div class="key mil"><p><strong>Two caveats, both making NCAA look <em>safer</em> than it is:</strong>
  military minutes exclude idle time; NCAA session minutes include it (no NCAA sport publishes intensity
  fractions). And schedule-based military estimates undercount badly — the Marine POI lists 46 miles of
  running; recruits actually cover 658 (Kloss 2024). We use measured activity throughout. Our
  "NCAA is comparable" conclusions are therefore conservative.</p></div>
</section>

<section>
  <h2>Primary comparison</h2>
  <p class="sub">Serious acute non-traumatic exertional events — hospitalization or urgent transport — per 1,000,000 participant-minutes.</p>
  <div class="tw"><table>
    <caption>TABLE A · point estimate at central minutes; 95% CI includes duration + Poisson uncertainty (Monte Carlo)</caption>
    <thead><tr><th>Population</th><th class="num">Events</th><th>Denominator</th><th class="num">Per 10⁶ min (95% CI)</th><th>Grade</th></tr></thead>
    <tbody>
      <tr class="ncaa"><td>NCAA all-sports — EHI emergency transport</td><td class="num">19</td><td>4.91M AE × session-min</td><td class="num">0.033 (0.019–0.055)</td><td><span class="tag g">B</span></td></tr>
      <tr class="ncaa"><td>NCAA football — EHI emergency transport</td><td class="num">9</td><td>1.12M AE × session-min</td><td class="num">0.056 (0.026–0.104)</td><td><span class="tag g">B</span></td></tr>
      <tr class="mil"><td>Military recruit — heat stroke + rhabdo-hosp <em>(all activity)</em></td><td class="num">49</td><td>23,150 recruit-yr × MVPA</td><td class="num">0.041 (0.029–0.057)</td><td><span class="tag g">B</span></td></tr>
      <tr class="mil"><td>Military recruit — heat stroke + rhabdo-hosp <em>(formal PT only)</em></td><td class="num">49</td><td>23,150 recruit-yr × PT-min</td><td class="num">0.140 (0.096–0.205)</td><td><span class="tag g">B</span></td></tr>
      <tr class="mil"><td>Army BCT — <em>all</em> heat illness (observed person-weeks)</td><td class="num">1210</td><td>3.36M p-wk × MVPA</td><td class="num">0.36 (0.30–0.44)</td><td><span class="tag g">A</span></td></tr>
    </tbody>
  </table></div>
  <p>For the serious endpoint, NCAA (0.033–0.056) and military recruits (0.041, all-activity denominator)
  overlap. The military rate exceeds NCAA only when credited with formal-PT minutes alone.</p>
  <figure><img alt="Forest plot of serious exertional-event incidence per participant-minute" src="{F1}">
    <figcaption>Fig 1 · Serious exertional-event incidence per participant-minute. NCAA (blue) and
    military recruit (orange) point estimates overlap; whiskers carry duration + count uncertainty. Log x-axis.</figcaption></figure>
</section>

<section>
  <h2>The answer lives in six cells</h2>
  <p class="sub">Sensitivity of the military ÷ NCAA serious-event rate ratio to the exposure-minute assumptions.</p>
  <div class="grid6">
    <div class="h">NCAA min / exposure</div><div class="h">Military = formal PT only</div><div class="h">Military = all strenuous activity</div>
    <div class="h">90</div><div class="lo">3.24×</div><div class="hi">0.86×</div>
    <div class="h">120</div><div class="lo">4.32×</div><div class="hi">1.15×</div>
    <div class="h">150</div><div class="lo">5.40×</div><div class="hi">1.44×</div>
  </div>
  <p>The entire dispute reduces to one choice: count only the military's formal PT sessions (they look
  3–5× worse) or count all the strenuous activity they actually perform (the two populations are equal).
  There is no single "right" number — the honest result is the range and its driver.</p>
  <figure><img alt="Line plot of rate ratio versus assumed NCAA minutes for two military denominators" src="{F6}">
    <figcaption>Fig 6 · The rust line (formal-PT denominator) sits well above parity; the blue line
    (all measured activity) hugs 1.0. Which line you believe is a denominator choice, not a finding.</figcaption></figure>
</section>

<section>
  <h2>Mortality — the cleanest comparison</h2>
  <p class="sub">Deaths are reported in matched person-year units by both literatures, so no minute conversion is needed. Grade A.</p>
  <div class="tw"><table>
    <caption>TABLE (mortality) · exertional / non-traumatic death, per 100,000 person or athlete-years</caption>
    <thead><tr><th>Population</th><th class="num">Deaths</th><th class="num">Person-years</th><th class="num">Rate /100k yr (95% CI)</th></tr></thead>
    <tbody>
      <tr class="ncaa"><td>NCAA all-sport exertional sudden cardiac death</td><td class="num">72</td><td class="num">9.11M</td><td class="num">0.79 (0.62–1.00)</td></tr>
      <tr class="ncaa"><td>NCAA all-sport total exertional death (approx)</td><td class="num">—</td><td class="num">—</td><td class="num">~1.1</td></tr>
      <tr class="ncaa"><td>NCAA football non-traumatic death (100% in conditioning)</td><td class="num">34</td><td class="num">1.29M</td><td class="num">2.65 (1.83–3.70)</td></tr>
      <tr class="mil"><td>Military recruit exercise-related death <em>(1977–2001)</em></td><td class="num">141</td><td class="num">969k</td><td class="num">14.5 (12.2–17.2)</td></tr>
      <tr class="mil"><td>Military recruit exertional heat-illness death <em>(1977–2001)</em></td><td class="num">30</td><td class="num">969k</td><td class="num">3.10 (2.09–4.42)</td></tr>
      <tr class="mil"><td>USAF basic training death <em>(2008–2020, modern regime)</em></td><td class="num">5</td><td class="num">463k acc.</td><td class="num">1.08 /100k trainees</td></tr>
    </tbody>
  </table></div>
  <p>Per person-year, old-regime recruit death (~14.5) is ~5× NCAA football and ~13× NCAA all-sport.
  But that figure predates universal sickle-cell screening and heat precautions; the modern regime is
  ~7× lower. And per training-minute the recruit-vs-football death ratio falls to
  <strong>2.4× (all-activity)</strong> or 8× (formal-PT).</p>
</section>

<section>
  <h2>Is football — or lacrosse — the real outlier?</h2>
  <p class="sub">NCAA exertional heat illness per 1,000,000 participant-minutes.</p>
  <p>Football is the unambiguous NCAA heat-illness outlier, driven by preseason (rate ratio 5.8 vs other
  periods; up to 92 per 100,000 exposures in the hottest states). <strong>Lacrosse ranks near the
  bottom</strong> — men's lacrosse logged zero heat-illness events in 4.9 million exposures. Its
  reputation is a single 2024 outbreak, not baseline risk. On <em>fatal</em> exertional events, men's
  basketball leads (sudden cardiac death), then football, swimming, wrestling.</p>
  <figure><img alt="Bar chart ranking NCAA sports by heat illness per participant-minute" src="{F3}">
    <figcaption>Fig 3 · Football's per-minute EHI rate is 2–13× every other sport. Women's lacrosse ranks last.</figcaption></figure>
  <figure><img alt="Bar chart of military recruit heat illness by BCT installation" src="{F4}">
    <figcaption>Fig 4 · Among recruits, Fort Benning runs ~4× the coolest Army BCT sites (Barnes 2019, observed person-weeks).</figcaption></figure>
</section>

<section>
  <h2>Outbreaks are conditional severity, not incidence</h2>
  <p class="sub">These clusters entered the record <em>because</em> an outbreak occurred. They answer "how severe was it?" — never "how common is this?"</p>
  <div class="tw"><table>
    <caption>TABLE C · extreme-conditioning clusters — selected on outcome, not comparable to population rates</caption>
    <thead><tr><th>Incident</th><th class="num">Exposed</th><th class="num">Hospitalized</th><th class="num">Attack rate</th><th class="num">Hosp / 10⁶ workout-min</th></tr></thead>
    <tbody>
      <tr class="ncaa"><td>Tufts men's lacrosse 2024 · ~250 burpees, 75 min</td><td class="num">61</td><td class="num">9</td><td class="num">0.148</td><td class="num">1,967</td></tr>
      <tr class="ncaa"><td>Texas Woman's volleyball 2016 · 75 triceps push-ups</td><td class="num">18</td><td class="num">8</td><td class="num">0.444</td><td class="num">—</td></tr>
      <tr class="ncaa"><td>Iowa football 2011 · 100 back squats</td><td class="num">—</td><td class="num">13</td><td class="num">—</td><td class="num">—</td></tr>
      <tr class="mil"><td>Army ROTC "Murph"-type extreme-conditioning</td><td class="num">44</td><td class="num">11</td><td class="num">0.250</td><td class="num">—</td></tr>
      <tr class="mil"><td>Navy BUD/S Class 352 Hell Week 2022</td><td class="num">~35</td><td class="num">7 +1 death</td><td class="num">~0.20</td><td class="num">~33</td></tr>
    </tbody>
  </table></div>
  <p>Outbreak hospitalization rates (≈2,000–13,000 per 10⁶ workout-minutes) sit 10³–10⁵× above the
  baseline rates in Table A. The collegiate signature recurs: return from a break, a novel or punitive
  workout, eccentric or upper-body-dominant exercise. Notably, BUD/S Hell Week produces
  outbreak-level casualty rates <em>by design</em> — it belongs beside collegiate "hell week" clusters,
  not beside ordinary football preseason.</p>
  <figure><img alt="Log-scale plot of outbreak rates against the baseline band" src="{F5}">
    <figcaption>Fig 5 · Every outbreak (red) sits far above the shaded baseline band. Note the log y-axis.</figcaption></figure>
</section>

<section>
  <h2>Ten questions, answered</h2>
  <p class="sub">Numbers where the evidence permits; the direction of each answer is robust to the assumptions.</p>
  <div class="qa"><p class="q"><span class="no">1</span>Average NCAA athlete vs military recruit, per exercise-minute?</p>
    <p class="a">Same order of magnitude. Serious-event rate ratio <b>≈0.9–1.4×</b> per minute of all strenuous activity — indistinguishable; only "formal-PT-only" accounting pushes it to 3–5×.</p></div>
  <div class="qa"><p class="q"><span class="no">2</span>Football preseason vs basic training?</p>
    <p class="a">Same band. Basic training edges higher for fatal events, by a factor that shrinks from ~5× to <b>~2×</b> once all recruit training-minutes are counted; comparable for non-fatal heat illness.</p></div>
  <div class="qa"><p class="q"><span class="no">3</span>Men's lacrosse — higher risk?</p>
    <p class="a"><b>No.</b> Zero heat-illness events in 4.9M exposures; bottom of the catastrophic tables. The 2024 Tufts cluster is an outbreak, not a baseline.</p></div>
  <div class="qa"><p class="q"><span class="no">4</span>Women's lacrosse — higher risk?</p>
    <p class="a"><b>No — it ranks last</b> among sports with any heat illness (0.08 per 10⁶ min; 1 event in 287,622 exposures).</p></div>
  <div class="qa"><p class="q"><span class="no">5</span>Highest-risk NCAA sports?</p>
    <p class="a">Heat illness: <b>football</b>, then women's outdoor track, men's cross-country, basketball. Fatal exertional events: <b>men's basketball</b> (cardiac), then football, swimming, wrestling. Not lacrosse.</p></div>
  <div class="qa"><p class="q"><span class="no">6</span>Highest-risk military programs?</p>
    <p class="a">The <b>Marine Corps</b> (rhabdomyolysis ~7× Navy/Air Force) and, for heat, <b>Army BCT at Fort Benning</b>. Recruits overall run 6–13× the active-component rate.</p></div>
  <div class="qa"><p class="q"><span class="no">7</span>BUD/S vs football preseason?</p>
    <p class="a">Not comparable. BUD/S Hell Week generates <b>outbreak-level</b> casualty rates by design (~20% hospitalized in Class 352 plus a death) — orders of magnitude above football-preseason baseline. Compare it to NCAA "hell week" clusters.</p></div>
  <div class="qa"><p class="q"><span class="no">8</span>Are NCAA "hell week" clusters representative of baseline?</p>
    <p class="a"><b>No — rare extreme outliers.</b> Outbreak hospitalization rates run 10³–10⁵× baseline. Selected on outcome; not population incidence.</p></div>
  <div class="qa"><p class="q"><span class="no">9</span>More outbreaks in college than military — or just more visible?</p>
    <p class="a">Mostly <b>more visible.</b> Only 2 of 12 collegiate clusters reached peer review; military clusters are surveilled but a different (environmental, cross-unit) phenomenon. Largely a media/publication artifact.</p></div>
  <div class="qa"><p class="q"><span class="no">10</span>Most confident statement?</p>
    <p class="a">The mortality comparison in matched person-year units (Grade A), and the central message: <b>once exposure is normalized to training-minutes, the gap is 1–5×, not 10–100×.</b></p></div>
</section>

</main>

<footer><div class="wrap">
  <p><strong>Evidence grading</strong> — C/D estimates are shown with wider intervals and never the apparent precision of A/B.</p>
  <div class="grades">
    <span class="grade"><b>A</b> Direct — observed events, observed comparable denominator</span>
    <span class="grade"><b>B</b> Strong reconstruction — denominator from measured duration data</span>
    <span class="grade"><b>C</b> Moderate — one component from supported assumptions</span>
    <span class="grade"><b>D</b> Weak — major denominator/endpoint uncertainty</span>
  </div>
  <p>Anchor sources (all traced in the source ledger): NCAA-ISP exertional heat illness (Yeargin 2019),
  NCCSIR / Boden / Harmon–Petek catastrophic &amp; sudden-death registries, MSMR exertional
  rhabdomyolysis &amp; heat-illness surveillance (2020–2025), Barnes 2019 Army BCT (observed person-weeks),
  Scoville / Borden &amp; Eckart recruit mortality, and measured activity studies (Alemany, McAdam, Kloss).
  Key limitations: NCAA-ISP is a convenience sample that excludes the strength-and-conditioning window
  where most NCAA exertional deaths occur; military 1977–2001 mortality predates modern precautions;
  no NCAA rhabdomyolysis incidence rate exists in the literature; military MVPA excludes idle time while
  NCAA session minutes include it.</p>
  <p>Reproduce: <code>python3 analysis/run_analysis.py</code> · <code>python3 analysis/make_figures.py</code>.
  Full dataset, code, source ledger and the 20-section report accompany this summary. Values that could
  not be established are marked <code>NA</code>, never guessed.</p>
</div></footer>
"""
open(os.path.join(ROOT,"report.html"),"w").write(HTML)
print("wrote report.html", len(HTML), "bytes")
