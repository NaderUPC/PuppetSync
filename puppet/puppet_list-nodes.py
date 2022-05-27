#!/usr/bin/python3

import puppet


# Puppet Master object instantiation
# (Load Balancer Puppet Master)
p = puppet.Puppet(host='puppet.pre.upc.edu',
                  port=8140,
                  key_file=None,
                  cert_file=None,
                  ssl_verify=False,
                  cache_enabled=True,
                  cache_file='pypuppet_cache',
                  cache_backend='sqlite',
                  cache_expire_after=3600)

# List certnames of known SSL certificates
p.certificates()
