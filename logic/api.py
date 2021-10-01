from flask import Flask, jsonify, request, abort

from .department import Department
from .faculty import Faculty
from .group import Group
from .student import Student

api_app = Flask(__name__)


# ФАКУЛЬТЕТЫ
@api_app.route('/faculties', methods=['GET'])
def get_faculties():
    return jsonify(list(map(Faculty.as_dict, get_faculties())))


@api_app.route('/faculty/<_id>', methods=['GET'])
def get_faculty(_id):
    try:
        return Faculty(_id).read().as_dict()
    except:
        abort(400)


@api_app.route('/faculty/<_id>', methods=['POST'])
def save_faculty(_id):
    try:
        name = request.values.get('name')
        dean = request.values.get('dean')
        info = request.values.get('info')
        return Faculty(_id, name, dean, info).save().read().as_dict()
    except:
        abort(400)


@api_app.route('/faculty/<_id>', methods=['DELETE'])
def delete_faculty(_id):
    try:
        return jsonify(Faculty(_id).delete())
    except:
        abort(400)


# КАФЕДРЫ
@api_app.route('/faculty_departments/<_id>', methods=['GET'])
def get_departments(_id):
    try:
        return jsonify(list(map(Department.as_dict, Faculty(_id).read_departments())))
    except:
        abort(400)


@api_app.route('/department/<_id>', methods=['GET'])
def get_department(_id):
    try:
        return Department(_id).read().as_dict()
    except:
        abort(400)


@api_app.route('/department/<_id>', methods=['POST'])
def save_department(_id):

    try:
        faculty = request.form.get('faculty')
        name = request.form.get('name')
        head = request.form.get('head')
        info = request.form.get('info')
        return Department(_id, faculty, name, head, info).save().read().as_dict()
    except:
        abort(400)


@api_app.route('/department/<_id>', methods=['DELETE'])
def delete_department(_id):
    try:
        return jsonify(Department(_id).delete())
    except:
        abort(400)


# ГРУППЫ
@api_app.route('/department_groups/<_id>', methods=['GET'])
def get_groups(_id):
    try:
        return jsonify(list(map(Group.as_dict, Department(_id).read_groups())))
    except:
        abort(400)


@api_app.route('/group/<_id>', methods=['GET'])
def get_group(_id):
    try:
        return Group(_id).read().as_dict()
    except:
        abort(400)


@api_app.route('/group/<_id>', methods=['POST'])
def save_group(_id):

    try:
        department = request.form.get('department')
        name = request.form.get('name')
        course = request.form.get('course')
        head = request.form.get('head')
        return Group(_id, department, name, course, head).save().read().as_dict()
    except:
        abort(400)


@api_app.route('/group/<_id>', methods=['DELETE'])
def delete_group(_id):
    try:
        return jsonify(Group(_id).delete())
    except:
        abort(400)


# СТУДЕНТЫ
@api_app.route('/group_students/<_id>', methods=['GET'])
def get_students(_id):
    try:
        return jsonify(list(map(Student.as_dict, Group(_id).read_students())))
    except:
        abort(400)


@api_app.route('/student/<_id>', methods=['GET'])
def get_student(_id):
    try:
        return Student(_id).read().as_dict()
    except:
        abort(400)


@api_app.route('/student/<_id>', methods=['POST'])
def save_student(_id):

    try:
        group = request.form.get('group')
        last_name = request.form.get('last_name')
        first_name = request.form.get('first_name')
        patronymic = request.form.get('patronymic')
        return Student(_id, group, last_name, first_name, patronymic).save().read().as_dict()
    except:
        abort(400)


@api_app.route('/student/<_id>', methods=['DELETE'])
def delete_student(_id):
    try:
        return jsonify(Student(_id).delete())
    except:
        abort(400)
