from app.extensions import mongo
from bson import ObjectId  # if user_id is a string

def assign_role(role, user_id):
    role_map = {
        "A": "admin",
        "M": "manager",
        "AA": "Admin Assist",
        "C": "contractor",
        "T": "tenant",
        "O": "owner"
    }

    role_name = role_map.get(role)
    if not role_name:
        return f"Unknown role code '{role}'"

    role_data = mongo.db.roles.find_one({"name": role_name})
    if not role_data:
        return f"Role '{role_name}' not found in the database."

    try:
        mongo.db.user_has_roles.insert_one({
            "user_id": ObjectId(user_id) if isinstance(user_id, str) else user_id,
            "role_id": role_data["_id"]
        })
        return f"Role '{role_name}' assigned successfully."
    except Exception as e:
        return f"Error assigning role: {str(e)}"
