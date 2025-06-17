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


def create_tenant(current_user):
    raw_data = request.get_json()

    # Convert user ID to string to safely pass it to the model
    raw_data["created_by"] = str(current_user["_id"])
    raw_data["updated_by"] = str(current_user["_id"])

    try:
        property_model = PropertyModel(raw_data)
        property_model.validate()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    result = mongo.db.properties.insert_one(property_model.to_dict())
    property_model._id = result.inserted_id

    return jsonify({
        "message": "Property created",
        "property": property_model.to_json()
    }), 201




