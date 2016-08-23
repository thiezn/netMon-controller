#!/usr/bin/env python3

class Database:
    """ Handle storage of tasks and task results """

    def __init__(self):
        """ Initialise the storage

        This is just a placeholder class for a database. We will use a single
        list that will take key/value pairs (aka dicts)
        """

        self.db = []

    def add(self, data):
        """ Adds a record to the db

        :param data: dictionary containing data to write
        """
        return self.db.append(data)

    def get(self, item_id):
        """ Retrieves an item from the db """
        pass

    def get_all(self):
        """Retrieve all records from the db"""
        return self.db

    def query(self, query):
        """ Query the db

        :param query: A record to query for. at the moment requires the full record
        """
        if query in self.db:
            return self.session.query(query)
        else:
            return None
