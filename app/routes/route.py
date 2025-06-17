from flask import Blueprint
from app.controllers.user_controller import get_users, register_user, user_login, logout_user
from app.controllers.property_controller import create_property, get_property
from app.auth.decorators import token_required

user_bp = Blueprint("user_bp", __name__)


# user register
@user_bp.route('/register', methods=['POST'])
def register():
    return register_user()


# user login
@user_bp.route('/login', methods=['POST'])  # Use POST for login
def login():
    return user_login()


# user logout
@user_bp.route("/logout", methods=["POST"])
@token_required
def logout(current_user):
    return logout_user(current_user)


# Route to get all users or a specific user
@user_bp.route("/users", methods=["GET"])
@user_bp.route("/users/<user_id>", methods=["GET"])
@token_required
def users(current_user, user_id=None):  # Add current_user as the first argument
    return get_users(user_id)

#create property
@user_bp.route("/properties", methods=["POST"])
@token_required
def properties(current_user):
    return create_property(current_user)

#get property
@user_bp.route("/property", methods=["GET"])
@user_bp.route("/property/<property_id>", methods=["GET"])
@token_required
def get_properties(current_user, property_id=None):
    return get_property(property_id)