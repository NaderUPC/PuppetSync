#!/usr/bin/env python3

import lib.puppet as puppet
import lib.cmdb as cmdb
import modules.config as config
import modules.args as args
import modules.funcs as funcs
import modules.logging as logging
import modules.threading as threading


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
    
    # === Logger === #
    log = logging.init()
    
    # === Main sync function === #
    def sync(host: str):
        if funcs.is_in_cmdb(log, cmdb_ep, host):
            sw_list = cmdb_ep.software_of(log, host["name"])
            # Has software in CMDB
            for sw in sw_list:
                # Operating system
                if funcs.is_os(sw):
                    log.info(f"Syncing OS between Puppet ({puppet_ep.os(log, host['name'])}) and CMDB ({sw['toProductName']}) for '{host['name']}'")
                    funcs.sync_os(log, puppet_ep, cmdb_ep, host["name"], sw["toProductName"])
                # Rest of software
                else:
                    pass
            # No software in CMDB
            if not sw_list:
                # Operating system
                log.info(f"Syncing OS between Puppet ({puppet_ep.os(host['name'])}) and CMDB (None) for '{host['name']}'")
                funcs.sync_os(log, puppet_ep, cmdb_ep, host["name"])
                # Rest of software
                pass
    
    # === Threads execution === #
    iterable, threads = threading.init(log, puppet_ep, args.group())
    threads.map(sync, iterable)


if __name__ == "__main__":
    main()
