from datetime import datetime, timedelta
from app.extensions import mongo
from app.services.email_service import send_verification_email

def retry_unverified_emails():
    one_day_ago = datetime.utcnow() - timedelta(hours=24)
    logs = mongo.db.email_logs.find({
        "type": "verification",
        "status": "sent",
        "retry_count": {"$lt": 5},
        "sent_at": {"$lt": one_day_ago}
    })

    for log in logs:
        user = mongo.db.users.find_one({"_id": log["user_id"], "email_verified": False})
        if user:
            send_verification_email(user)
            mongo.db.email_logs.update_one(
                {"_id": log["_id"]},
                {"$inc": {"retry_count": 1}, "$set": {"sent_at": datetime.utcnow()}}
            )
