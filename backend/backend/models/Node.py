from backend.models import db

forbidden = ['Pick', 'Feeding', 'Transport']

class Node(db.Model):
    __tablename__ = 'node_table'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer())
    cell_id = db.Column(db.Integer())
    time = db.Column(db.Float())
    cost = db.Column(db.Float())
    quality = db.Column(db.Float())

    def __init__(self, node_id, task_id, cell_id, task_type,
                 time=0, cost=0, quality=0):
        self.id = node_id
        self.task_id = task_id
        self.cell_id = cell_id
        self.time = time
        self.cost = cost
        self.quality = quality
        if task_type not in forbidden:
            self.add()

    def add(self):
        db.session.add(self)
        db.session.commit()

    def get(self):
        return {
            'id': self.id,
            'taskId': self.task_id,
            'cellId': self.cell_id,
            'features': {
                'time': self.time,
                'cost': self.cost,
                'quality': self.quality
            }
        }

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def update_features(self, time=0, cost=0, quality=0):
        self.time = time
        self.cost = cost
        self.quality = quality
        db.session.commit()

    def update_by_fuzzy(self, time):
        self.time = time
        db.session.commit()
