#!/usr/bin/env python3

from lib.puppet import Puppet
from lib.cmdb import CMDB
import config
import sys

from pprint import pprint


# Ctrl+C
def def_handler(sig, frame):
    print("\n\n[!] Exiting...\n")
    sys.exit(1)


def main():
    puppet = Puppet(config.puppet.url,
                    config.puppet.username,
                    config.puppet.password)
    cmdb = CMDB(config.cmdb.url,
                config.cmdb.username,
                config.cmdb.password,
                config.cmdb.soa_username,
                config.cmdb.soa_password)
    print(puppet)
    print(cmdb)


if __name__ == "__main__":
    main()