import sys
import signal
import lib.puppet as puppet
import lib.cmdb as cmdb

# Temporal import (for testing purposes)
from pprint import pprint


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

def sync_os(puppet_ep: puppet.Puppet, cmdb_ep: cmdb.CMDB, hostname: str, cmdb_os: str) -> None:
    """
    Synchronizes the host's OS in CMDB with the one registered in Puppet.
    If they are equal, then it does not do anything (since it already has the correct OS).
    Instead, if they differ, the one that prevails is the one present within Puppet. 
    """
    
    if puppet_ep.os(hostname) != cmdb_os:
        cmdb_ep.link_host_sw(hostname, puppet_ep.os(hostname))

def sync_sw(puppet_ep: puppet.Puppet, cmdb_ep: cmdb.CMDB, hostname: str, cmdb_sw: str) -> None:
    """
    (...)
    """
    
    pass

def add_os(puppet_ep: puppet.Puppet, cmdb_ep: cmdb.CMDB, hostname: str) -> None:
    """
    (...)
    """
    
    cmdb_ep.link_host_sw(hostname, puppet_ep.os(hostname))

def add_sw():
    """
    (...)
    """
    
    pass
