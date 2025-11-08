#!/usr/bin/env python3
# functional_benchmarks/metrics.py
"""
Metrics — functional performance measurements.

Implements pure-ish metric collectors:
- time
- memory
- recursion_depth
- logger_overhead_pct
- ops_per_sec

The main function is `measure(fn, args, metrics, logger) -> Dict[str, Any]`.
"""

from typing import Callable, Dict, Any, List, Optional
import time
import tracemalloc
import sys
import logging
import gc
from functools import reduce

# -- Helpers ------------------------------------------------------------------

def _call(fn: Callable, args: Optional[Dict[str, Any]] = None):
    """Call target function with args dict or without args."""
    if args:
        return fn(**args)
    return fn()

def _time_call(fn: Callable, args: Optional[Dict[str, Any]] = None) -> float:
    """Return elapsed seconds for a single call of fn(**args)."""
    t0 = time.perf_counter()
    _call(fn, args)
    t1 = time.perf_counter()
    return t1 - t0

def _memory_snapshot_call(fn: Callable, args: Optional[Dict[str, Any]] = None) -> float:
    """
    Run fn and return peak memory usage (MB) observed via tracemalloc.
    Note: tracer measures Python memory allocator only (not full RSS).
    """
    gc.collect()
    tracemalloc.start()
    try:
        _call(fn, args)
        current, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    # return peak in MB
    return peak / 1024 / 1024

def _recursion_limit_snapshot() -> int:
    """Return current interpreter recursion limit (not runtime depth)."""
    return sys.getrecursionlimit()

def _throughput(fn: Callable, args: Optional[Dict[str, Any]] = None, repeat: int = 1) -> Dict[str, Any]:
    """
    Run fn `repeat` times and return total time and ops/sec.
    Returns dict with keys: total_time_s, ops_per_sec
    """
    if repeat <= 0:
        repeat = 1
    # warmup
    _call(fn, args)
    t0 = time.perf_counter()
    for _ in range(repeat):
        _call(fn, args)
    t1 = time.perf_counter()
    total = t1 - t0
    ops_per_sec = repeat / total if total > 0 else float("inf")
    return {"total_time_s": total, "ops_per_sec": ops_per_sec}

def _run_with_disabled_logging(fn: Callable, args: Optional[Dict[str, Any]] = None) -> float:
    """
    Temporarily disable all handlers of the logger root (and descendants) and time the call.
    Returns elapsed seconds.
    """
    root = logging.getLogger()
    # store levels and handlers state
    handlers = list(root.handlers)
    level = root.level
    # temporarily disable by setting a high level and removing handlers
    for h in handlers:
        root.removeHandler(h)
    root.setLevel(logging.CRITICAL + 10)
    try:
        elapsed = _time_call(fn, args)
    finally:
        # restore
        for h in handlers:
            root.addHandler(h)
        root.setLevel(level)
    return elapsed

def _run_with_logger(logger: logging.Logger, fn: Callable, args: Optional[Dict[str, Any]] = None) -> float:
    """
    Ensure logger stays active and time the call. Use logger passed in to perform
    a no-op log during execution so that log I/O is measured where applicable.
    Returns elapsed seconds.
    """
    # Log a start marker if logger enabled
    logger.debug("benchmark-run-start")
    return _time_call(fn, args)

# -- Metric implementations ---------------------------------------------------

def measure_time(fn: Callable, args: Optional[Dict[str, Any]] = None, logger: Optional[logging.Logger] = None) -> float:
    """Measure elapsed time (seconds) for a single call."""
    return _time_call(fn, args)

def measure_memory(fn: Callable, args: Optional[Dict[str, Any]] = None, logger: Optional[logging.Logger] = None) -> float:
    """Measure peak memory for a single call (MB) using tracemalloc."""
    return _memory_snapshot_call(fn, args)

def measure_recursion_depth(fn: Callable, args: Optional[Dict[str, Any]] = None, logger: Optional[logging.Logger] = None) -> int:
    """Return current recursion limit (proxy for allowed depth)."""
    # Note: this returns interpreter limit, not measured call depth.
    return _recursion_limit_snapshot()

def measure_logger_overhead(fn: Callable, args: Optional[Dict[str, Any]] = None, logger: Optional[logging.Logger] = None, repeat: int = 1) -> float:
    """
    Estimate percent overhead of having logging enabled.
    Procedure:
        - time_no_log = run fn with logging handlers removed
        - time_with_log = run fn with logger active (calls made normally)
        - overhead_pct = (time_with_log - time_no_log) / max(time_no_log, tiny) * 100
    Returns overhead percent (float).
    """
    # baseline: disabled logging
    t_no_log = _run_with_disabled_logging(fn, args)
    # with logger enabled: use provided logger if any, else root logger
    active_logger = logger or logging.getLogger()
    # Ensure the logger has at least one handler (so logging does something)
    if not active_logger.handlers:
        # attach a null handler to avoid "No handler" warnings but still measure minimal overhead
        active_logger.addHandler(logging.NullHandler())
    t_with_log = _run_with_logger(active_logger, fn, args)
    tiny = 1e-9
    overhead = (t_with_log - t_no_log) / max(t_no_log, tiny) * 100.0
    return overhead

def measure_ops_per_sec(fn: Callable, args: Optional[Dict[str, Any]] = None, repeat: int = 1, logger: Optional[logging.Logger] = None) -> Dict[str, Any]:
    """Return throughput metrics for `repeat` executions."""
    return _throughput(fn, args, repeat)

# -- Top-level measure dispatcher --------------------------------------------

_METRIC_FUNCS = {
    "time": measure_time,
    "memory": measure_memory,
    "recursion_depth": measure_recursion_depth,
    "logger_overhead_pct": measure_logger_overhead,
    "ops_per_sec": measure_ops_per_sec,
}

def measure(fn: Callable, args: Optional[Dict[str, Any]], metrics: List[str], logger: Optional[logging.Logger] = None) -> Dict[str, Any]:
    """
    Measure the requested metrics for fn(**args).
    - `fn` : callable
    - `args`: dict of kwargs to pass (may be None)
    - `metrics`: list of metric keys from _METRIC_FUNCS
    - `logger`: logger instance to use for logger_overhead_pct if requested

    Returns a dict mapping metric -> measured value (floats/ints/dicts).
    """
    results: Dict[str, Any] = {}
    # local copy to avoid mutation of input
    args_copy = dict(args) if args else {}
    # allow 'repeat' as special key used by ops_per_sec and logger_overhead_pct
    repeat = int(args_copy.pop("repeat", 1))

    # Ensure deterministic GC state
    gc.collect()

    for m in metrics:
        if m not in _METRIC_FUNCS:
            raise ValueError(f"Unknown metric requested: {m}")
        if m == "ops_per_sec":
            results[m] = _METRIC_FUNCS[m](fn, args_copy, repeat, logger)
        elif m == "logger_overhead_pct":
            # logger-specific uses repeat for more stable measurement if >1
            # perform multiple quick runs to stabilize
            results[m] = _METRIC_FUNCS[m](fn, args_copy, logger, repeat)
        else:
            results[m] = _METRIC_FUNCS[m](fn, args_copy, logger)

    return results

