"""
Threading Module
~~~~~~~~~~~~~~~~

(...)
"""

from concurrent.futures import ThreadPoolExecutor


def init(n_threads: int):
    return ThreadPoolExecutor(max_workers = n_threads)
