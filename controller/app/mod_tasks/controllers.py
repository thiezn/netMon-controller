#!/usr/bin/env python3

from flask import Blueprint, render_template, request, redirect, url_for
from libs.tasks import TaskHandler, form_to_json_task
from libs.database import Database
from .forms import AddTask, DeleteTask
import json


mod_tasks = Blueprint('tasks', __name__, url_prefix='/tasks')
task_handler = TaskHandler(pollers=[('127.0.0.1', 9090), ('127.0.0.1', 9091)])
database = Database()


@mod_tasks.route('/', methods=['GET'])
def get_tasks():
    tasks = task_handler.get_tasks()

    return render_template('tasks/scheduled.html',
                           title='Scheduled tasks',
                           tasks=tasks)


@mod_tasks.route('/<task_id>', methods=['GET'])
def get_task(task_id):
    task = task_handler.get_task(task_id)
    print(task)
    return render_template('tasks/task.html',
                           title='Task',
                           task=task,
                           data=task[task_id])


@mod_tasks.route('/results', methods=['GET'])
def get_results():
    results = task_handler.get_results()
    if 'error' in results:
        return render_template('tasks/scheduled.html',
                               title='Scheduled tasks',
                               results=[results])

    return render_template('tasks/results.html',
                           title='Task results',
                           results=results)


@mod_tasks.route('/add', methods=['GET', 'POST'])
def add_tasks():
    form = AddTask(request.form)

    if request.method == 'POST' and form.validate():
        task = form_to_json_task(form)
        result = task_handler.add_task(task)
        if result and 'error' in result:
            return render_template('tasks/add.html',
                                   form=form,
                                   error=result)
        return redirect(url_for('tasks.get_tasks'))

    return render_template('tasks/add.html', form=form)


@mod_tasks.route('/update/<task_id>', methods=['GET', 'PUT'])
def update_task(task_id):
    pass


@mod_tasks.route('/delete', methods=['GET', 'POST'])
def delete_task():
    form = DeleteTask(request.form)

    if request.method == 'POST' and form.validate():
        result = task_handler.delete_task(form.task_id.data)
        if result and 'error' in result:
            return render_template('tasks/delete.html',
                                   form=form,
                                   error=result['error'])
        return redirect(url_for('tasks.get_tasks'))

    return render_template('tasks/delete.html', form=form)
