#!/usr/bin/env python3

from flask import Blueprint, render_template

mod_configuration = Blueprint('configuration', __name__, url_prefix='/configuration')


@mod_configuration.route('/', methods=['GET'])
def get_configuration():
    return render_template('configuration/index.html')
