from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User

users_api_blueprint = Blueprint('users_api', __name__)


@users_api_blueprint.route("/me", methods=["GET"])
@jwt_required()
def show_user():
    user = User.get_by_id(get_jwt_identity())
    results = {
        "id" : user.id,
        "username" : user.username,
        "email" : user.email,
        "profile_picture" : user.profile_picture,
        "info" : user.info,
        "is_private" : user.is_private
    }
    return jsonify({ "data" : results })


@users_api_blueprint.route("/search=<keyword>", methods=["GET"])
@jwt_required()
def search_user(keyword):
    user = User.get_by_id(get_jwt_identity())

    search_user = User.select().where(User.username.contains(keyword))

    result = []
    for s in search_user:
        if s.username == user.username:
            pass
        else:
            data = {
                "id" : s.id,
                "username" : s.username
            }
            result.append(data)

    if len(result)==0:
        return jsonify({ "error" : "No user is found!"})
    else:
        return jsonify({ "data" : result })


@users_api_blueprint.route("/<id>", methods=["GET"])
def user_profile(id):
    user = User.get_by_id(id)

    results = {
        "username" : user.username,
        "email" : user.email,
        "profile_picture" : user.profile_picture,
        "info" : user.info,
        "is_private" : user.is_private
    }
    return jsonify({ "data" : results })
