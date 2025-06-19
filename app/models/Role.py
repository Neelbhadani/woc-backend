from datetime import datetime


class RoleModel:
    required_fields = {
        "name": "Role name is required",
    }

    def __init__(self, data):
        self.data = data  # Store raw input data for validation
        self.name = data.get("name", "").strip()  # Strip to remove extra spaces

        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def validate(self):
        errors = []
        for field, error_msg in self.required_fields.items():
            value = self.data.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append(error_msg)

        if errors:
            raise ValueError("; ".join(errors))

    def to_public_dict(self):
        return {
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
