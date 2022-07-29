# PuppetSync
## Puppet <--> CMDB syncing tool

Refactor and improvement of the puppet-gn6 sync tool in Python currently in production.

Es necesario disponer de un archivo de configuración donde se deben especificar las siguientes constantes:

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
- **INFO** -> Normal messages
- **WARNING** -> Host without software in CMDB
- **ERROR** -> RequestError(error_code, error_msg): *CMDB Requests*
- **CRITICAL** -> NotAvailableError(status_code): *HTTP Requests*