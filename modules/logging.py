"""
Logging Module
~~~~~~~~~~~~~~

Management and administration of the logs created by the program.
The format used is the following:
    {timestamp} {log_level} [{thread_id}] [{func_name}:{line_number}] {message}
Example:
    2022-07-29 10:37:55.832919 INFO [140635865786176] [main:45] This is a test!
"""

import logging
import logging.handlers
import modules.args as args


def init() -> logging.Logger:
    """
    Logger initialization.
    """
    
    logger = logging.getLogger("PuppetSync Logger")
    handler = logging.handlers.SysLogHandler(address = "/dev/log")
    
    if args.debug():
        logger.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        handler.setLevel(logging.INFO)
        
    format = logging.Formatter("%(asctime)s %(levelname)s [%(thread)d] [%(module)s:%(funcName)s:%(lineno)d] %(message)s")
    handler.setFormatter(format)
    logger.addHandler(handler)
    
    return logger
