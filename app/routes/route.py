from flask import Blueprint
from app.controllers.UserController import UserController
from app.controllers.PropertyController import PropertyController
from app.controllers.RoleController import RoleController

from app.auth.decorators import token_required

user_bp = Blueprint("user_bp", __name__)


# user register
@user_bp.route('/register', methods=['POST'])
def register():
    return UserController.register_user()


# user login
@user_bp.route('/login', methods=['POST'])  # Use POST for login
def login():
    return UserController.user_login()


# user logout
@user_bp.route("/logout", methods=["POST"])
@token_required
def logout(current_user):
    return UserController.logout_user(current_user)


# Route to get all users or a specific user
@user_bp.route("/users", methods=["GET"])
@user_bp.route("/users/<user_id>", methods=["GET"])
@token_required
def users(current_user, user_id=None):  # Add current_user as the first argument
    return UserController.get_users(user_id)

#create property
@user_bp.route("/properties", methods=["POST"])
@token_required
def properties(current_user):
    return PropertyController.create_property(current_user)

#get property
@user_bp.route("/property", methods=["GET"])
@user_bp.route("/property/<property_id>", methods=["GET"])
@token_required
def get_properties(current_user, property_id=None):
    return PropertyController.get_property(property_id)

#create roles
@user_bp.route("/roles", methods=["POST"])
@token_required
def roles(current_user):
    return RoleController.create_role(current_user)

# Route to get all users or a specific user
@user_bp.route("/roles", methods=["GET"])
@user_bp.route("/roles/<role_id>", methods=["GET"])
@token_required
def get_role(current_user, role_id=None):  # Add current_user as the first argument
    return RoleController.get_roles(role_id)