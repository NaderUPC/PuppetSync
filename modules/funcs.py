"""
Functions/Functionalities Module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Definition of the tasks to perform for each specific action.
It is the main communication pipe between the program and the libraries.
"""

import sys
import signal
import lib.puppet as puppet
import lib.cmdb as cmdb
import logging


# === Lambda/Arrow function definitions === #
is_in_cmdb = lambda log, cmdb_ep, host: "dadesInfraestructura" in cmdb_ep.info_of(log, host["name"])
is_os = lambda software: software["sistemaOperatiu"] == 'Y'


# === Function definitions === #
def ctrl_c():
    """
    Catching and handling any KeyboardInterrupt ('SIGINT' code) sent by the user
    when a Ctrl+C is performed at any time during the execution of the script.
    """
    
    def def_handler(sig, frame):
        print("\n\n[!] Exiting...\n")
        sys.exit(1)
    
    signal.signal(signal.SIGINT, def_handler)


def sync_os(log: logging.Logger, puppet_ep: puppet.Puppet, cmdb_ep: cmdb.CMDB, hostname: str, cmdb_os: str = None) -> None:
    """
    Synchronizes the host's OS in CMDB with the one registered in Puppet.
    If they are equal, then it does not do anything (since it already has the correct OS).
    Instead, if they differ, the one that prevails is the one present within Puppet. 
    """
    
    if puppet_ep.os(log, hostname) != cmdb_os or not cmdb_os:
        log.debug(f"Starting sync of '{hostname}' OS")
        cmdb_ep.link_host_sw(hostname, puppet_ep.os(hostname))
    else:
        log.debug(f"Host's ({hostname}) OS ({puppet_ep.os(log, hostname)}) is already in sync, no need to do anything.")


def sync_sw(log: logging.Logger, puppet_ep: puppet.Puppet, cmdb_ep: cmdb.CMDB, hostname: str, cmdb_sw: str = None) -> None:
    """
    (...)
    """
    
    pass
