# MongoDB compass code

# from dotenv import load_dotenv, find_dotenv
# import os
# from pymongo import MongoClient
# import pprint
# from bson.objectid import ObjectId

# load_dotenv(find_dotenv())

# password = os.environ.get("MONGODB_PWD")

# connection_string = (
#     f"mongodb+srv://madhavilatha6:{password}@basics.f1e73fz.mongodb.net/?retryWrites=true&w=majority&appName=basics"
# )

# # connection_string = (f"mongodb://localhost:27017")
# client = MongoClient(connection_string)

# dbs = client.list_database_names()
# test_db = client.testdb
# collections = test_db.list_collection_names()
# print(collections)

# def insert_test_doc():
#     collection = test_db.testdb
#     test_document = {
#         "name" : "latha",
#         "type" : "test"
#     }
#     inserted_id = collection.insert_one(test_document).inserted_id
#     print(inserted_id)
# # insert_test_doc()

# production = client.production
# person_collection = production.person_collection

# def create_documents():
#     first_names = ["Tim","Sarah","Jennifer","Jose","Bard","madhavi"]
#     Last_names = ["Ruscica","smith","bart","cater","pit","latha"]
#     ages = [21,35,25,71,22,25]

#     docs = []

#     for first_name,last_name,age in zip(first_names,Last_names,ages):
#         doc = {"first_name":first_name,"last_name":last_name,"age" : age}
#         docs.append(doc)

#     person_collection.insert_many(docs)
# create_documents()

# printer = pprint.PrettyPrinter()

# def find_all_people():
#     people = person_collection.find()
#     # print(list(people))

#     for person in people:
#         printer.pprint(person)

# # find_all_people()

# def find_tim():
#     tim = person_collection.find_one({"first_name":"Tim"})
#     printer.pprint(tim)

# # find_tim()

# def count_all_people():
#     count = person_collection.count_documents(filter={})
#     print("Number of People",count)

# # count_all_people()

# def get_person_by_id(person_id):
#     from bson.objectid import ObjectId

#     _id = ObjectId(person_id)
#     person = person_collection.find_one({"_id":_id})
#     printer.pprint(person)

# # get_person_by_id("65f2ac6c7dd4f24a21c74000")

# def get_age_range(min_age,max_age):
#     query = {
#         "$and" : [
#             {"age":{"$gte":min_age}},
#             {"age":{"$lte":max_age}},
#         ]}
#     people = person_collection.find(query).sort("age")
#     for person in people:
#         printer.pprint(person)

# # get_age_range(20,60)

# def project_columns():
#     columns = {"_id" : 0,"first_name" : 1,"last_name" : 1,}
#     people = person_collection.find({},columns)
#     for person in people:
#         printer.pprint(person)

# # project_columns()

# def update_person_by_id(person_id):
#     from bson.objectid import ObjectId

#     _id = ObjectId(person_id)

#     #adding updates

#     # all_updates = {
#     #     "$set" : {"new_field" : True},
#     #     "$inc" : {"age" : 1},
#     #     "$rename" : {"first_name":"first" , "last_name" :"last"}
#     # }
#     # person_collection.update_one({"_id":_id},all_updates)

#     #removing Updates

#     person_collection.update_one({"_id":_id},{"$unset":{"last":""}})

# update_person_by_id("65f3ebb561d6d14c31c62e39")

# def replace_one(person_id):
#     from bson.objectid import ObjectId

#     _id = ObjectId(person_id)

#     new_doc = {
#          "first_name" : "madhu",
#          "last_name" : "latha",
#          "age" :16
#     }

#     person_collection.replace_one({"_id" : _id},new_doc)

# replace_one("65f3ebb561d6d14c31c62e38")


# def delete_doc_by_id(person_id):
#     from bson.objectid import ObjectId

#     _id = ObjectId(person_id)
#     person_collection.delete_one({"_id" : _id})

# delete_doc_by_id("5f3ebb561d6d14c31c62e35")


# # --------------------------------------------

# address = {
#     "_id" : "65f3d0943d4bcb6b0a4f9a60",
#     "street" : "palamaner",
#     "number" : "23456",
#     "city" :"AndraPradesh",
#     "country" : "India",
#     "zip" : "12345"
# }

# def add_address_embed(person_id,address):
#     from bson.objectid import ObjectId

#     _id = ObjectId(person_id)
#     person_collection.update_one(
#         {"_id":_id},{"$addToSet":{'addresses':address}}
#     )

# add_address_embed("65f3d0943d4bcb6b0a4f9a60",address)

# def add_address_relationship(person_id,address):
#     from bson.objectid import ObjectId

#     _id = ObjectId(person_id)
#     address = address.copy()
#     address["owner_id"] = person_id

#     address_collection = production.address
#     address_collection.insert_one(address)

# add_address_relationship("65f3d0943d4bcb6b0a4f9a60",address)


from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
DATABASE_NAME = "production"

client = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = client[DATABASE_NAME]
person_collection = db.person_collection


@app.route("/find_all_people", methods=["GET"])
def find_all_people():
    try:
        people = list(person_collection.find())

        for person in people:
            person["_id"] = str(person["_id"])

        return jsonify(people), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


from flask import jsonify


@app.route("/get_person_by_id/<string:person_id>", methods=["GET"])
def get_person_by_id(person_id):
    try:
        from bson.objectid import ObjectId

        _id = ObjectId(person_id)
        person = person_collection.find_one({"_id": _id})

        if person:
            person["_id"] = str(person["_id"])
            return jsonify(person), 200
        else:
            return jsonify({"error": "Person not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/create-person", methods=["POST"])
def create_person_doc():
    try:
        information = request.json
        result = person_collection.insert_one(information)
        return (
            jsonify(
                {
                    "message": "person created successfully",
                    "_id": str(result.inserted_id),
                }
            ),
            200,
        )
    except Exception as ele:
        return jsonify({"error": str(ele)}), 500


@app.route("/update-person/<string:person_id>", methods=["PUT"])
def update_person_by_id(person_id):
    try:
        _id = ObjectId(person_id)
        updates = request.json

        updates.pop("_id", None)

        person_collection.update_one({"_id": _id}, {"$set": updates})

        return jsonify({"message": "Person updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/remove-updated-person/<string:person_id>", methods=["PUT"])
def remove_updated_person(person_id):
    try:
        _id = ObjectId(person_id)

        person_collection.delete_one({"_id": _id})

        return jsonify({"message": "Person removed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/delete-person/<string:person_id>", methods=["DELETE"])
def delete_doc_by_id(person_id):
    try:
        _id = ObjectId(person_id)
        person_collection.delete_one({"_id": _id})

        return jsonify({"message": "Person deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
