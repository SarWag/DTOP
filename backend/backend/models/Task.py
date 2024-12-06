from backend.models import db
import re

forbidden = ['Pick', 'Feeding', 'Transport']

class Task(db.Model):
    __tablename__ = 'task_table'

    id = db.Column(db.Integer, primary_key=True)
    task_type = db.Column(db.String())
    process_type = db.Column(db.String())
    modules = db.Column(db.String())
    parts_weight = db.Column(db.Float())
    length_extraction = db.Column(db.Float())
    accessibility = db.Column(db.Float())
    distance = db.Column(db.Float())
    diam_screw = db.Column(db.Float())
    len_screw = db.Column(db.Float())
    fit = db.Column(db.Float())
    complexity = db.Column(db.Float())
    depth = db.Column(db.Float())
    range_movement = db.Column(db.Float())


    def __init__(self, task_id, task_type, process_type, modules,
                 parts_weight=0, length_extraction=0, accessibility=0, distance=0, diam_screw=0, len_screw=0, fit=0,
                 complexity=0, depth=0, range_movement=0):
        self.id = task_id
        self.task_type = task_type
        self.process_type = re.sub(r'[0-9]+', '', process_type)
        self.modules = modules
        self.parts_weight = float(parts_weight)
        self.length_extraction = float(length_extraction)
        self.accessibility = float(accessibility)
        self.distance = float(distance)
        self.diam_screw = float(diam_screw)
        self.len_screw = float(len_screw)
        self.fit = float(fit)
        self.complexity = float(complexity)
        self.depth = float(depth)
        self.range_movement = float(range_movement)
        if self.task_type not in forbidden:
            self.add()

    def add(self):
        db.session.add(self)
        db.session.commit()

    def get(self):
        return {
            'id': self.id,
            'task_type': self.task_type,
            'process_type': self.process_type,
            'modules': self.modules,
            'features': {
                'parts_weight': self.parts_weight,
                'length_extraction': self.length_extraction,
                'accessibility': self.accessibility,
                'distance': self.distance,
                'diam_screw': self.diam_screw,
                'len_screw': self.len_screw,
                'fit': self.fit,
                'complexity': self.complexity,
                'depth': self.depth,
                'range_movement': self.range_movement
            }
        }

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def update_features(self, parts_weight=0, length_extraction=0, accessibility=0, distance=0, diam_screw=0,
                        len_screw=0, fit=0, complexity=0, depth=0, range_movement=0):
        self.parts_weight = float(parts_weight)
        self.length_extraction = float(length_extraction)
        self.accessibility = float(accessibility)
        self.distance = float(distance)
        self.diam_screw = float(diam_screw)
        self.len_screw = float(len_screw)
        self.fit = float(fit)
        self.complexity = float(complexity)
        self.depth = float(depth)
        self.range_movement = float(range_movement)
        db.session.commit()


    # def get_features(self):
    #     return {
    #             'parts_weight': self.parts_weight,
    #             'placing_precision': self.placing_precision,
    #             'distance': self.distance,
    #             'diam_screw': self.diam_screw,
    #             'len_screw': self.len_screw
    #         }
