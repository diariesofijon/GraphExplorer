#!/usr/bin/env python3
"""
Benchmark Runner — orchestrates benchmarks using manifest + registry.
"""

from datetime import datetime
from typing import Dict, List
from .metrics import measure
from .registry import resolve

def run_benchmarks(manifest: Dict, registry: Dict, logger) -> List[Dict]:
    """
    Run all benchmarks sequentially, collecting structured results.
    """
    results = []
    for bench in manifest.get("benchmarks", []):
        fn = resolve(bench["function"], registry)
        args = {k: v for k, v in bench.items() if k not in ("id", "function", "metrics")}
        metrics = bench.get("metrics", [])
        data = measure(fn, args, metrics, logger)
        results.append({
            "id": bench["id"],
            "function": bench["function"],
            "metrics": data,
            "timestamp": datetime.utcnow().isoformat(),
        })
    return results

