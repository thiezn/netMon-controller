#!/usr/bin/env python3

from flask import Blueprint, render_template, jsonify, request
from libs.pollers import Poller

mod_pollers = Blueprint('pollers', __name__, url_prefix='/pollers')

pollers = {}


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
        return jsonify({'status': 'poller created'}), 201
    else:
        pollers[request.json['name']].keepalive()
        return jsonify({'status': 'poller keepalive'}), 201
