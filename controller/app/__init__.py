from flask import Flask
app = Flask(__name__)
app.config.from_object('config')

from app import views   # importing this will register all routes
from app.mod_tasks.controllers import mod_tasks
from app.mod_inventory.controllers import mod_inventory
from app.mod_configuration.controllers import mod_configuration

app.register_blueprint(mod_tasks)
app.register_blueprint(mod_inventory)
app.register_blueprint(mod_configuration)
