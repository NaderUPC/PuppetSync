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
import yaml


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
    
    log.info(f"Syncing OS between Puppet ({puppet_ep.os(log, hostname)}) and CMDB ({cmdb_os}) for '{hostname}'")
    puppet_os = puppet_ep.os(log, hostname)
    
    if puppet_os != cmdb_os or not cmdb_os:
        log.debug(f"Starting sync of '{hostname}' OS")
        cmdb_ep.link_host_sw(log, hostname, puppet_os)
    else:
        log.debug(f"Host's ({hostname}) OS ({puppet_os}) is already in sync, no need to do anything.")


def sync_sw(log: logging.Logger, puppet_ep: puppet.Puppet, cmdb_ep: cmdb.CMDB, hostname: str, cmdb_sw: str = None) -> None:
    """
    Synchronizes the host's software in CMDB with the ones registered in Puppet.
    If they are equal, then it does not do anything (since it already has the correct SW).
    Instead, if they differ, the one that prevails is the one present within Puppet.
    """
    
    software = puppet_ep.software(log, hostname)
    if not software:
        log.warning(f"Host '{hostname}' has no software registered in Puppet")
        return
    
    relations = yaml.safe_load(open("relations.yaml"))
    
    for sw in software:
        puppet_sw = None
        for item in relations:
            if sw[0] == item:
                puppet_sw = relations[item]
        if not puppet_sw:
            log.warning(f"Software '{sw[0]}' of host '{hostname}' does not exist in 'relations.yaml'")
            continue
        else:
            log.info(f"Syncing SW between Puppet ({puppet_sw}) and CMDB for '{hostname}'")
            
            if puppet_sw != cmdb_sw or not cmdb_sw:
                log.debug(f"Starting sync of '{hostname}' SW ({puppet_sw})")
                cmdb_ep.link_host_sw(log, hostname, puppet_sw)
            else:
                log.debug(f"Host's ({hostname}) SW ({puppet_sw}) is already in sync, no need to do anything.")
