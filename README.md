# PuppetSync
### Puppet <--> CMDB syncing tool

Syncing app between Puppet & CMDB Databases.

It is required to have a configuration file, which must have the following structure:


`config.yaml`
```yaml
puppet:
    url: https://puppet.pre.upc.edu/
    username: <XXX>
    password: <XXX>

cmdb:
    url: https://bus-soades.upc.edu/
    username: <XXX>
    password: <XXX>
    soa_username: <XXX>
    soa_password: <XXX>
```

### Logging Levels Information:
- **DEBUG** -> Very verbose messages: *for debugging purposes*
- **INFO** -> Informative messages
- **WARNING** -> Host without software in CMDB
- **ERROR** -> RequestError(error_code, error_msg): *CMDB Requests*
- **CRITICAL** -> NotAvailableError(status_code): *HTTP Requests*

### Arguments:
- `-d` or `--debug`: Enables **DEBUG** level for logging. When it is not specified, it uses the default **INFO** level.
- `-g` or `--group`: Specify the parent hostgroup in order to perform a smaller search in the Puppet's Foreman API. If not specified, it will request the full list of hosts without any group filtering.