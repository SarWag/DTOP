from backend.models import db


class Cell(db.Model):
    __tablename__ = 'cell_table'

    id = db.Column(db.Integer, primary_key=True)
    cell_name = db.Column(db.String())
    cell_type = db.Column(db.String())
    velocity = db.Column(db.Float())
    distance_gripper = db.Column(db.Float())

    def __init__(self, cell_id, cell_name, cell_type,
                 velocity=0, distance_gripper=0):
        self.id = cell_id
        self.cell_name = cell_name
        self.cell_type = cell_type
        self.velocity = float(velocity)
        self.distance_gripper = float(distance_gripper)
        self.add()

    def add(self):
        db.session.add(self)
        db.session.commit()

    def get(self):
        return {
            'id': self.id,
            'cell_name': self.cell_name,
            'cell_type': self.cell_type,
            'features': {
                'velocity': self.velocity,
                'distance_gripper': self.distance_gripper,
            }
        }

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def update_features(self, velocity=0, distance_gripper=0):
        self.velocity = float(velocity)
        self.distance_gripper = float(distance_gripper)
        db.session.commit()

    # def get_features(self):
    #     return {
    #         'skill': self.skill,
    #         'automation': self.automation,
    #         'layout': self.layout,
    #     }
