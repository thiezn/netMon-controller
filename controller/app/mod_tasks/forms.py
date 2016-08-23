from wtforms import Form, validators, SelectField, TextField, IntegerField


class AddTask(Form):
    """ Add a task to the poller """
    task_type = SelectField('Type',
                            [validators.Required()],
                            choices=[('InterfaceOctetsProbe', 'InterfaceOctetsProbe'),
                                     ('SystemInfoProbe', 'SystemInfoProbe'),
                                     ('SshRunSingleCommand', 'SshRunSingleCommand'),
                                     ('GetPage', 'GetPage'),
                                     ('Trace', 'Trace'),
                                     ('Ping', 'Ping')])
    device = TextField('Device')
    if_index = TextField('if_index')
    ssh_cmd = TextField('SSH Command')
    url = TextField('URL')
    run_at = IntegerField('Run at', [validators.Required()])
    recurrence_count = IntegerField('Recurrence', [validators.optional()])
    recurrence_time = IntegerField('Recurrence time (in sec)',
                                   [validators.optional()])

class DeleteTask(Form):
    """ Delete a task to the poller """
    task_id = IntegerField('Task ID', [validators.Required()])
