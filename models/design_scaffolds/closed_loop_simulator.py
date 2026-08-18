#!/usr/bin/env python3
"""
Ra-Thor-Protein-Molecular-Design — Closed-Loop Success Rate Simulator
PATSAGi / TOLC 8 — Phase 2 Preparation

Purpose:
  Monte-Carlo style exploration of how in-silico filter strength and
  experimental hit rate affect the number of sequences that must be
  tested to obtain functional molecules.

Truth Gate:
  Hit rates are user-supplied parameters. This tool does not predict
  real experimental outcomes; it only helps reason about campaign design.
"""

import random
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class CampaignParams:
    n_designs_generated: int
    in_silico_keep_fraction: float   # after filters
    experimental_hit_rate: float     # fraction of tested sequences that work
    n_rounds: int = 1


def run_campaign(p: CampaignParams, seed: int = 42) -> Dict:
    random.seed(seed)
    results = []
    total_tested = 0
    total_hits = 0

    for rnd in range(p.n_rounds):
        n_keep = max(1, int(p.n_designs_generated * p.in_silico_keep_fraction))
        hits = sum(1 for _ in range(n_keep) if random.random() < p.experimental_hit_rate)
        total_tested += n_keep
        total_hits += hits
        results.append({"round": rnd + 1, "tested": n_keep, "hits": hits})

    return {
        "rounds": results,
        "total_tested": total_tested,
        "total_hits": total_hits,
        "overall_success_rate": round(total_hits / max(total_tested, 1), 4),
    }


if __name__ == "__main__":
    print("=== Closed-loop campaign simulator (illustrative) ===\n")

    # Example inspired by recent RFdiffusion2-style small-library success
    optimistic = CampaignParams(
        n_designs_generated=500,
        in_silico_keep_fraction=0.2,   # keep 100
        experimental_hit_rate=0.04,    # 4% of tested work
        n_rounds=1,
    )
    res = run_campaign(optimistic)
    print("Optimistic small-library style:")
    print(f"  Tested: {res['total_tested']}, Hits: {res['total_hits']}, Rate: {res['overall_success_rate']}")

    conservative = CampaignParams(
        n_designs_generated=2000,
        in_silico_keep_fraction=0.1,
        experimental_hit_rate=0.01,
        n_rounds=2,
    )
    res2 = run_campaign(conservative, seed=7)
    print("\nMore conservative multi-round:")
    print(f"  Tested: {res2['total_tested']}, Hits: {res2['total_hits']}, Rate: {res2['overall_success_rate']}")
    print("\nReplace hit-rate assumptions with real campaign data.")
