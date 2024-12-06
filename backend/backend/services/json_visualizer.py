from flask import Blueprint
import json

json_visualizer = Blueprint('json_visualizer', __name__)

@json_visualizer.route("/json")
def visualize_nodes():
    data = import_json()
    return {'nodes': data['Node']}


def import_json():
    with open('ProcessGraph1_2.json') as json_file:
        data = json.load(json_file)
    return data



