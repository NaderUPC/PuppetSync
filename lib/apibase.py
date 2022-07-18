import requests


class API:
    """
    (...)
    """
    
    def __init__(self, url: str, username: str, password: str) -> None:
        """
        (...)
        """
        
        self.url = url
        self.username = username
        self.password = password
        self.headers = {
            "Content-Type": "application/json"
        }
    
    
    def __request__(self, method: str, uri: str, params: dict = None, data: dict = None) -> requests.Response:
        """
        (...)
        """
        
        return requests.request(
            method = method,
            url = self.url + uri,
            auth = (self.username, self.password),
            data = data,
            params = params
        )
    
    
    def get(self, uri: str, params: dict = None) -> requests.Response:
        """
        (...)
        """
        
        return self.__request__("GET", uri, params = params)
    
    
    def post(self, uri: str, data: dict, params: dict = None) -> requests.Response:
        """
        (...)
        """
        
        return self.__request__("POST", uri, params = params, data = data)
    
    
    def put(self, uri: str, data: dict, params: dict = None) -> requests.Response:
        """
        (...)
        """
        
        return self.__request__("PUT", uri, params = params, data = data)
    
    
    def delete(self, uri: str, data: dict, params: dict = None) -> requests.Response:
        """
        (...)
        """
        
        return self.__request__("DELETE", uri, params = params, data = data)
