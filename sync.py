#!/usr/bin/env python3

import lib.puppet as puppet
import lib.cmdb as cmdb
import modules.config as config
import modules.args as args
import sys

# Temporal import (for testing purposes)
from pprint import pprint
import signal


# Ctrl+C
def def_handler(sig, frame):
    """
    Catching and handling any KeyboardInterrupt ('SIGINT' code) sent by the user
    when a Ctrl+C is performed at any time during the execution of the script.
    """
    
    print("\n\n[!] Exiting...\n")
    sys.exit(1)
    
signal.signal(signal.SIGINT, def_handler)


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
    print("HOST: PUPPET OS <-> CMDB OS")
    print("--------------------------------")
    for host in puppet_ep.hosts(group):
        if "dadesInfraestructura" in cmdb_ep.info_of(host["name"]):
            sw_list = cmdb_ep.software_of(host["name"])
            if not sw_list:
                print(host["name"] + ": " + puppet_ep.os(host["name"]) + " <-> " + "None")
            else:
                for sw in sw_list:
                    if sw["sistemaOperatiu"] == 'Y':
                        print(host["name"] + ": " + puppet_ep.os(host["name"]) + " <-> " + sw["toProductName"])


if __name__ == "__main__":
    main()
