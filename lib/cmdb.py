import requests
import apibase


class CMDB(apibase.API):
    """
    (...)
    """
    
    def __init__(self, url: str, username: str, password: str, soa_username: str, soa_password: str) -> None:
        """
        Class initialization method.
        """
        
        super().__init__(url, username, password)
        self.headers["domini"] = "1123"
        self.headers["login.username"] = soa_username
        self.headers["login.password"] = soa_password
    
    
    def info_of(self, hostname: str) -> dict | None:
        """
        (...)
        """
        
        r = self.get("gN6/Infraestructuresv1/" + hostname)
        try:
            return r.json()
        except requests.exceptions.JSONDecodeError:
            raise apibase.API.NotAvailableError(r.status_code)
    
    
    def software_of(self, hostname: str) -> list | None:
        """
        (...)
        """
        
        r = self.get("gN6/Infraestructuresv1/" + hostname + "/software")
        try:
            r = r.json()["llistaRelacions"]
        except requests.exceptions.JSONDecodeError:
            raise apibase.API.NotAvailableError(r.status_code)
        except KeyError:
            return []
