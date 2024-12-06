import json
from backend.models.JsonFile import JsonFile
from backend.services import db_service
from assistant_project.dict_wrapper.dict_wrapper import DictReader
from backend.utils import imports
from datetime import date

cases = ['ProductGraph, ProductionSystemGraph, ProcessGraph']
CONFIG = imports.import_yaml('backend/services/yaml_config_change.yaml')

def get_file(name):
    file = JsonFile.query.filter_by(name=name).first()
    return file


def get_file_content(name):
    file = get_file(name)
    if file is None:
        return {'content': {}, 'data': ""}
    return {'content': json.loads(file.content), 'date': file.date}


def save_file(name, file):
    # print(file['content'])
    content = json.loads(file['content'])
    old_file = get_file(name)
    if old_file is not None:
        old_file.remove()  # Remove old file before adding new
    # Save file in database
    file_db = JsonFile(name=name, content=json.dumps(content), date=file['date'])
    file_db.add()
    return file_db


def handle_file(name, file):
    file_db = save_file(name, file)
    # Extract contents and add to database
    db_service.add_entries_from_file(file_db)


def update_process_graph():
    reader = DictReader(data_cfg=CONFIG)
    file = get_file('ProcessGraph').get()
    nodes = db_service.get_all_entries('Node', formated=True)
    new_content = reader.change_items(file['content'], nodes, 'NODE')
    file['content'] = json.dumps(new_content)
    file['date'] = date.today().strftime('%Y-%m-%d')
    print(file['date'])
    save_file('ProcessGraph_', file)
