"""
Configuration Module
~~~~~~~~~~~~~~~~~~~~

Parsing of the `config.yaml` file, making all data accessible.
"""

import yaml


config = yaml.safe_load(open("config.yaml"))

class puppet:
    url = config["puppet"]["url"]
    username = config["puppet"]["username"]
    password = config["puppet"]["password"]

class cmdb:
    url = config["cmdb"]["url"]
    username = config["cmdb"]["username"]
    password = config["cmdb"]["password"]
    soa_username = config["cmdb"]["soa_username"]
    soa_password = config["cmdb"]["soa_password"]
