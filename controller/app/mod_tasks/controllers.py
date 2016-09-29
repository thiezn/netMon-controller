#!/usr/bin/env python3

from flask import Blueprint, render_template, request, redirect, url_for
from libs.tasks import form_to_json_task, task_handler
from libs.database import Database
from .forms import AddTask
from libs.pollers import pollers

mod_tasks = Blueprint('tasks', __name__, url_prefix='/tasks')
database = Database()


@mod_tasks.route('/', methods=['GET'])
def get_tasks():
    tasks = task_handler.get_tasks()

    return render_template('tasks/tasks.html',
                           title='Scheduled tasks',
                           tasks=tasks)


@mod_tasks.route('/<task_id>', methods=['GET'])
def get_task(task_id):
    """Returns a single task

    :return: List of the Task on each poller
    """
    tasks = task_handler.get_task(task_id)
    results = task_handler.get_result(task_id)

    data = {}
    for poller in results:
        data[poller['poller']] = []
        for result in poller[task_id]:
            if tasks[0]['type'] == 'Ping':
                data[poller['poller']].append(result['avg'])

    # data[0][tasks[0]._id]|safe

    return render_template('tasks/task.html',
                           title='Task',
                           tasks=tasks,
                           data=data)


@mod_tasks.route('/results', methods=['GET'])
def get_results():
    results = task_handler.get_results()
    if 'error' in results:
        return render_template('tasks/tasks.html',
                               title='Scheduled tasks',
                               results=[results])

    return render_template('tasks/results.html',
                           title='Task results',
                           results=results)


@mod_tasks.route('/add', methods=['GET', 'POST'])
def add_tasks():
    form = AddTask(request.form)
    form.pollers.choices.extend([(name, name) for name in pollers])

    if request.method == 'POST' and form.validate():
        task = form_to_json_task(form)
        result = task_handler.add_task(task, pollers=form['pollers'])
        if result and 'error' in result:
            return render_template('tasks/add.html',
                                   form=form,
                                   error=result)

        if request.form['submit'] == 'Add':
            return redirect(url_for('tasks.get_tasks'))
        elif request.form['submit'] == 'Repeat':
            return render_template('tasks/add.html', form=form, alert='Added task {} {}'.format(task['type'], task['description']))

    return render_template('tasks/add.html', form=form)


@mod_tasks.route('/update/<task_id>', methods=['GET', 'PUT'])
def update_task(task_id):
    pass


@mod_tasks.route('/delete/<task_id>', methods=['GET', 'POST'])
def delete_task(task_id):
    task_handler.delete_task(task_id)
    return redirect(url_for('tasks.get_tasks'))
