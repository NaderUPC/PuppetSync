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


# === Lambda/Arrow function definitions === #
is_in_cmdb = lambda cmdb_ep, host: "dadesInfraestructura" in cmdb_ep.info_of(host["name"])
is_os = lambda software: software["sistemaOperatiu"] == 'Y'


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
    for host in puppet_ep.hosts(group):
        if is_in_cmdb(cmdb_ep, host):
            sw_list = cmdb_ep.software_of(host["name"])
            # Has software in CMDB
            if sw_list:
                for sw in sw_list:
                    # Operating system
                    if is_os(sw):
                        print(f"Syncing OS between Puppet ({puppet_ep.os(host['name'])}) and CMDB ({sw['toProductName']}) for '{host['name']}'")
                        input("Enter to continue...")
                        funcs.sync_os(puppet_ep, cmdb_ep, host["name"], sw["toProductName"])
                    # Rest of software
                    else:
                        funcs.sync_sw()
            # No software in CMDB
            else:
                # Operating system
                print(f"Adding OS ({puppet_ep.os(host['name'])}) to '{host['name']}'")
                input("Enter to continue...")
                funcs.add_os()
                # Rest of software
                funcs.add_sw()


if __name__ == "__main__":
    main()
