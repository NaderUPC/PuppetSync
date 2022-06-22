# Puppet <--> CMDB (gn6) syncing tool

Refactor and improvement of the puppet-gn6 sync tool in Python currently in production.

Es necesario disponer de un archivo de configuración donde se deben especificar las siguientes constantes:

`config.py`
```python

class cmdb:
    URL = "https://bus-soades.upc.edu/"
    HEADERS = {
        "Content-Type" : "application/json",
        "login.username" :"<XXX>",
        "login.password" : "<XXX>",
        "domini" : "1123"
    }
    USER = "<XXX>"
    PASSWD = "<XXX>"

class puppet:
    URL = "https://puppet.pre.upc.edu/"
    HEADERS = {'Content-Type': 'application/json'}
    USER = "<XXX>"
    PASSWD = "<XXX>"

```