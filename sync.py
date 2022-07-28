#!/usr/bin/env python3

import lib.puppet as puppet
import lib.cmdb as cmdb
import modules.config as config
import modules.args as args
import modules.funcs as funcs

# Temporal import (for testing purposes)
from pprint import pprint


# === Ctrl+C === #    
funcs.ctrl_c()


# === MAIN === #
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
    args.init_args(puppet_ep)
    
    # === Main loop === #
    for host in puppet_ep.hosts(args.group()):
        if funcs.is_in_cmdb(cmdb_ep, host):
            sw_list = cmdb_ep.software_of(host["name"])
            # Has software in CMDB
            for sw in sw_list:
                # Operating system
                if funcs.is_os(sw):
                    print(f"Syncing OS between Puppet ({puppet_ep.os(host['name'])}) and CMDB ({sw['toProductName']}) for '{host['name']}'")
                    input("Enter to continue...")
                    funcs.sync_os(puppet_ep, cmdb_ep, host["name"], sw["toProductName"])
                # Rest of software
                else:
                    print(sw["toProductName"])
                    input()
                    ####funcs.sync_sw()
            # No software in CMDB
            if not sw_list:
                # Operating system
                print(f"Adding OS ({puppet_ep.os(host['name'])}) to '{host['name']}'")
                input("Enter to continue...")
                funcs.sync_os(puppet_ep, cmdb_ep, host["name"])
                # Rest of software
                ####funcs.sync_sw()


if __name__ == "__main__":
    main()
