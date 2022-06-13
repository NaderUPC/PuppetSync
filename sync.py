#!/usr/bin/env python3

from pwn import *
import sys
import signal
import requests
from requests.auth import HTTPBasicAuth
import time
import argparse

import config


# Ctrl+C
def def_handler(sig, frame):
    """
    Catching and handling any KeyboardInterrupt ('SIGINT' code) sent by the user
    when does Ctrl+C any time during the execution of the script.
    """

    print("\n\n[!] Exiting...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)


def request_to_puppet(group):
    """
    HTTP GET request to Puppet's Foreman API to obtain the list with all registered hosts
    (either all or specified ones based on the group parameter).
    """

    uri = "api/hosts"
    params = {
        "per_page": "all"
    }
    if group:
        params["search"] = "parent_hostgroup={}".format(group)

    r = requests.get(config.puppet.URL + uri, params=params,
                     auth=(config.puppet.USER,config.puppet.PASSWD),
                     headers=config.puppet.HEADERS)
    return r.json()['results']


def request_to_cmdb(host: str):
    """
    HTTP GET request to BUS SOA API (gn6) to obtain information about the host specified
    via parameter.
    """

    r = requests.get(config.cmdb.URL + host,
                     auth=HTTPBasicAuth(config.cmdb.USER,config.cmdb.PASSWD),
                     headers=config.cmdb.HEADERS)
    return r.json()


def get_puppet_groups():
    """
    HTTP GET request to Puppet's Foreman API to obtain all hostgroups with their respective
    parent hostgroup (on order to perform a parent_hostgroup based search).
    """

    r = requests.get(config.puppet.URL + "/api/hostgroups?per_page=all",
                     auth=(config.puppet.USER,config.puppet.PASSWD),
                     headers=config.puppet.HEADERS).json()['results']
    return [x['title'] for x in r]


def group_handler(parser: argparse.ArgumentParser):
    """
    Handling the 'group' argument, through the -g or --group label.
    """

    parser.add_argument("-g", "--group", type=str,
                         help="Specify the parent hostgroup in order to perform \
                         a smaller search in the Puppet's Foreman API. If not specified, \
                         it will request the full list of hosts without any group filtering.")
    args = parser.parse_args()
    p_args = log.progress("Group checker (-g / --group)")
    if args.group:
        if args.group in get_puppet_groups():
            p_args.success("[DONE] Filtering by '{}'".format(args.group))
            return args.group
        else:
            p_args.failure("[FAIL] No filtering will be done.")
            return None
    else:
        p_args.failure("[FAIL] No filtering will be done.")
        return None


def main():
    """
    Main program flow.
    """

    # === Title === #
    log.info("\033[1m\033[4m" + "Syncing Puppet & CMDB Databases" + "\033[0m")
    
    print()
    time.sleep(2)

    # === Arguments === #
    parser = argparse.ArgumentParser(description="Syncing script between Puppet & CMDB Databases")
    group = group_handler(parser)
    
    print()
    time.sleep(2)
    
    # === Main variables === #
    not_in_cmdb = []
    p_puppet = log.progress("Puppet")

    p_puppet.status("Sending GET request to Puppet's Foreman API...")
    all_hosts = request_to_puppet(group)

    p_cmdb = log.progress("CMDB")
    p_not_synced = log.progress("Hosts not synced {Puppet <--> CMDB}")

    print()
    p_software = log.progress("Software")

    # === Main loop === #
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

    p_puppet.success("[DONE]")
    p_cmdb.success("[DONE]")
    p_not_synced.success(str(len(not_in_cmdb)))
    p_software.success("[DONE]")

    # === Writing final list to file === #
    if group:
        filename = "not_in_cmdb_{}.txt".format(group).replace('/', '-')
    else:
        filename = "not_in_cmdb_ALL.txt"
    with open(filename, "w") as f:
        for host in not_in_cmdb:
            f.write("{}\n".format(host))


if __name__ == "__main__":
    main()
