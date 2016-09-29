from flask import render_template
from app import app

from libs.tasks import task_handler
from libs.pollers import pollers


@app.route('/', methods=['GET'])
def home():
    task_types = {}

    for task_id, task in task_handler.tasks.items():
        if task['type'] not in task_types:
            task_types[task['type']] = 1
        else:
            task_types[task['type']] += 1

    return render_template('index.html', task_types=task_types)
