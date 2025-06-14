from flask_mail import Message
from flask import current_app
from app.extensions import mail, mongo
from app.utils.token_utils import generate_verification_token
from app.services.ai_email_generator import generate_email
from datetime import datetime


def send_email(subject, recipients, html):
    msg = Message(subject=subject, recipients=recipients)
    msg.html = html
    mail.send(msg)


def send_verification_email(user):
    token = generate_verification_token(user["email"])
    link = f"{current_app.config['BASE_URL']}/verify/{token}"
    html = f"<p>Hi {user['first_name']}, click <a href='{link}'>here</a> to verify.</p>"
    send_email("Verify your email", [user["email"]], html)
    log_email("verification", user, html)


def send_ai_welcome_email(user):
    prompt = f"Write a short welcome email to {user['first_name']} who just signed up."
    html = generate_email(prompt)
    send_email("Welcome to our platform!", [user["email"]], html)
    log_email("welcome", user, html)


def log_email(email_type, user, body):
    mongo.db.email_logs.insert_one({
        "type": email_type,
        "user_id": str(user["_id"]),
        "email": user["email"],
        "sent_at": datetime.utcnow(),
        "retry_count": 0,
        "status": "sent",
        "body": body
    })
