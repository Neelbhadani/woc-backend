from bson import ObjectId
from flask import jsonify, request

from app import mongo
from app.models.PropertyModel import PropertyModel


def get_property(property_id=None):
    if property_id:
        property_data = mongo.db.properties.find_one({"_id": ObjectId(property_id)})
        if property_data:
            return jsonify(serialize_property(property_data))
        else:
            return jsonify({"error": "property not found"}), 404
    else:
        property_data = mongo.db.properties.find()
        property_list = [serialize_property(prop) for prop in property_data]
        return jsonify(property_list)



def create_property(current_user):
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


from bson import ObjectId


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
