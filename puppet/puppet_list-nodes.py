#!/usr/bin/python3

import puppet


# Puppet Master object instantiation
# (Load Balancer Puppet Master)
p = puppet.Puppet(host='puppet-m1-pre.upc.edu',
                  port=8140,
                  key_file='ssl/kali.upc.edu.key',
                  cert_file='ssl/kali.upc.edu.pem',
                  ssl_verify=True,
                  cache_enabled=True,
                  cache_file='pypuppet_cache',
                  cache_backend='sqlite',
                  cache_expire_after=3600)

# List certnames of known SSL certificates
p.certificates()
