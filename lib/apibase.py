"""
Base API Library
~~~~~~~~~~~~~~~~

Base implementation of an API, to be used by more specific API wrappers.
"""

import requests
from http.client import responses


class API:
    """
    Base API Library
    ~~~~~~~~~~~~~~~~
    
    Base implementation of an API, to be used by more specific API wrappers.
    
    Args:
        url: Base URL of the API.
        username: Username to use for Authentication against the API.
        password: Password to use for Authentication against the API.
    """
    
    def __init__(self, url: str, username: str, password: str) -> None:
        """
        Class initialization method (private).
        """
        
        self.url = url
        self.username = username
        self.password = password
        self.headers = {
            "Content-Type": "application/json"
        }
    
    
    def __request__(self, method: str, uri: str, data: dict = None, params: dict = None) -> requests.Response:
        """
        Request base method to be used further on (private).
        """
        try:
            return requests.request(
                method = method,
                url = self.url + uri,
                auth = (self.username, self.password),
                data = data,
                params = params,
                headers = self.headers
            )
        except requests.exceptions.ConnectionError:
            raise API.NotAvailableError(404) from None
    
    
    def get(self, uri: str, params: dict = None) -> requests.Response:
        """ 
        GET HTTP method against the API endpoint specified by the 'uri' argument.
        """
        
        return self.__request__("GET", uri, params = params)
    
    
    def post(self, uri: str, data: dict, params: dict = None) -> requests.Response:
        """ 
        POST HTTP method against the API endpoint specified by the 'uri' argument.
        """
        
        return self.__request__("POST", uri, params = params, data = data)
    
    
    def put(self, uri: str, data: dict, params: dict = None) -> requests.Response:
        """ 
        PUT HTTP method against the API endpoint specified by the 'uri' argument.
        """
        
        return self.__request__("PUT", uri, params = params, data = data)
    
    
    def delete(self, uri: str, data: dict, params: dict = None) -> requests.Response:
        """ 
        DELETE HTTP method against the API endpoint specified by the 'uri' argument.
        """
        
        return self.__request__("DELETE", uri, params = params, data = data)
    
    
    class NotAvailableError(Exception):
        """
        Exception made to be raised when the API URL is not available.
        """
        
        def __init__(self, status_code: int) -> None:
            """
            Class initialization method.
            """
            
            super().__init__("{}: {}".format(status_code, responses[status_code]))
