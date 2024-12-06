from flask import Blueprint, render_template, request
from backend.services import test_service

test_controller = Blueprint('test_controller', __name__)


@test_controller.route('/form')
def form():
    return render_template('test.html')


@test_controller.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        if test_service.add_user(name, age):
            return f"Done!!"
        return f"Did not work!"


@test_controller.route('/users/<int:id>')
def user(id):
    return test_service.get_user_by_name(id)

@test_controller.route('/users')
def users():
    return test_service.get_users()