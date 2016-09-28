#!/usr/bin/env python3

from time import time


class Poller:
    """A single poller connection"""

    def __init__(self, ip, port, name=None):
        """ Initialise task handler

        :param ip: Poller IP address
        :param port: Poller listening port
        :param name: Poller name
        """
        self.ip = ip
        self.port = port
        self.name = name
        self.online_since = time()
        self.last_keepalive = None
