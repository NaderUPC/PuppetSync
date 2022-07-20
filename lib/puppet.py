import requests
import apibase


class Puppet(apibase.API):
    """
    (...)
    """
    
    def __init__(self, url: str, username: str, password: str) -> None:
        """
        Class initialization method.
        """
        
        super().__init__(url, username, password)
    
    
    def hosts(self, group: str = None) -> list | None:
        """
        (...)
        """
        
        params = { "per_page": "all" }
        if group:
            params["search"] = "parent_hostgroup={}".format(group)
            
        r = self.get("api/hosts", params = params)
        try:
            return r.json()["results"]
        except requests.exceptions.JSONDecodeError:
            raise apibase.API.NotAvailableError(r.status_code)
    
    
    def groups(self) -> list | None:
        """
        (...)
        """
        
        params = { "per_page": "all" }
        r = self.get("api/hostgroups", params = params)
        try:
            r = r.json()["results"]
        except requests.exceptions.JSONDecodeError:
            raise apibase.API.NotAvailableError(r.status_code)
        return [x["title"] for x in r]
    
    
    def facts_of(self, hostname: str) -> dict | None:
        """
        (...)
        """
        params = { "per_page": "1000" }
        r = self.get("api/hosts/" + hostname + "/facts", params = params)
        try:
            return r.json()["results"][hostname]
        except requests.exceptions.JSONDecodeError:
            raise apibase.API.NotAvailableError(r.status_code)
