from datetime import datetime
import bcrypt
from bson.objectid import ObjectId


class UserModel:
    def __init__(self, data):
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.phone_number = data["phone_number"]
        self.user_name = data["user_name"]

        self.email_verified = False
        self.email_verified_at = None
        self.is_active = True
        self.is_phone_number_verified = False
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.deleted_at = None

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
