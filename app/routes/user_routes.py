from flask import Blueprint
from app.controllers.user_controller import get_users, register_user

user_bp = Blueprint("user_bp", __name__)

# Route to get all users or a specific user
@user_bp.route("/users", methods=["GET"])
@user_bp.route("/users/<user_id>", methods=["GET"])
def users(user_id=None):
    return get_users(user_id)

@user_bp.route('/register', methods=['POST'])
def register():
    return register_user()
