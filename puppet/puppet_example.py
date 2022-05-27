#!/usr/bin/python3

import puppet


# Puppet Master object instantiation
# (Load Balancer Puppet Master)
p = puppet.Puppet(host='puppet.pre.upc.edu',
                  port=8140,
                  key_file=None,
                  cert_file=None,
                  ssl_verify=True,
                  cache_enabled=True,
                  cache_file='pypuppet_cache',
                  cache_backend='sqlite',
                  cache_expire_after=3600)


# Puppet Node object instantiation
n = p.node(None)


# Node object available variables:
n.certname
n.classes
n.environment
n.facts
n.node
n.parameters

# Node object available methods:
n.certificate()
n.certificate_status()
catalog = n.catalog() # Compile and download the node's catalog


# List certnames of known SSL certificates
p.certificates()

# Delete certificate of host (ISSUE: https://github.com/daradib/pypuppet/issues/5)
p.certificate_clean(None)

# List certnames of SSL certificate requests
p.certificate_requests()


# Iterate over all hosts discharged in Puppet
for certname in p.certificates():
    try:
        print(p.node(certname))
        break
    except puppet.APIError:
        # Node probably does not exist
        continue

# List nodes matching matching arguments of fact comparison
# More info on 'Facts Search': https://puppet.com/docs/puppetdb/7/api/query/v4/facts.html
# In this example, we are searching for all hosts running a RedHat distribution based on a x86_64 architecture:
p.facts_search(('osfamily', 'RedHat'), ('architecture', 'x86_64'))

# Another example would be searching for all hosts that have been up (powered on) for >100 days:
p.facts_search(('uptime_days', 'gt', 100))


# Requestor object (for more advanced and precise queries)
p.requestor.get('certificate_revocation_list', 'ca', parser='s')
p.requestor.get('resource', 'package/puppet')
p.requestor.get('resources', 'user')
