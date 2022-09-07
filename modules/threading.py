"""
Threading Module
~~~~~~~~~~~~~~~~

(...)
"""

import lib.puppet as puppet
from concurrent.futures import ThreadPoolExecutor
import logging


def init(log: logging.Logger, puppet_ep: puppet.Puppet, group: str):
    iterable = puppet_ep.hosts(log, group)
    return iterable, ThreadPoolExecutor(max_workers = len(iterable))
