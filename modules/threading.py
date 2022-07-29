"""
Threading Module
~~~~~~~~~~~~~~~~

(...)
"""

from concurrent.futures import ThreadPoolExecutor


def init(n_threads: int):
    thread_pool = ThreadPoolExecutor(max_workers = n_threads)
    
