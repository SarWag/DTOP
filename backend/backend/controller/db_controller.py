from flask import Blueprint, request
from backend.services import db_service

db_controller = Blueprint('db_controller', __name__)


@db_controller.route('/db/<string:class_name>/<int:task_id>')
def get_entry_by_id(class_name, class_id):
    pass


@db_controller.route('/db/<string:class_name>', methods=['GET', 'POST'])
def get_all_entries(class_name):
    if request.method == "POST":
        # print(f"For {class_name} got following body: {request.get_json()}")
        db_service.update_features(class_name, request.get_json())
    return db_service.get_all_entries(class_name, formated=True)
