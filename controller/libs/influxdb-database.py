#!/usr/bin/env python3

import influxdb

class Database:
    """ Handle storage of tasks and task results """

    def __init__(self, host='localhost', port=8086,
                 user='root', passwd='root', db_name='netmon'):
        """ Initialise the storage

        This is just a placeholder class for a database. We will use a single
        list that will take key/value pairs (aka dicts)
        """

        self.session = influxdb.InfluxDBClient(host, port, user, passwd, db_name)

        try:
            self.session.create_database(db_name)
        except influxdb.exceptions.InfluxDBClientError:
            print("Can't create db {}, exists already".format(db_name))

    def add(self, data):
        """ Adds a record to the db

        :param data: dictionary containing data to write
        """
        return self.session.write_points(data)

    def get(self, item_id):
        """ Retrieves an item from the db """
        pass

    def query(self, query_string):
        """ Query the db

        :param query_string: Query the database
        """
        return self.session.query(query_string)


def main():
    db = Database()

    data = [{
        "measurement": "cpu_load_short",
        "tags": {
            "host": "server01",
            "region": "us-west"
        },
        "time": "2009-11-10T23:00:00Z",
        "fields": {
            "value": 0.64
        }
    }]

    print(db.add(data))


if __name__ == '__main__':
    main()
