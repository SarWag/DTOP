from backend.models.Cell import Cell
from backend.models.Task import Task
from backend.models.Node import Node
from backend.models import db
import json
from assistant_project.dict_wrapper.dict_wrapper import DictReader
from backend.utils import wrappers, imports

CONFIG = imports.import_yaml('backend/services/yaml_config.yaml')

__db__ = {
    'Task': Task,
    'Cell': Cell,
    'Node': Node
}


def get_entry_by_id(db_class, db_id, formated=False):
    db_class = __db__[db_class] if isinstance(db_class, str) else db_class
    entry = db.get_or_404(db_class, db_id)
    if formated:
        return entry.get()
    return entry


def get_all_entries(db_class, formated=False):
    db_class = __db__[db_class] if isinstance(db_class, str) else db_class
    entries = db.session.execute(db.select(db_class).order_by(db_class.id)).scalars().all()
    if formated:
        return [entry.get() for entry in entries]
    return entries


def remove_old_entries(db_class):
    db_class = __db__[db_class] if isinstance(db_class, str) else db_class
    entries = get_all_entries(db_class)
    for entry in entries:
        entry.remove()


# @wrappers.input_result_wrapper
def add_entries_from_file(file):
    reader = DictReader(data_cfg=CONFIG)
    db_names = reader.get_cfg_from_name(file.name)
    for db_name in db_names:
        db_entries = reader.get_items(json.loads(file.content), db_name)
        db_class = reader.config[db_name]['DATABASE']
        # Remove existing rows from database
        db.session.query(__db__[db_class]).delete()
        # Add new rows from file
        for entry in db_entries:
            __db__[db_class](**entry)


def update_features(class_name, db_obj):
    db_class = __db__[class_name]
    for entry in db_obj:
        db_entry = db.get_or_404(db_class, entry['id'])
        db_entry.update_features(**entry['features'])


# def update_task_table(tasks):
#     for task in tasks:
#         task = get_task_by_id(task.task_id)
#         task.update_features(task.features)
def update_table(data):
    return None