from flask import jsonify,request
from bson import ObjectId
from app.extensions import mongo
from datetime import datetime
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

    required_fields = ["first_name", "last_name", "email", "password", "phone_number", "user_name"]
    if not all(data.get(field) for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if user already exists
    if mongo.db.users.find_one({"email": data["email"]}):
        return jsonify({"error": "Email already exists"}), 400

    if mongo.db.users.find_one({"user_name": data["user_name"]}):
        return jsonify({"error": "Username already taken"}), 400

    # Hash the password
    hashed_password = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())

    # Create the user document
    user_document = {
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "email": data["email"],
        "password": hashed_password.decode("utf-8"),
        "email_verified": False,
        "email_verified_at": None,
        "is_active": True,
        "phone_number": data["phone_number"],
        "is_phone_number_verified": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "deleted_at": None,
        "user_name": data["user_name"]
    }

    # Insert into MongoDB
    result = mongo.db.users.insert_one(user_document)

    return jsonify({"message": "User registered successfully", "user_id": str(result.inserted_id)}), 201
def user_login():
    try:
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
    except PyMongoError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
