#!/usr/bin/env python3
"""
Simple structured recorder for real design → experiment campaigns.
"""

from dataclasses import dataclass, asdict
from typing import List, Optional
import json
from datetime import date


@dataclass
class CampaignRecord:
    name: str
    date: str
    target: str
    method: str
    sequences_tested: int
    functional_hits: int
    success_rate: float
    notes: str = ""
    reference: Optional[str] = None


def make_record(name: str, target: str, method: str,
                tested: int, hits: int, notes: str = "",
                reference: str = None) -> CampaignRecord:
    rate = round(hits / max(tested, 1), 4)
    return CampaignRecord(
        name=name,
        date=str(date.today()),
        target=target,
        method=method,
        sequences_tested=tested,
        functional_hits=hits,
        success_rate=rate,
        notes=notes,
        reference=reference,
    )


if __name__ == "__main__":
    example = make_record(
        name="RFdiffusion2-enzyme-demo",
        target="retroaldolase / active-site scaffold",
        method="RFdiffusion2 + filtering",
        tested=96,
        hits=3,
        notes="Illustrative numbers inspired by published small-library success",
        reference="Nature Methods / related 2025-2026 work",
    )
    print(json.dumps(asdict(example), indent=2))
