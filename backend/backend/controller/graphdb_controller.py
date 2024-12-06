from flask import Blueprint, render_template, abort
from backend.services import graphdb_service as gdb

graphdb_controller = Blueprint('graphdb_controller', __name__)

@graphdb_controller.route("/graphdb/tasks")
def get_tasks():
    return gdb.get_tasks_service()

