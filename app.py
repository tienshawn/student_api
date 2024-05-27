from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS
from bson import ObjectId
import os


application = Flask(__name__)
CORS(application)

application.secret_key = 'xyzsdfg'

# application.config["MONGO_URI"] = 'mongodb://' + ':' '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']

# MONGODB_URI = os.environ.get("MONGODB_ENDPOINT")
# application.config["MONGO_URI"] = 'mongodb://db:27017/'

client = MongoClient('mongodb://localhost:27017/')
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


if __name__ == '__main__':
    application.run(debug=True)
