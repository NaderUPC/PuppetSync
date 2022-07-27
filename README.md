# Puppet <--> CMDB (gn6) syncing tool

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