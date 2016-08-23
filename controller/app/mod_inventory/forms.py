from wtforms import Form, validators, TextField, IntegerField


class AddDevice(Form):
    """ Add a Device to the inventory """
    name = TextField('Name/IP', [validators.Required()])
    description = TextField('Description')


class DeleteDevice(Form):
    """ Delete a task to the poller """
    device_id = IntegerField('Device ID', [validators.Required()])
