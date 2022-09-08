"""
Arguments Module
~~~~~~~~~~~~~~~~

Adding and parsing all arguments, making them accessible.
"""

import argparse
import lib.puppet as puppet
import modules.logging as logging


parser = argparse.ArgumentParser(description = "Syncing app between Puppet & CMDB Databases")

args = {}
group = lambda: args["group"]
debug = lambda: args["debug"]

def init_args(puppet_ep: puppet.Puppet) -> None:
    """
    Initializes all defined arguments.
        group (-g/--group <GROUP>): Filter the search request to Puppet's API for a
                                    specific parent hostgroup.
        debug_mode (-d/--debug): Enables the debug mode for the logging of the program.
    """
    
    # === Adding arguments === #
    parser.add_argument("-g", "--group", type=str,
                        help="Specify the parent hostgroup in order to perform \
                        a smaller search in the Puppet's Foreman API. If not specified, \
                        it will request the full list of hosts without any group filtering.")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Enables DEBUG level for logging. When it is not specified, \
                        it uses the default INFO level.")
    
    # === Parsing arguments === #
    parsed_args = parser.parse_args()
    
    # === Making arguments accessible through constants === #
    # Debug mode
    args["debug"] = parsed_args.debug
    
    # Temporal initialization of log
    log = logging.init()
    
    # Group
    if parsed_args.group and parsed_args.group in puppet_ep.groups(log):
        args["group"] = parsed_args.group
    else:
        args["group"] = None
