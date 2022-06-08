#!/usr/bin/python3

from pwn import *

import sys
import signal
import requests
from requests.auth import HTTPBasicAuth
import time

import config

from pprint import pprint


# Ctrl+C
def def_handler(sig, frame):
    print("\n\n[!] Exiting...\n")
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
    log.info("\033[1m\033[4m" + "Syncing Puppet & CMDB Databases" + "\033[0m")
    
    print()
    time.sleep(2)
    
    not_in_cmdb = []
    p_puppet = log.progress("Puppet")

    p_puppet.status("Sending GET request to Puppet's Foreman API...")
    all_hosts = request_to_puppet()

    p_cmdb = log.progress("CMDB")
    p_not_synced = log.progress("Hosts not synced {Puppet <--> CMDB}")

    print()
    p_software = log.progress("Software")

    for host in all_hosts:
        hostname = host['name']
        p_puppet.status("Iterating over host [{}/{}] '{}'".format(all_hosts.index(host) + 1, len(all_hosts), hostname))

        p_cmdb.status("Checking whether it is registered in CMDB...")
        if "dadesInfraestructura" not in request_to_cmdb(hostname):
            not_in_cmdb.append(hostname)
        else:
            try:
                sw_list = request_to_cmdb(hostname + "/software")['llistaRelacions']
                for software in sw_list:
                    software_name = software['toBrandName']
                    p_software.status("Iterating over software '{}'".format("\033[1m\033[92m" + software_name + "\033[0m"))
                    # (...)
            except:
                p_software.status("Iterating over software '{}'".format("\033[1m\033[91m" + "N/A" + "\033[0m"))
        p_not_synced.status(str(len(not_in_cmdb)))

    p_puppet.success("[OK]")
    p_cmdb.success("[OK]")
    p_not_synced.success(str(len(not_in_cmdb)))
    p_software.success("[OK]")


if __name__ == "__main__":
    main()
