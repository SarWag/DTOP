from backend.models import db
import json
# from sqlalchemy.dialects.postgresql import JSON


class JsonFile(db.Model):
    __tablename__ = 'json_file_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    content = db.Column(db.String())
    date = db.Column(db.String())

    def __init__(self, name, content, date):
        self.name = name
        self.content = content
        self.date = date

    def add(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def get(self):
        return {'id': self.id,
                'name': self.name,
                'content': json.loads(self.content),
                'date': self.date
                }
