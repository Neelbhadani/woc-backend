import jwt
from flask import jsonify, request, current_app
from bson import ObjectId
from app.extensions import mongo
from app.models.User import UserModel
from pymongo.errors import PyMongoError
from datetime import datetime
import bcrypt

from app.services.email_service import send_verification_email, send_ai_welcome_email


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
        send_verification_email(user)
        send_ai_welcome_email(user)
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
            "user_id": str(user["_id"]),
            "email": user["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # expires in 1 hour
        }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
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
