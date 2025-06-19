import jwt
from flask import jsonify, request, current_app
from bson import ObjectId
from app.extensions import mongo
from app.models.Role import RoleModel
from pymongo.errors import PyMongoError


class RoleController:

    @staticmethod
    def get_roles(role_id=None):
        if role_id:
            try:
                role = mongo.db.roles.find_one({"_id": ObjectId(role_id)})
                if role:
                    role['_id'] = str(role['_id'])
                    role_model = RoleModel(role)
                    public_role = role_model.to_public_dict()
                    public_role['_id'] = role['_id']
                    return jsonify(public_role)
                else:
                    return jsonify({"error": "Role not found"}), 404
            except Exception as e:
                return jsonify({"error": "Invalid role ID", "details": str(e)}), 400
        else:
            try:
                roles = mongo.db.roles.find()
                role_list = []
                for role in roles:
                    role['_id'] = str(role['_id'])
                    role_model = RoleModel(role)
                    public_role = role_model.to_public_dict()
                    public_role['_id'] = role['_id']
                    role_list.append(public_role)
                return jsonify(role_list)
            except Exception as e:
                return jsonify({"error": "Failed to fetch roles", "details": str(e)}), 500

    @staticmethod
    def create_role(current_user):
        try:
            data = request.get_json()

            if mongo.db.roles.find_one({"name": data.get("name")}):
                return jsonify({"error": "Role already exists"}), 400

            role = RoleModel(data)
            role.validate()

            role_dict = role.to_public_dict()
            result = mongo.db.roles.insert_one(role_dict)

            role_data = role.to_public_dict()
            role_data["_id"] = str(result.inserted_id)

            return jsonify({
                "message": "Role added successfully",
                "role": role_data
            }), 201

        except ValueError as ve:
            return jsonify({"error": "Validation error", "details": str(ve)}), 400
        except PyMongoError as e:
            return jsonify({"error": "Database error", "details": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
