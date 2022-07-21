#!/usr/bin/env python3

import lib.puppet as puppet
import lib.cmdb as cmdb
import modules.config as config
import modules.args as args
import sys

# Temporal import (for testing purposes)
from pprint import pprint


# Ctrl+C
def def_handler(sig, frame):
    """
    Catching and handling any KeyboardInterrupt ('SIGINT' code) sent by the user
    when a Ctrl+C is performed at any time during the execution of the script.
    """
    
    print("\n\n[!] Exiting...\n")
    sys.exit(1)


def main():
    """
    Main program flow.
    """
    
    # === API Endpoints instantiation === #
    puppet_ep = puppet.Puppet(config.puppet.url,
                    config.puppet.username,
                    config.puppet.password)
    cmdb_ep = cmdb.CMDB(config.cmdb.url,
                config.cmdb.username,
                config.cmdb.password,
                config.cmdb.soa_username,
                config.cmdb.soa_password)
    
    # === Arguments === #
    group = args.group_handler(puppet_ep)
    
    # === Main loop === #
    not_synced = []
    for host in puppet_ep.hosts(group):
        if "dadesInfraestructura" not in cmdb_ep.info_of(host["name"]):
            not_synced.append(host["name"])
            
    pprint(not_synced)


if __name__ == "__main__":
    main()
