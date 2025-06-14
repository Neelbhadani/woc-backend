import jwt
from flask import jsonify, request, current_app
from bson import ObjectId
from app.extensions import mongo
from app.models.User import UserModel
from pymongo.errors import PyMongoError
from datetime import datetime, timedelta
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

        if mongo.db.users.find_one({"email": data.get("email")}):
            return jsonify({"error": "Email already exists"}), 400

        if mongo.db.users.find_one({"user_name": data.get("user_name")}):
            return jsonify({"error": "Username already taken"}), 400

        user = UserModel(data)
        user.validate()
        user.hash_password()

        result = mongo.db.users.insert_one(user.to_dict())
        user_data = user.to_public_dict()
        user_data["_id"] = str(result.inserted_id)

        return jsonify({
            "message": "User registered successfully",
            "user": user_data
        }), 201

    except ValueError as ve:
        return jsonify({"error": "Validation error", "details": str(ve)}), 400
    except PyMongoError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

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

        payload = {
            "u": str(user["_id"]),
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": {
                "user_id": str(user["_id"]),
                "email": user["email"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "user_name": user["user_name"]
            }
        }), 200

    except PyMongoError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
