from flask import jsonify,request
from bson import ObjectId
from app.extensions import mongo
from app.models.User import UserModel
import bcrypt

def get_users(user_id=None):
    if user_id:
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            user['_id'] = str(user['_id'])
            return jsonify(user)
        else:
            return jsonify({"error": "User not found"}), 404
    else:
        users = mongo.db.users.find()
        user_list = []
        for user in users:
            user['_id'] = str(user['_id'])
            user_list.append(user)
        return jsonify(user_list)

def register_user():
    data = request.get_json()

    try:
        user = UserModel(data)
        user.validate()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Duplicate checks
    if mongo.db.users.find_one({"email": user.email}):
        return jsonify({"error": "Email already exists"}), 400

    if mongo.db.users.find_one({"user_name": user.user_name}):
        return jsonify({"error": "Username already taken"}), 400

    user.hash_password()
    result = mongo.db.users.insert_one(user.to_dict())

    user_data = user.to_dict()
    user_data["_id"] = str(result.inserted_id)
    user_data.pop("password")

    return jsonify({
        "message": "User registered successfully",
        "user": user_data
    }), 201

def user_login():
    data = request.get_json()
    required_fields = ["email", "password"]
    if not all(data.get(field) for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    user = mongo.db.users.find_one({"email": data["email"]})
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    if not bcrypt.checkpw(data["password"].encode("utf-8"), user["password"].encode("utf-8")):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({
        "message": "Login successful",
        "user_id": str(user["_id"]),
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
        "user_name": user["user_name"]
    }), 200
