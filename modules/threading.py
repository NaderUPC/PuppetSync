"""
Threading Module
~~~~~~~~~~~~~~~~

Handling of the multithreading capability. Enables the ability to perform hosts
synchronization in parallel with multiple threads.
"""

import lib.puppet as puppet
from concurrent.futures import ThreadPoolExecutor
import logging


def init(log: logging.Logger, puppet_ep: puppet.Puppet, group: str):
    hosts = puppet_ep.hosts(log, group)
    return hosts, ThreadPoolExecutor(max_workers = len(hosts))
