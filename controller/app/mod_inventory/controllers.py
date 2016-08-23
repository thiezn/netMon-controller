#!/usr/bin/env python3

from flask import Blueprint, render_template, request, url_for, redirect
from .forms import AddDevice, DeleteDevice
from libs.tasks import TaskHandler
from libs.database import Database

mod_inventory = Blueprint('inventory', __name__, url_prefix='/inventory')

task_handler = TaskHandler()
device_db = Database()


@mod_inventory.route('/', methods=['GET'])
def get_devices():
    devices = device_db.get_all()

    return render_template('inventory/devices.html', devices=devices)


@mod_inventory.route('/add', methods=['GET', 'POST'])
def add_device():
    form = AddDevice(request.form)

    if request.method == 'POST' and form.validate():

        device = {'name': form.name.data,
                  'description': form.description.data}

        # SNMP details
        sys_info_task = {'_id': 999,
                         'type': 'SystemInfoProbe',
                         'device': device['name'],
                         'run_at': 1,
                         'run_instant': True}

        result = task_handler.add_task(sys_info_task)
        if 'error' in result:
            return render_template('inventory/add.html',
                                   form=form,
                                   error=result['error'])

        device['uptime'] = result['uptime']
        device['contact'] = result['contact']
        device['location'] = result['location']
        device['snmp_description'] = result['description']
        device['probes'] = []
        device_db.add(device)

        return redirect(url_for('inventory.get_devices'))

    return render_template('inventory/add.html', form=form)


@mod_inventory.route('/delete', methods=['GET', 'POST'])
def delete_device():
    form = DeleteDevice(request.form)

    if request.method == 'POST' and form.validate():

        # Delete all accociated tasks and the device itself
        device = device_db.get(form.device_id.data)

        if not device:
            return render_template('inventory/delete.html',
                                   form=form,
                                   error='Could not find device ID {}'.format(form.device_id.data))

        for task_id in device['probes']:
            task_handler.delete_task(task_id)

        device_db.delete(form.device_id.data)

        return redirect(url_for('inventory.get_devices'))

    return render_template('inventory/delete.html', form=form)

