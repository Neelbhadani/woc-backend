from datetime import datetime
import bcrypt
from bson.objectid import ObjectId


class UserModel:
    required_fields = {
        "first_name": "First name is required",
        "last_name": "Last name is required",
        "email": "Email is required",
        "password": "Password is required",
        "phone_number": "Phone number is required",
        "user_name": "Username is required"
    }

    def __init__(self, data):
        self.data = data  # store raw data for validation
        self.first_name = data.get("first_name")
        self.last_name = data.get("last_name")
        self.email = data.get("email")
        self.password = data.get("password")
        self.phone_number = data.get("phone_number")
        self.user_name = data.get("user_name")

        self.email_verified = False
        self.email_verified_at = None
        self.is_active = True
        self.is_phone_number_verified = False
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.deleted_at = None

    def validate(self):
        errors = []

        for field, error_msg in self.required_fields.items():
            value = self.data.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append(error_msg)

        if errors:
            raise ValueError("; ".join(errors))

    def hash_password(self):
        hashed = bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt())
        self.password = hashed.decode("utf-8")

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "email_verified": self.email_verified,
            "email_verified_at": self.email_verified_at,
            "is_active": self.is_active,
            "phone_number": self.phone_number,
            "is_phone_number_verified": self.is_phone_number_verified,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
            "user_name": self.user_name
        }
