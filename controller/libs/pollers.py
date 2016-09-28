#!/usr/bin/env python3

from time import time

pollers = {}


class Poller:
    """A single poller connection"""

    def __init__(self, ip, port, name=None, keepalive_interval=None):
        """ Initialise task handler

        :param ip: Poller IP address
        :param port: Poller listening port
        :param name: Poller name
        """
        self.ip = ip
        self.port = port
        self.name = name
        self.online_since = time()
        self.last_keepalive = time()

        if keepalive_interval:
            self.keepalive_interval = keepalive_interval
        else:
            self.keepalive_interval = 120

        self._is_online = True

    @property
    def is_online(self):
        """Check if the poller is still online"""
        next_keepalive = self.last_keepalive + self.keepalive_interval
        if next_keepalive >= time():
            self._is_online = True
        else:
            self._is_online = False

        return self._is_online

    def keepalive(self):
        """Handle received keepalive"""
        self.last_keepalive = time()
