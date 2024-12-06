from flask import Blueprint, request
from backend.services import file_handle_service
import json

file_handle_controller = Blueprint('file_handle_controller', __name__)


def process_json(content):
    return json.loads(content)


@file_handle_controller.route('/file/<string:name>', methods=['GET', 'POST'])
def process_file(name):
    file = None
    if request.method == "POST":
        file_handle_service.handle_file(name, process_json(request.data))

    file = file_handle_service.get_file(name)
    return file.get()


@file_handle_controller.route('/file/update', methods=['GET'])
def update_file():
    file_handle_service.update_process_graph()

