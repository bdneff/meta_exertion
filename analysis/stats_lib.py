"""
Core statistical utilities for the NCAA vs Military exertional-events meta-analysis.

All rate math is Poisson-based (events are rare). Confidence intervals for a
single count use the exact (Garwood) Poisson interval. Rate ratios use the
exact conditional-binomial method. Pooling uses a random-effects model on the
log-rate scale (DerSimonian-Laird). Participant-minute conversions propagate
duration uncertainty by Monte Carlo.

No data are hard-coded here; this is a pure library imported by the analysis
scripts.
"""

import numpy as np
from scipy import stats


# ---------------------------------------------------------------------------
# Single-rate exact Poisson confidence interval
# ---------------------------------------------------------------------------
def poisson_ci(count, exposure, per=1_000_000, alpha=0.05):
    """
    Exact (Garwood) Poisson CI for a rate = count / exposure, scaled to `per`
    units of exposure.

    Returns (rate, lo, hi) in events per `per` exposure units.
    For count == 0 the lower limit is 0 and the upper uses the chi-square rule.
    """
    count = float(count)
    if exposure <= 0:
        return (np.nan, np.nan, np.nan)
    rate = count / exposure * per
    if count == 0:
        lo = 0.0
        hi = stats.chi2.ppf(1 - alpha / 2, 2 * (count + 1)) / 2 / exposure * per
        return (rate, lo, hi)
    lo = stats.chi2.ppf(alpha / 2, 2 * count) / 2 / exposure * per
    hi = stats.chi2.ppf(1 - alpha / 2, 2 * (count + 1)) / 2 / exposure * per
    return (rate, lo, hi)


# ---------------------------------------------------------------------------
# Rate ratio (two independent Poisson counts) — exact conditional method
# ---------------------------------------------------------------------------
def rate_ratio(c1, e1, c2, e2, alpha=0.05):
    """
    Rate ratio (rate1 / rate2) with exact conditional-Poisson 95% CI.

    c1,e1 = numerator group count & exposure; c2,e2 = denominator group.
    Exposure units must be identical between the two groups (e.g. both in
    participant-minutes). Returns (rr, lo, hi).
    Uses the binomial-proportion method of exact conditional inference:
    given c1+c2, c1 ~ Binom(n, p) with p/(1-p) = (e1/e2)*RR.
    """
    c1, c2 = float(c1), float(c2)
    if c1 == 0 and c2 == 0:
        return (np.nan, np.nan, np.nan)
    r1 = c1 / e1
    r2 = c2 / e2
    rr = r1 / r2 if r2 > 0 else np.inf
    n = c1 + c2
    # exact CI on p via Clopper-Pearson, then transform to RR
    if c1 == 0:
        p_lo = 0.0
    else:
        p_lo = stats.beta.ppf(alpha / 2, c1, c2 + 1)
    if c2 == 0:
        p_hi = 1.0
    else:
        p_hi = stats.beta.ppf(1 - alpha / 2, c1 + 1, c2)

    def p_to_rr(p):
        if p >= 1:
            return np.inf
        if p <= 0:
            return 0.0
        return (p / (1 - p)) * (e2 / e1)

    return (rr, p_to_rr(p_lo), p_to_rr(p_hi))


