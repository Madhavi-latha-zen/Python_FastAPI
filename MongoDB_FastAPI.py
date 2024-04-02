from flask import Flask, request, jsonify
from bson import ObjectId
from pymongo import ReturnDocument
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["school"]
classes_collection = db["classes"]
students_collection = db["students"]

# Class
class ClassModel:
    def __init__(self, grade, subject_name, teacher_name, topic_name):
        self.grade = grade
        self.subject_name = subject_name
        self.teacher_name = teacher_name
        self.topic_name = topic_name


# Student
class StudentModel:
    def __init__(self, student_name, age, enrolled_class):
        self.student_name = student_name
        self.age = age
        self.enrolled_class = enrolled_class


# find_all_students
@app.route("/find_all_students", methods=["GET"])
def find_all_students():
    all_students = []
    for student in students_collection.find():
        student["_id"] = str(student["_id"])
        all_students.append(student)
    return jsonify({"students": all_students})


# find_all_classes
@app.route("/find_all_classes", methods=["GET"])
def find_all_classes():
    all_classes = []
    for class_info in classes_collection.find():
        class_info["_id"] = str(class_info["_id"])
        all_classes.append(class_info)
    return jsonify({"students": all_classes})


# add_class
@app.route("/add_class", methods=["POST"])
def add_class():
    data = request.json
    grade = data["grade"]
    subject_name = data["subject_name"]
    teacher_name = data["teacher_name"]
    topic_name = data["topic_name"]

    new_class = ClassModel(grade, subject_name, teacher_name, topic_name)
    classes_collection.insert_one(new_class.__dict__)

    return jsonify({"message": "Class added successfully"})


# add students
@app.route("/add_students", methods=["POST"])
def add_students():
    data = request.json
    student_name = data.get("student_name")
    age = data.get("age")
    enrolled_class_name = data.get("enrolled_class")

    if not all([student_name, age, enrolled_class_name]):
        return (
            jsonify(
                {
                    "error": "Invalid input data. Each student should have a name, age, and enrolled class."
                }
            ),
            400,
        )

    class_data = classes_collection.find_one({"subject_name": enrolled_class_name})
    if class_data:
        teacher_name = class_data.get("teacher_name", "")
        enrolled_class = {
            "subject_name": enrolled_class_name,
            "teacher_name": teacher_name,
            "topic_name": "",
        }
        new_student = StudentModel(student_name, age, enrolled_class)
        students_collection.insert_one(new_student.__dict__)
        return jsonify({"message": "Student added successfully"}), 201
    else:
        return jsonify({"error": f"Class '{enrolled_class_name}' not found"}), 404


# Edit class
@app.route("/edit_class/<class_id>", methods=["PUT"])
def edit_class(class_id):
    data = request.json
    updated_values = {}
    for key, value in data.items():
        if key != "_id":
            updated_values[key] = value

    if updated_values:
        result = classes_collection.update_one(
            {"_id": ObjectId(class_id)}, {"$set": updated_values}
        )
        if result.modified_count:
            return jsonify({"message": "Class updated successfully"}), 200
        else:
            return jsonify({"error": f"Class with id '{class_id}' not found"}), 404
    else:
        return jsonify({"error": "No fields provided for update"}), 400


# Edit student
@app.route("/edit_student/<student_id>", methods=["PUT"])
def edit_student(student_id):
    data = request.json
    updated_values = {}
    for key, value in data.items():
        if key != "_id":
            updated_values[key] = value

    if updated_values:
        result = students_collection.update_one(
            {"_id": ObjectId(student_id)}, {"$set": updated_values}
        )
        if result.modified_count:
            return jsonify({"message": "Student updated successfully"}), 200
        else:
            return jsonify({"error": f"Student with id '{student_id}' not found"}), 404
    else:
        return jsonify({"error": "No fields provided for update"}), 400


