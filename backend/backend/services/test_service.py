import json

from backend.models.InfoModel import db, InfoModel


def add_user(name, age):
    try:
        user = InfoModel(name=name, age=age)
        print("Test User")
        user.add()
        return True
    except Exception as e:
        print(e)
        db.session.rollback()
        return False


def get_user_by_name(id):
    user = db.get_or_404(InfoModel, id)
    return user.get()

def get_users():
    users = db.session.execute(db.select(InfoModel).order_by(InfoModel.name)).scalars().all()
    users = [user.get() for user in users]
    return users
