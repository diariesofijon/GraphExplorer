#!/usr/bin/env python3
"""
Results Writer — persist benchmark output to JSON.
"""

import json
from datetime import datetime
from typing import List, Dict
from pathlib import Path

def write_results(results: List[Dict], out_dir: str) -> None:
    """
    Write results to JSON file in the output directory.
    """
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    path = Path(out_dir) / f"bench_{ts}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

