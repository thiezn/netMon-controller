#!/usr/bin/env python3

from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from libs.pollers import Poller, pollers
from libs.tasks import task_handler

mod_pollers = Blueprint('pollers', __name__, url_prefix='/pollers')


@mod_pollers.route('/', methods=['GET'])
def get_pollers():
    return render_template('pollers/pollers.html', pollers=pollers)


@mod_pollers.route('/register', methods=['POST'])
def register():
    if not request.json:
        return render_template('pollers/pollers.html', pollers=pollers)

    if request.json['name'] not in pollers:
        poller = Poller(request.json['ip'],
                        request.json['port'],
                        request.json['name'])
        pollers[request.json['name']] = poller

        # TODO, Handle offline pollers
        task_handler.pollers.append((request.json['ip'], request.json['port']))
        return jsonify({'status': 'poller created'}), 201
    else:
        pollers[request.json['name']].keepalive()
        return jsonify({'status': 'poller keepalive'}), 201


@mod_pollers.route('/delete/<poller_name>', methods=['GET', 'POST'])
def delete_poller(poller_name):
    print('hit')
    del pollers[poller_name]
    return redirect(url_for('pollers.get_pollers'))
