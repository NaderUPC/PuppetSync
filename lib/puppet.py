"""
Puppet API Library
~~~~~~~~~~~~~~~~~~

Library made to act as a wrapper for the Puppet API.
"""

import simplejson
import lib.apibase as apibase
import logging
import sys
import re


class Puppet(apibase.API):
    """
    Puppet API Library
    ~~~~~~~~~~~~~~~~~~

    Library made to act as a wrapper for the Puppet API.
    
    Args:
        url: Base URL of the Puppet API.
        username: Username to use for Authentication against the Puppet API.
        password: Password to use for Authentication against the Puppet API.
    """
    
    def __init__(self, url: str, username: str, password: str) -> None:
        """
        Class initialization method.
        """
        
        super().__init__(url, username, password)
    
    
    def hosts(self, log: logging.Logger, group: str = None) -> list:
        """
        Get list of all hosts registered within Puppet. A specific group
        can be provided, to only return the hosts the belong to it.
        """
        
        params = { "per_page": "all" }
        if group:
            params["search"] = f"parent_hostgroup={group}"
        
        log.debug(f"Gathering hosts list (with a group filter -> {group}) from Puppet")
        r = self.get(log, "api/hosts", params = params)
        try:
            return r.json()["results"]
        except (simplejson.JSONDecodeError, KeyError):
            e = self.NotAvailableError(r.status_code)
            log.critical(e)
            sys.exit(r.status_code)
    
    
    def groups(self, log: logging.Logger) -> list:
        """
        Get list of groups registered within Puppet.
        """
        
        params = { "per_page": "all" }
        log.debug("Gathering groups list from Puppet")
        r = self.get(log, "api/hostgroups", params = params)
        try:
            r = r.json()["results"]
        except (simplejson.JSONDecodeError, KeyError):
            e = self.NotAvailableError(r.status_code)
            log.critical(e)
            sys.exit(r.status_code)
        return [x["title"] for x in r]
    
    
    def facts_of(self, log: logging.Logger, hostname: str) -> dict:
        """
        Given a specific hostname, gets and returns a JSON object (dict)
        with all Puppet facts associated to that host.
        """
        
        params = { "per_page": "1000" }
        r = self.get(log, f"api/hosts/{hostname}/facts", params = params)
        log.debug(f"Gathering facts list of '{hostname}' from Puppet")
        try:
            return r.json()["results"][hostname]
        except (simplejson.JSONDecodeError, KeyError):
            e = self.NotAvailableError(r.status_code)
            log.critical(e)
            sys.exit(r.status_code)
    
    
    def os(self, log: logging.Logger, hostname: str) -> str:
        """
        Given a specific hostname, returns its OS name and version.
        """
        
        facts = self.facts_of(log, hostname)
        log.debug(f"Gathering OS value from the facts list of '{hostname}' from Puppet")
        return f"{facts['operatingsystem']} {facts['operatingsystemrelease']}"
    
    
    def software(self, log: logging.Logger, hostname: str):
        """
        Given a specific hostname, returns a list of its recognized software
        in a tuple form: `(sw_name, sw_version)`.
        """
        
        facts = self.facts_of(log, hostname)
        log.debug(f"Gathering software from the facts list of '{hostname}' from Puppet")
        
        is_software = lambda fact: "_version" in fact and '::' not in fact
        is_not_coherent = lambda version: version == "false"
        
        def is_already_registered(name: str, software: list) -> bool:
            is_already_registered = lambda sw1, sw2: sw1[0] in sw2 or sw1[0] == sw2 or sw2 in sw1[0]
            already_registered = False
            for sw in software:
                if is_already_registered(sw, name):
                    already_registered = True
                    break
            return already_registered
        
        software = []
        for fact in facts:
            if is_software(fact):
                name = fact.split('_')[0]
                if is_already_registered(name, software): continue
                version = facts[fact]
                if is_not_coherent(version):
                    version = ""
                sw = (name, version)
                software.append(sw)
        
        return software
