#!/usr/bin/python3

import requests, json, sys
from requests.auth import HTTPBasicAuth


url = "https://bus-soa.upc.edu/gN6/Infraestructuresv1/"

user = "usuari.ana"
password = "<XXX>"

headers = {
        "Content-Type" : "application/json",
        "login.username" :"usuarisoa.upcnet",
        "login.password" : "<XXX>",
        "domini" : "1123"
}

r = requests.get(url + sys.argv[1], auth=HTTPBasicAuth(user,password), headers=headers)
print(json.dumps(r.json(), sort_keys=True, indent=4))
