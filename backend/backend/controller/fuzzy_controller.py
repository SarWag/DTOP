from flask import Blueprint, request
from backend.services import fuzzy_service

fuzzy_controller = Blueprint('fuzzy_controller', __name__)


@fuzzy_controller.route('/fuzzy_control')
def calculate_node_kpi():
    return fuzzy_service.calculate_kpi_fuzzy()


# @fuzzy_controller.route('/<string:class_name>', methods=['GET', 'POST'])
# def get_all_entries(class_name):
#     if request.method == "POST":
#         print(f"For {class_name} got following body: {request.get_json()}")
#         .update_features(class_name, request.get_json())
#     return db_service.get_all_entries(class_name, formated=True)
