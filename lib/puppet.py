"""
Puppet API Library
~~~~~~~~~~~~~~~~~~

Library made to act as a wrapper for the Puppet API.
"""

import simplejson
from lib.apibase import API


class Puppet(API):
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
    
    
    def hosts(self, group: str = None) -> list | None:
        """
        Get list of all hosts registered within Puppet. A specific group
        can be provided, to only return the hosts the belong to it.
        """
        
        params = { "per_page": "all" }
        if group:
            params["search"] = "parent_hostgroup={}".format(group)
            
        r = self.get("api/hosts", params = params)
        try:
            return r.json()["results"]
        except (simplejson.JSONDecodeError, KeyError):
            raise API.NotAvailableError(r.status_code) from None
    
    
    def groups(self) -> list | None:
        """
        Get list of groups registered within Puppet.
        """
        
        params = { "per_page": "all" }
        r = self.get("api/hostgroups", params = params)
        try:
            r = r.json()["results"]
        except (simplejson.JSONDecodeError, KeyError):
            raise API.NotAvailableError(r.status_code) from None
        return [x["title"] for x in r]
    
    
    def facts_of(self, hostname: str) -> dict | None:
        """
        Given a specific hostname, gets and returns a JSON object (dict)
        with all Puppet facts associated to that host.
        """
        
        params = { "per_page": "1000" }
        r = self.get("api/hosts/" + hostname + "/facts", params = params)
        try:
            return r.json()["results"][hostname]
        except (simplejson.JSONDecodeError, KeyError):
            raise API.NotAvailableError(r.status_code) from None
    
    
    def os(self, hostname: str) -> str:
        """
        Given a specific hostname, returns its OS name and version.
        """
        
        facts = self.facts_of(hostname)
        return "{} {}".format(facts["operatingsystem"],
                              facts["operatingsystemrelease"])
