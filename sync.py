#!/usr/bin/python3

from pwn import *

import sys
import signal
import requests
from requests.auth import HTTPBasicAuth
import time

import config


# Ctrl+C
def def_handler(sig, frame):
    print("\n\nExiting...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)


def request_to_puppet():
    uri = "api/hosts?per_page=all"
    r = requests.get(config.puppet.URL + uri,
                     auth=(config.puppet.USER,config.puppet.PASSWD),
                     headers=config.puppet.HEADERS)
    return r.json()['results']


def request_to_cmdb(host: str):
    r = requests.get(config.cmdb.URL + host,
                     auth=HTTPBasicAuth(config.cmdb.USER,config.cmdb.PASSWD),
                     headers=config.cmdb.HEADERS)
    return r.json()


def main():
    log.info("Syncing Puppet & CMDB Databases")
    
    print()
    time.sleep(2)
    
    result = ""
    p_puppet = log.progress("Puppet")

    p_puppet.status("Making GET request to Puppet...")
    all_hosts = request_to_puppet()

    p_cmdb = log.progress("CMDB")
    p_result = log.progress("Hosts not synced {Puppet <--> CMDB}")

    for host in all_hosts:
        hostname = host['name']
        p_puppet.status("Iterating over host '{}'".format(hostname))

        p_cmdb.status("Checking whether it is registered in CMDB")
        if "dadesInfraestructura" not in request_to_cmdb(hostname):
            result += "{} , ".format(hostname)
        p_result.status(result)

    p_puppet.success("Done!")
    p_cmdb.success("Done!")
    p_result.success("{} hosts not in CMDB".format(result.count(',') + 1))
    

if __name__ == "__main__":
    main()

