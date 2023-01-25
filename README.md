# PuppetSync
### Puppet <--> CMDB syncing tool

Syncing app between Puppet & CMDB Databases.

It is required to have a configuration file, which must have the following structure:

`config.yaml`
```yaml
puppet:
    url: https://puppet.upc.edu/
    username: <XXX>
    password: <XXX>

cmdb:
    url: https://bus-soa.upc.edu/
    username: <XXX>
    password: <XXX>
    soa_username: <XXX>
    soa_password: <XXX>
```

### Logging Levels Information:
- **DEBUG** -> Very verbose messages: *for debugging purposes*
- **INFO** -> Informative messages
- **WARNING** -> Host without software in CMDB | Relation is not correct within `relations.yaml`
- **ERROR** -> RequestError(error_code, error_msg): *CMDB Requests*
- **CRITICAL** -> NotAvailableError(status_code): *HTTP Requests*

### Arguments:
- `-d` or `--debug`: Enables **DEBUG** level for logging. When it is not specified, it uses the default **INFO** level.
- `-g` or `--group`: Specify the parent hostgroup in order to perform a smaller search in the Puppet's Foreman API. If not specified, it will request the full list of hosts without any group filtering.

### Building the image
```console
docker build -t puppetsync:1.0.0
```
##### Docker
```console
docker run -v /dev/log:/dev/log puppetsync:1.0.0
```
##### Docker Compose
```console
docker compose up
```