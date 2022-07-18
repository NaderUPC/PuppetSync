import requests
import apibase


class Puppet(apibase.API):
    """
    (...)
    """
    
    def __init__(self, url: str, username: str, password: str) -> None:
        """
        (...)
        """
        
        super().__init__(url, username, password)
    
    
    def hosts(self, group: str = None):
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
            return r.status_code
    
    
    def groups(self):
        pass
