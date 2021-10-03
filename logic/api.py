from flask import Flask, jsonify, request, abort, make_response

from .department import Department
from .faculty import Faculty, get_faculties
from .group import Group
from .student import Student

api_app = Flask(__name__)


def __set_cors_headers__(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


def __get_options_method_response__(access_methods):
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', access_methods)
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


# OPTIONS
@api_app.route('/faculties', methods=['OPTIONS'])
@api_app.route('/faculty/<_id>', methods=['OPTIONS'])
@api_app.route('/faculty_departments/<_id>', methods=['OPTIONS'])
@api_app.route('/department/<_id>', methods=['OPTIONS'])
@api_app.route('/department_groups/<_id>', methods=['OPTIONS'])
@api_app.route('/group/<_id>', methods=['OPTIONS'])
@api_app.route('/group_students/<_id>', methods=['OPTIONS'])
@api_app.route('/student/<_id>', methods=['OPTIONS'])
def app_faculties_options():
    try:
        return __get_options_method_response__(['OPTIONS', 'GET', 'POST', 'DELETE'])
    except:
        abort(400)


# ФАКУЛЬТЕТЫ
@api_app.route('/faculties', methods=['GET'])
def app_get_faculties():
    try:
        return __set_cors_headers__(jsonify(list(map(Faculty.as_dict, get_faculties()))))
    except:
        abort(400)


@api_app.route('/faculty/<_id>', methods=['GET'])
def app_get_faculty(_id):
    try:
        return __set_cors_headers__(jsonify(Faculty(_id).read().as_dict()))
    except:
        abort(400)


@api_app.route('/faculty/<_id>', methods=['POST'])
def app_save_faculty(_id):
    try:
        name = request.values.get('name')
        dean = request.values.get('dean')
        info = request.values.get('info')
        return __set_cors_headers__(jsonify(Faculty(_id, name, dean, info).save().read().as_dict()))
    except:
        abort(400)


@api_app.route('/faculty/<_id>', methods=['DELETE'])
def app_delete_faculty(_id):
    try:
        return __set_cors_headers__(jsonify(Faculty(_id).delete()))
    except:
        abort(400)


# КАФЕДРЫ
@api_app.route('/faculty_departments/<_id>', methods=['GET'])
def app_get_departments(_id):
    try:
        return __set_cors_headers__(jsonify(list(map(Department.as_dict, Faculty(_id).read_departments()))))
    except:
        abort(400)


@api_app.route('/department/<_id>', methods=['GET'])
def app_get_department(_id):
    try:
        return __set_cors_headers__(jsonify(Department(_id).read().as_dict()))
    except:
        abort(400)


@api_app.route('/department/<_id>', methods=['POST'])
def app_save_department(_id):

    try:
        faculty = request.form.get('faculty')
        name = request.form.get('name')
        head = request.form.get('head')
        info = request.form.get('info')
        return __set_cors_headers__(jsonify(Department(_id, faculty, name, head, info).save().read().as_dict()))
    except:
        abort(400)


@api_app.route('/department/<_id>', methods=['DELETE'])
def app_delete_department(_id):
    try:
        return __set_cors_headers__(jsonify(Department(_id).delete()))
    except:
        abort(400)


# ГРУППЫ
@api_app.route('/department_groups/<_id>', methods=['GET'])
def app_get_groups(_id):
    try:
        return __set_cors_headers__(jsonify(list(map(Group.as_dict, Department(_id).read_groups()))))
    except:
        abort(400)


@api_app.route('/group/<_id>', methods=['GET'])
def app_get_group(_id):
    try:
        return __set_cors_headers__(jsonify(Group(_id).read().as_dict()))
    except:
        abort(400)


@api_app.route('/group/<_id>', methods=['POST'])
def app_save_group(_id):

    try:
        department = request.form.get('department')
        name = request.form.get('name')
        course = request.form.get('course')
        head = request.form.get('head')
        return __set_cors_headers__(jsonify(Group(_id, department, name, course, head).save().read().as_dict()))
    except:
        abort(400)


@api_app.route('/group/<_id>', methods=['DELETE'])
def app_delete_group(_id):
    try:
        return __set_cors_headers__(jsonify(Group(_id).delete()))
    except:
        abort(400)


# СТУДЕНТЫ
@api_app.route('/group_students/<_id>', methods=['GET'])
def app_get_students(_id):
    try:
        return __set_cors_headers__(jsonify(list(map(Student.as_dict, Group(_id).read_students()))))
    except:
        abort(400)


@api_app.route('/student/<_id>', methods=['GET'])
def app_get_student(_id):
    try:
        return __set_cors_headers__(jsonify(Student(_id).read().as_dict()))
    except:
        abort(400)


@api_app.route('/student/<_id>', methods=['POST'])
def app_save_student(_id):

    try:
        group = request.form.get('group')
        last_name = request.form.get('last_name')
        first_name = request.form.get('first_name')
        patronymic = request.form.get('patronymic')
        return __set_cors_headers__(
            jsonify(Student(_id, group, last_name, first_name, patronymic).save().read().as_dict())
        )
    except:
        abort(400)


@api_app.route('/student/<_id>', methods=['DELETE'])
def app_delete_student(_id):
    try:
        return __set_cors_headers__(jsonify(Student(_id).delete()))
    except:
        abort(400)
