#!/usr/bin/env python3

from flask import Blueprint, render_template

mod_pollers = Blueprint('pollers', __name__, url_prefix='/pollers')


@mod_pollers.route('/', methods=['GET'])
def home():
    return render_template('pollers/pollers.html')
