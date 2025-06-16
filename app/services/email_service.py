from flask_mail import Message
from flask import current_app
from app.extensions import mail, mongo
from app.utils.token_utils import generate_verification_token
from app.services.ai_email_generator import generate_email
from app.models.EmailLogModel import EmailLogModel
from datetime import datetime


def send_email(subject, recipients, html):
    msg = Message(
        subject=subject,
        sender=current_app.config['MAIL_USERNAME'],  # 👈 add this line
        recipients=recipients
    )
    msg.html = html
    mail.send(msg)


def send_verification_email(user):
    token = generate_verification_token(user["email"])
    link = f"{current_app.config['BASE_URL']}/verify/{token}"
    html = f"<p>Hi {user['first_name']}, click <a href='{link}'>here</a> to verify your email.</p>"

    send_email("Verify your email", [user["email"]], html)

    log = EmailLogModel(
        email_type="verification",
        user_id=user["_id"],
        email=user["email"],
        subject="Verify your email",
        body=html
    )
    mongo.db.email_logs.insert_one(log.to_dict())


def send_ai_welcome_email(user):
    prompt = f"Write a short welcome email to {user['first_name']} who just signed up."
    html = generate_email(prompt)

    send_email("Welcome to our platform!", [user["email"]], html)

    log = EmailLogModel(
        email_type="welcome",
        user_id=user["_id"],
        email=user["email"],
        subject="Welcome to our platform!",
        body=html
    )
    mongo.db.email_logs.insert_one(log.to_dict())
