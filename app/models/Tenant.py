from datetime import datetime
from bson import ObjectId


class Tenant:
    required_fields = {
        "first_name": "Street address is required",
        "last_name": "Address is required",
        "user_id": "Unit is required",
    }

    def __init__(self, data):

        self.data = data  # Raw input for validation

        self.first_name = data.get("first_name")
        self.last_name = data.get("last_name")
        self.user_id = data.get("user_id")


        self.created_by = ObjectId(data.get("created_by")) if data.get("created_by") else None
        self.updated_by = ObjectId(data.get("updated_by")) if data.get("updated_by") else None

        now = datetime.utcnow()
        self.created_at = data.get("created_at") or now
        self.updated_at = data.get("updated_at") or now

    def validate(self):
        errors = []
        for field, error_msg in self.required_fields.items():
            value = self.data.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append(error_msg)

        if errors:
            raise ValueError("; ".join(errors))

    def to_dict(self):
        result = {
            "street_address": self.street_address,
            "address": self.address,
            "unit": self.unit,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "zip": self.zip,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


    def to_json(self):
        result = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "user_id": self.user_id,
            "created_by": str(self.created_by) if self.created_by else None,
            "updated_by": str(self.updated_by) if self.updated_by else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }