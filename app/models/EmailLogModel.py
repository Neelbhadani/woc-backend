from datetime import datetime
from bson import ObjectId


class EmailLogModel:
    def __init__(self, email_type, user_id, email, subject, body, status="sent", retry_count=0, sent_at=None):
        self.email_type = email_type  # e.g., "verification", "welcome"
        self.user_id = str(user_id) if isinstance(user_id, ObjectId) else user_id
        self.email = email
        self.subject = subject
        self.body = body
        self.status = status
        self.retry_count = retry_count
        self.sent_at = sent_at or datetime.utcnow()

    def to_dict(self):
        return {
            "type": self.email_type,
            "user_id": self.user_id,
            "email": self.email,
            "subject": self.subject,
            "body": self.body,
            "status": self.status,
            "retry_count": self.retry_count,
            "sent_at": self.sent_at
        }

    @staticmethod
    def from_dict(data):
        return EmailLogModel(
            email_type=data.get("type"),
            user_id=data.get("user_id"),
            email=data.get("email"),
            subject=data.get("subject"),
            body=data.get("body"),
            status=data.get("status", "sent"),
            retry_count=data.get("retry_count", 0),
            sent_at=data.get("sent_at", datetime.utcnow())
        )
