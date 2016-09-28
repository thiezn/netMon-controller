from flask import Flask
app = Flask(__name__)
app.config.from_object('config')

# Import all views and controllers
from app import views   # importing this will register all routes
from app.mod_tasks.controllers import mod_tasks
from app.mod_inventory.controllers import mod_inventory
from app.mod_configuration.controllers import mod_configuration
from app.mod_pollers.controllers import mod_pollers

# Register blueprints
app.register_blueprint(mod_tasks)
app.register_blueprint(mod_inventory)
app.register_blueprint(mod_configuration)
app.register_blueprint(mod_pollers)