# Delete class
@app.route("/delete_class/<class_id>", methods=["DELETE"])
def delete_class(class_id):
    result = classes_collection.delete_one({"_id": ObjectId(class_id)})
    if result.deleted_count:
        return jsonify({"message": "Class deleted successfully"}), 200
    else:
        return jsonify({"error": f"Class with id '{class_id}' not found"}), 404


# Delete student
@app.route("/delete_student/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    result = students_collection.delete_one({"_id": ObjectId(student_id)})
    if result.deleted_count:
        return jsonify({"message": "Student deleted successfully"}), 200
    else:
        return jsonify({"error": f"Student with id '{student_id}' not found"}), 404


# filter_students_by_class
@app.route("/filter_students_by_class/<class_name>", methods=["GET"])
def filter_students_by_class(class_name):
    filtered_students = []
    for student in students_collection.find(
        {"enrolled_class.subject_name": class_name}
    ):
        student["_id"] = str(student["_id"])
        filtered_students.append(student)
    return jsonify({"students": filtered_students})


# filter_students_by_age
@app.route("/filter_students_by_age/<int:max_age>", methods=["GET"])
def filter_students_by_age(max_age):
    min_age = request.args.get("min_age")

    query = {}

    if min_age and max_age:
        query["age"] = {"$gte": int(min_age), "$lte": max_age}
    elif min_age:
        query["age"] = {"$gte": int(min_age)}
    else:
        query["age"] = {"$lte": max_age}

    filtered_students = []
    for student in students_collection.find(query):
        student["_id"] = str(student["_id"])
        filtered_students.append(student)

    return jsonify({"students": filtered_students})


# Search students by name
@app.route("/search_students_by_name/<student_name>", methods=["GET"])
def search_students_by_name(student_name):
    filtered_students = [] 
    for student in students_collection.find(
        {"student_name": {"$regex": student_name, "$options": "i"}}
    ):
        student["_id"] = str(student["_id"])
        filtered_students.append(student)

    return jsonify({"students": filtered_students})


# filter_classes_by_student
@app.route("/filter_classes_by_student/<student_name>", methods=["GET"])
def filter_classes_by_student(student_name):
    student = students_collection.find_one({"student_name": student_name})
    if not student:
        return jsonify({"error": f"Student with name '{student_name}' not found"}), 404

    enrolled_class = student.get("enrolled_class")
    if not enrolled_class:
        return (
            jsonify(
                {"message": f"Student '{student_name}' is not enrolled in any class"}
            ),
            200,
        )

    classes = classes_collection.find(
        {"subject_name": enrolled_class.get("subject_name")}
    )

    filtered_classes = []
    for cls in classes:
        cls["_id"] = str(cls["_id"])
        cls["enrolled_students"] = [student_name]
        filtered_classes.append(cls)

    return jsonify({"classes": filtered_classes}), 200


# search_classes_by_subject
@app.route("/search_classes_by_subject/<subject_name>", methods=["GET"])
def search_classes_by_subject(subject_name):
    classes = classes_collection.find({"subject_name": subject_name})

    filtered_classes = []
    for cls in classes:
        cls["_id"] = str(cls["_id"])
        filtered_classes.append(cls)

    if filtered_classes:
        return jsonify({"classes": filtered_classes}), 200
    else:
        return (
            jsonify({"message": f"No classes found for subject '{subject_name}'"}),
            404,
        )


# search_classes_by_grade
@app.route("/search_classes_by_grade/<grade>", methods=["GET"])
def search_classes_by_grade(grade):

    classes = classes_collection.find({"grade": grade})

    filtered_classes = []
    for cls in classes:
        cls["_id"] = str(cls["_id"])
        filtered_classes.append(cls)

    if filtered_classes:
        return jsonify({"classes": filtered_classes}), 200
    else:
        return jsonify({"message": f"No classes found for grade '{grade}'"}), 404


if __name__ == "__main__":
    app.run(debug=True)
