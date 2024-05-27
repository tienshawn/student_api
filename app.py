from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS
from bson import ObjectId


application = Flask(__name__)
CORS(application)

application.secret_key = 'xyzsdfg'

client = MongoClient("mongodb://db:27017/VDT24")
db = client.flask_db


student_database = db.student_database

@application.route('/')
def get_all_students():
    students = []
    for element in student_database.find():
        student = {
            'id': str(element['_id']),
            'name': element['name'],
            'gender': element['gender'],
            'birth': element['birth'],
            'university': element['university'],
            'country': element['country']
        }
        students.append(student)

    return jsonify(students)


@application.route('/', methods=['POST'])
def create_student():
    student_data = request.get_json()
    student_name = student_data['name']
    student_gender = student_data['gender']
    student_birth = student_data['birth']
    student_university = student_data['university']
    student_country = student_data['country']
    
    new_student = {
        'name': student_name,
        'gender': student_gender,
        'birth': student_birth,
        'university': student_university,
        'country': student_country
    }
    student_database.insert_one(new_student)

    return jsonify({"status": 'success'})


@application.route('/<id>', methods=['GET'])
def get_student(id):
    student = student_database.find_one({'_id': ObjectId(id)})

    if student:
        student_detail = {
            'id': str(student['_id']),
            'name': student['name'],
            'gender': student['gender'],
            'university': student['university'],
            'birth': student['birth'],
            'country': student['country']
        }
        return jsonify(student_detail)
    else:
        return jsonify({"error": "Student not found"})


@application.route('/<id>', methods=['DELETE'])
def delete_student(id):
    student_database.delete_one({'_id': ObjectId(id)})
    return jsonify({"status": 'success'})


@application.route('/<id>', methods=['PUT'])
def update_student(id):
    student_data = request.get_json()
    updated_student = {

        'name': student_data['name'],
        'gender': student_data['gender'],
        'birth': student_data['birth'],
        'university': student_data['university'],
        'country': student_data['country']
    }
    student_database.replace_one({'_id': ObjectId(id)}, updated_student)

    return jsonify({"status": 'success'})



if __name__ == '__main__':
    application.run(debug=True)
