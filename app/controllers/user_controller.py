from flask import jsonify,request
from bson import ObjectId
from app.extensions import mongo
from app.models.User import UserModel
from pymongo.errors import PyMongoError
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
    try:
        data = request.get_json()

        required_fields = ["first_name", "last_name", "email", "password", "phone_number", "user_name"]
        if not all(data.get(field) for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Check for existing email or username
        if mongo.db.users.find_one({"email": data["email"]}):
            return jsonify({"error": "Email already exists"}), 400

        if mongo.db.users.find_one({"user_name": data["user_name"]}):
            return jsonify({"error": "Username already taken"}), 400

        # Create user model and hash password
        user = UserModel(data)
        user.hash_password()

        # Insert into DB
        result = mongo.db.users.insert_one(user.to_dict())

        # Prepare response
        user_data = user.to_dict()
        user_data["_id"] = str(result.inserted_id)
        user_data.pop("password")

        return jsonify({
            "message": "User registered successfully",
            "user": user_data
        }), 201
    except PyMongoError as e:
        # Catch MongoDB-related errors
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except Exception as e:
        # Catch all other unexpected errors
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500