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




if __name__ == '__main__':
    application.run(debug=True)