# ---------------------------------------------------------------------------
# Random-effects pooling of log rates (DerSimonian-Laird)
# ---------------------------------------------------------------------------
def pool_log_rates(counts, exposures, per=1_000_000, alpha=0.05):
    """
    Random-effects pooled rate across studies, DerSimonian-Laird on log rates.

    A continuity correction of 0.5 is applied to zero-count studies for the
    variance only. Returns a dict with pooled rate, CI, tau^2, I^2, Q, p_Q,
    prediction interval, k studies, total events, total exposure.
    """
    counts = np.asarray(counts, float)
    exposures = np.asarray(exposures, float)
    k = len(counts)
    cc = np.where(counts == 0, 0.5, counts)
    y = np.log(cc / exposures)                 # log rate
    v = 1.0 / cc                               # var(log rate) ~ 1/count
    w = 1.0 / v
    ybar_fixed = np.sum(w * y) / np.sum(w)
    Q = np.sum(w * (y - ybar_fixed) ** 2)
    df = k - 1
    C = np.sum(w) - np.sum(w ** 2) / np.sum(w)
    tau2 = max(0.0, (Q - df) / C) if C > 0 else 0.0
    w_re = 1.0 / (v + tau2)
    ybar = np.sum(w_re * y) / np.sum(w_re)
    se = np.sqrt(1.0 / np.sum(w_re))
    z = stats.norm.ppf(1 - alpha / 2)
    lo, hi = ybar - z * se, ybar + z * se
    I2 = max(0.0, (Q - df) / Q) * 100 if Q > 0 else 0.0
    p_Q = 1 - stats.chi2.cdf(Q, df) if df > 0 else np.nan
    # prediction interval (Higgins-Thompson), needs k>=3
    if k >= 3:
        t = stats.t.ppf(1 - alpha / 2, df - 1) if df - 1 > 0 else z
        pi_se = np.sqrt(se ** 2 + tau2)
        pi_lo, pi_hi = ybar - t * pi_se, ybar + t * pi_se
    else:
        pi_lo = pi_hi = np.nan
    ex = lambda a: np.exp(a) * per
    return {
        "pooled_rate": ex(ybar), "ci_lo": ex(lo), "ci_hi": ex(hi),
        "tau2": tau2, "I2": I2, "Q": Q, "p_Q": p_Q, "k": k,
        "total_events": float(counts.sum()), "total_exposure": float(exposures.sum()),
        "pi_lo": ex(pi_lo) if np.isfinite(pi_lo) else np.nan,
        "pi_hi": ex(pi_hi) if np.isfinite(pi_hi) else np.nan,
        "per": per,
    }


# ---------------------------------------------------------------------------
# Participant-minute conversion with Monte-Carlo duration uncertainty
# ---------------------------------------------------------------------------
def rate_per_minute_mc(count, n_exposures, minutes_lo, minutes_hi,
                       per=1_000_000, n_sim=200_000, seed=12345,
                       minutes_dist="uniform"):
    """
    Convert an event count with an athlete-exposure (or session) denominator to
    events per `per` participant-minutes, propagating uncertainty in the
    per-exposure minute count AND Poisson uncertainty in the event count.

    minutes_lo/hi bound the plausible mean minutes per exposure. The event count
    is resampled from a Gamma(count+0.5) posterior (Jeffreys) to reflect Poisson
    sampling error. Returns (median, p2.5, p97.5, mean).
    """
    rng = np.random.default_rng(seed)
    if minutes_dist == "uniform":
        mins = rng.uniform(minutes_lo, minutes_hi, n_sim)
    elif minutes_dist == "triangular":
        mid = 0.5 * (minutes_lo + minutes_hi)
        mins = rng.triangular(minutes_lo, mid, minutes_hi, n_sim)
    else:
        raise ValueError(minutes_dist)
    lam = rng.gamma(count + 0.5, 1.0, n_sim)          # Poisson posterior on count
    part_minutes = n_exposures * mins
    rate = lam / part_minutes * per
    return (np.median(rate), np.percentile(rate, 2.5),
            np.percentile(rate, 97.5), np.mean(rate))


def rate_ratio_mc(c1, n1, min1_lo, min1_hi, c2, n2, min2_lo, min2_hi,
                  n_sim=200_000, seed=999):
    """
    Monte-Carlo rate ratio between two populations whose exposures are
    participant-minutes reconstructed from (n_exposures * minutes-per-exposure),
    propagating both duration ranges and Poisson count error.
    n1/n2 are the exposure (session) counts; min*_lo/hi bound minutes/exposure.
    Returns (median RR, p2.5, p97.5).
    """
    rng = np.random.default_rng(seed)
    m1 = rng.uniform(min1_lo, min1_hi, n_sim)
    m2 = rng.uniform(min2_lo, min2_hi, n_sim)
    l1 = rng.gamma(c1 + 0.5, 1.0, n_sim)
    l2 = rng.gamma(c2 + 0.5, 1.0, n_sim)
    r1 = l1 / (n1 * m1)
    r2 = l2 / (n2 * m2)
    rr = r1 / r2
    return (np.median(rr), np.percentile(rr, 2.5), np.percentile(rr, 97.5))


if __name__ == "__main__":
    # quick self-test
    print("poisson_ci(19, 4_908_478*120, per=1e6):",
          poisson_ci(19, 4_908_478 * 120))
    print("rate_ratio(174,1e6, 95,2e5):", rate_ratio(174, 1e6, 95, 2e5))
    print("pool sample:", pool_log_rates([174, 12, 6], [1.1e6, 2.9e5, 1.9e5]))
