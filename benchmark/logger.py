#!/usr/bin/env python3
"""
Benchmark Logger — provides standard logging configuration.
"""

import logging

def get_logger(name: str = "functional_benchmarks"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))
    if not logger.handlers:
        logger.addHandler(handler)
    return logger

