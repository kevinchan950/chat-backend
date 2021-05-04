from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

sessions_api_blueprint = Blueprint('sessions_api', __name__)


@sessions_api_blueprint.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.get_or_none(username = username)
    
    if user: 
        if check_password_hash(user.hashed_password, password):
            token = create_access_token(identity = user.id, expires_delta = False)
            update = User.update(is_online=True).where(User.id==user.id)
            update.execute()    
            return jsonify({ "token" : token , "message" : "Login successful!"})
        else:
            return jsonify({ "error" : "Username or password is not correct!"})
    else:
        return jsonify({ "error" : "Username or password is not correct!"})


@sessions_api_blueprint.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    update = User.update(is_online=False).where(User.id==get_jwt_identity())
    update.execute()
    return jsonify({ "message" : "Logout Successful!"})


@sessions_api_blueprint.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    hashed_password = generate_password_hash(password)
    create_user = User(username = username, email = email, password = password, hashed_password = hashed_password)
    if create_user.save():
        token = create_access_token(identity = create_user.id, expires_delta= False)
        update = User.update(is_online=True).where(User.id==create_user.id)
        update.execute()
        return jsonify({ "token" : token, "message" : "Login successful!"})
    else:
        return jsonify({ "error" : create_user.errors})


@sessions_api_blueprint.route("/signup/checkemail=<check_email>", methods=["GET"])
def check_email(check_email):
    duplicate_email = User.get_or_none(email=check_email)

    if duplicate_email: 
        return jsonify({ "exist" : True})
    else:
        return jsonify({ "exist" : False})
    

@sessions_api_blueprint.route("/signup/checkusername=<check_username>", methods=["GET"])
def check_username(check_username):
    duplicate_username = User.get_or_none(username=check_username)

    if duplicate_username:
        return jsonify({ "exist" : True})
    else:
        return jsonify({ "exist" : False})