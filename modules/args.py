import argparse
import lib.puppet as puppet


parser = argparse.ArgumentParser(description = "Syncing script between Puppet & CMDB Databases")


def group_handler(puppet_ep: puppet.Puppet) -> str | None:
    """
    Handling the 'group' argument, through the -g or --group label.
    """
    
    parser.add_argument("-g", "--group", type=str,
                        help="Specify the parent hostgroup in order to perform \
                        a smaller search in the Puppet's Foreman API. If not specified, \
                        it will request the full list of hosts without any group filtering.")
    args = parser.parse_args()
    
    if args.group and args.group in puppet_ep.groups():
        return args.group
    return None
