#!/usr/bin/env python3

import requests
import pickle
from base64 import b64encode, b64decode
import json


def form_to_json_task(form):
    """ Generate JSON from a task form """

    task_type = form.task_type.data
    run_at = form.run_at.data
    device = form.device.data
    recurrence_count = form.recurrence_count.data
    recurrence_time = form.recurrence_time.data
    if_index = form.if_index.data
    ssh_cmd = form.ssh_cmd.data
    url = form.url.data

    task = {}
    task['type'] = task_type
    task['device'] = device
    task['run_at'] = run_at
    task['recurrence_count'] = recurrence_count
    task['recurrence_time'] = recurrence_time

    if task_type == 'InterfaceOctetsProbe':
        if not if_index:
            raise ValueError('InterfaceOctetsProbe requires if_index')
        task['if_index'] = if_index
    elif task_type == 'SystemInfoProbe':
        pass
    elif task_type == 'SshRunSingleCommand':
        if not ssh_cmd:
            raise ValueError('SshRunSingleCommand requires command')
        task['cmd'] = ssh_cmd
    elif task_type == 'GetPage':
        if not url:
            raise ValueError('GetPage requires url')
        task['url'] = url
    elif task_type == 'Trace':
        pass
    elif task_type == 'Ping':
        pass
    else:
        raise ValueError('Unknown task type {}'.format(task_type))

    return task


class TaskHandler:
    """ Manage scheduled tasks on poller(s) and retrieve the results """

    def __init__(self, pollers=[("127.0.0.1", 9090)]):
        """ Initialise task handler

        :param pollers: List of pollers. Poller is a tuple of (ip, port)
        """
        # TODO: Currently only supporting a single poller
        self.pollers = pollers
        self.tasks = {}
        proxies = {"http": None, "https": None}
        self.session = requests.Session()
        self.session.proxies = proxies
        self.session.headers.update({'Content-Type': 'application/json'})

    def generate_task_id(self, new_task):
        """ Returns a new unique task id """
        return b64encode(pickle.dumps(new_task)).decode('utf-8')

    def reverse_task_id(self, task_id):
        """ Returns the original task dict """
        return pickle.loads(b64decode(task_id))

    def _url(self, partial_url):
        """ Creates a full url """

        return ["http://{}:{}/{}".format(*poller, partial_url) for poller in self.pollers]
        #return "{}{}".format(self._BASE_URL, partial_url)

    def _get(self, url):
        """ GET Request to REST API """
        poller_urls = self._url(url)

        for poller_url in poller_urls:
            try:
                response = self.session.get(poller_url)
            except requests.exceptions.ConnectionError:
                return {'error': 'Could not establish session with {}'
                                 .format(poller_url)}

            if response.status_code != 200:
                return {'error': "{}: {}".format(response.status_code,
                                                 response.content)}
            else:
                return json.loads(response.text)

    def _post(self, url, payload):
        """ POST Request to REST API """
        poller_urls = self._url(url)

        for poller_url in poller_urls:
            try:
                response = self.session.post(poller_url,
                                             data=json.dumps(payload))
            except requests.exceptions.ConnectionError:
                return {'error': 'Could not establish session with {}'
                                 .format(poller_url)}

            if response.status_code == 200:
                return json.loads(response.text)

            if response.status_code != 204:
                return {'error': "{}: {}".format(response.status_code,
                                                 response.content)}
            else:
                return None

    def _delete(self, url, payload=None):
        """ DELETE request to REST API """
        poller_urls = self._url(url)
        print(poller_urls)

        for poller_url in poller_urls:
            try:
                response = self.session.delete(poller_url,
                                               data=json.dumps(payload))
            except requests.exceptions.ConnectionError:
                return {'error': 'Could not establish session with {}'
                                 .format(poller_url)}

            if response.status_code != 204:
                return {'error': "{}: {}".format(response.status_code,
                                                 response.content)}
            else:
                None

    def _put(self, url, payload):
        """ PUT Request to REST API """
        pass

    def _patch(self, url, payload):
        """ PATCH Request to REST API """
        pass

    def add_task(self, task, pollers=None):
        """ Add a task to the poller(s)

        :param task: dictionary containing task object
        :param pollers: list of pollers to query, None=query all
        """
        task['_id'] = self.generate_task_id(task)
        result = self._post('tasks', task)

        # result can contain the data in case of run_instant.
        # it could also contain a dict with {'error': code}
        if not result:
            return task['_id']
        else:
            return result

    def delete_task(self, task_id, pollers=None):
        """ Deletes a task from the poller(s) """

        return self._delete('tasks', {'task_id': task_id})

    def get_task(self, task_id, pollers=None):
        """ Retrieve a scheduled task from poller(s)

        :param task_id: the ID of the task to retrieve
        :param pollers: list of pollers to query, None=query all
        """
        return self._get('tasks/{}'.format(task_id))

    def get_result(self, task_id, pollers=None):
        """ Retrieve the results of a scheduled task on poller(s)

        :param task_id: the ID of the task to retrieve results for
        :param pollers: list of pollers to query, None=query all
        """
        pass

    def get_tasks(self, pollers=None):
        """ Retrieve all scheduled tasks on poller(s)

        :param pollers: list of pollers to query, None=query all
        """
        return self._get('tasks')

    def get_results(self, pollers=None):
        """ Retrieve all results from scheduled tasks on poller(s)

        :param pollers: list of pollers to query, None=query all
        """
        return self._get('results')
