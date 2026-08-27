"""
Exposure model: convert calendar/exposure denominators to participant-minutes
of strenuous physical training. Every annual-minute figure traces to a cited
source in sources/source_ledger.md (S06). All are given as (low, central, high)
to drive Monte-Carlo uncertainty. Quality grade attached to each.

Two denominator definitions per population, per the protocol:
  A = formal PT / practice time only (conservative -> HIGH risk per minute)
  B = all strenuous activity (measured MVPA for military; full session for NCAA)

KEY CONSTRUCT CAVEAT (documented, propagated): military denominator B is
accelerometer MVPA (idle time excluded). NCAA session minutes are wall-clock
(idle included), because NO NCAA sport has published %-above-threshold data
(S06/S11). Therefore NCAA per-minute rates are, if anything, UNDER-stated
relative to military B (NCAA denominator contains idle time). This biases NCAA
toward looking safer per active minute -> our NCAA>military conclusions are
conservative. Flagged wherever used.
"""

# ---------------------------------------------------------------------------
# Annual strenuous-training MINUTES per participant per YEAR
# (for converting athlete-year / recruit-year death denominators to minutes)
# ---------------------------------------------------------------------------
# Military recruit, per recruit-year (recruit = in trainee status; trains ~6 d/wk)
#   Denom A: 45-60 min PT session x 5-6/wk x 52 wk       (TC 3-22.20, S06)
#   Denom B: 133-182 MVPA min/day x ~323 train-days/yr   (Alemany/McAdam, S06)
MIL_RECRUIT_MIN_PER_YEAR = {
    "A": (11700, 15200, 18720),      # formal PT only
    "B": (43000, 57000, 61000),      # all measured MVPA
}
# NCAA athlete, per athlete-year (TOTAL SESSION minutes, incl idle; Grade C build-up
#   from measured session durations x typical season structure, S06). Football is
#   the most data-rich; "generic" is the cross-sport bracket.
NCAA_MIN_PER_YEAR = {
    "football":  (15000, 21000, 30000),
    "generic":   (10000, 16000, 24000),
    "lacrosse":  (10000, 15000, 22000),
}

# ---------------------------------------------------------------------------
# MINUTES per single exposure (athlete-exposure) or per person-week
# ---------------------------------------------------------------------------
# NCAA minutes per athlete-exposure (AE) = total session wall-clock (S06)
NCAA_MIN_PER_AE = {
    "football_practice": (126, 142, 180),
    "football_all":      (120, 140, 175),   # practice+game blend
    "soccer":            (59, 100, 129),
    "basketball":        (95, 104, 114),
    "lacrosse":          (80, 100, 120),
    "generic":           (90, 120, 150),
}
# Military strenuous minutes per BCT person-WEEK (Barnes denominator, S09)
#   A: formal PT 45-60 min x 5-6/wk;  B: MVPA 133-182 min/day x ~6.2 d/wk
MIL_MIN_PER_PERSONWEEK = {
    "A": (225, 292, 360),
    "B": (825, 1140, 1200),
}

# ---------------------------------------------------------------------------
# Recruit-year <-> training-cycle helpers
# ---------------------------------------------------------------------------
WEEKS_PER_YEAR = 52.14
COURSE_WEEKS = {"army": 10, "usmc": 13, "navy": 9, "af": 7.5, "avg": 8}


def recruit_year_to_minutes(person_years, denom="B"):
    """(low, central, high) participant-minutes for N recruit-person-years."""
    lo, ce, hi = MIL_RECRUIT_MIN_PER_YEAR[denom]
    return (person_years * lo, person_years * ce, person_years * hi)


def ncaa_year_to_minutes(athlete_years, sport="generic"):
    lo, ce, hi = NCAA_MIN_PER_YEAR.get(sport, NCAA_MIN_PER_YEAR["generic"])
    return (athlete_years * lo, athlete_years * ce, athlete_years * hi)


if __name__ == "__main__":
    print("Military recruit min/yr B:", MIL_RECRUIT_MIN_PER_YEAR["B"])
    print("NCAA football min/yr:", NCAA_MIN_PER_YEAR["football"])
