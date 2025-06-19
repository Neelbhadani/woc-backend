from bson import ObjectId
from flask import jsonify, request
from pymongo.errors import PyMongoError

from app.extensions import mongo
from app.models.Property import PropertyModel


class PropertyController:

    @staticmethod
    def get_property(property_id=None):
        try:
            if property_id:
                property_data = mongo.db.properties.find_one({"_id": ObjectId(property_id)})
                if property_data:
                    return jsonify(PropertyController.serialize_property(property_data))
                else:
                    return jsonify({"error": "Property not found"}), 404
            else:
                property_data = mongo.db.properties.find()
                property_list = [PropertyController.serialize_property(prop) for prop in property_data]
                return jsonify(property_list)
        except Exception as e:
            return jsonify({"error": "Failed to retrieve property", "details": str(e)}), 500

    @staticmethod
    def create_property(current_user):
        try:
            raw_data = request.get_json()
            raw_data["created_by"] = str(current_user["_id"])
            raw_data["updated_by"] = str(current_user["_id"])

            property_model = PropertyModel(raw_data)
            property_model.validate()

            result = mongo.db.properties.insert_one(property_model.to_dict())
            property_model._id = result.inserted_id

            return jsonify({
                "message": "Property created",
                "property": property_model.to_json()
            }), 201

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except PyMongoError as e:
            return jsonify({"error": "Database error", "details": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

    @staticmethod
    def serialize_property(property_data):
        property_data['_id'] = str(property_data['_id'])

        if 'created_by' in property_data and isinstance(property_data['created_by'], ObjectId):
            property_data['created_by'] = str(property_data['created_by'])

        if 'updated_by' in property_data and isinstance(property_data['updated_by'], ObjectId):
            property_data['updated_by'] = str(property_data['updated_by'])

        if 'created_at' in property_data and hasattr(property_data['created_at'], 'isoformat'):
            property_data['created_at'] = property_data['created_at'].isoformat()

        if 'updated_at' in property_data and hasattr(property_data['updated_at'], 'isoformat'):
            property_data['updated_at'] = property_data['updated_at'].isoformat()

        return property_data

