"""
CMDB (gN6) API Library
~~~~~~~~~~~~~~~~~~

Library made to act as a wrapper for the CMDB API (gN6).
"""

import simplejson
import lib.apibase as apibase


class CMDB(apibase.API):
    """
    CMDB (gN6) API Library
    ~~~~~~~~~~~~~~~~~~

    Library made to act as a wrapper for the CMDB API (gN6).
    
    Args:
        url: Base URL of the CMDB (gN6) API.
        username: Username to use for Authentication against the CMDB (gN6) API.
        password: Password to use for Authentication against the CMDB (gN6) API.
        soa_username: Username to use for Authenticaion against the Bus SOA.
        soa_password: Password to use for Authenticaion against the Bus SOA.
    """
    
    def __init__(self, url: str, username: str, password: str, soa_username: str, soa_password: str) -> None:
        """
        Class initialization method.
        """
        
        super().__init__(url, username, password)
        self.headers["domini"] = "1123"
        self.headers["login.username"] = soa_username
        self.headers["login.password"] = soa_password
    
    
    def info_of(self, hostname: str) -> dict:
        """
        Given a specific hostname, gets and returns a JSON object (dict)
        with all information and properties about that host.
        """
        
        r = self.get(f"gN6/Infraestructuresv1/{hostname}")
        try:
            return r.json()
        except simplejson.JSONDecodeError:
            raise self.NotAvailableError(r.status_code) from None
    
    
    def software_of(self, hostname: str) -> list:
        """
        Given a specific hostname, gets and returns a list of all software
        associated to that host within CMDB.
        """
        
        r = self.get(f"gN6/Infraestructuresv1/{hostname}/software")
        try:
            return r.json()["llistaRelacions"]
        except simplejson.JSONDecodeError:
            raise self.NotAvailableError(r.status_code) from None
        except KeyError:
            return []
    
    
    def link_host_sw(self, hostname: str, software: str) -> None:
        """
        Given a hostname and a software name, links both in a relationship.
        """        
        
        data = {
            "idInfra": hostname,
            "nomSoftware": software
        }
        r = self.post(f"gN6/Infraestructuresv1/{hostname}/software/{software}", data)
        try:
            if r.json()["resultat"] == "SUCCESS":
                return
            else:
                raise self.RequestError(r.json()["codiError"], r.json()["resultatMissatge"]) from None
        except simplejson.JSONDecodeError:
            raise self.NotAvailableError(r.status_code) from None
    
    
    class RequestError(Exception):
        """
        Exception made to be raised when a request to the CMDB's API that carries data
        (POST, PUT, DELETE) fails and returns an error.
        """
        
        def __init__(self, error_code: str, error_msg: str) -> None:
            """
            Class initialization method.
            """
            
            super().__init__(f"{error_code}: {error_msg}")
