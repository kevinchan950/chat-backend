from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.friend import Friend
from models.friend_request import FriendRequest

friends_api_blueprint = Blueprint('friends_api', __name__)

@friends_api_blueprint.route("/new", methods=["POST"])
@jwt_required()
def new_friend():
    current_user = User.get_by_id(get_jwt_identity())

    approve_user = User.get_by_id(request.form.get("id"))

    friend = Friend(user1_id=current_user.id, user2_id=approve_user.id)

    if friend.save():
        delete = FriendRequest.delete().where(FriendRequest.sender_id == approve_user.id, FriendRequest.recipient_id==current_user.id)
        delete.execute()
        return jsonify({ "successful" : True, "message" : "Friend request has been accepted!"})
    else:
        return jsonify({ "error" : "Something went wrong!"})


@friends_api_blueprint.route("/me", methods=["GET"])
@jwt_required()
def show_friend():
    current_user = User.get_by_id(get_jwt_identity())

    first_selection = Friend.select().where(Friend.user1_id==current_user.id)
    second_selection = Friend.select().where(Friend.user2_id==current_user.id)
    results = []
    for f in first_selection:
        user = User.get_by_id(f.user2_id)
        data = {
            "name" : user.username,
            "is_online": user.is_online
        }
        results.append(data)
    
    for s in second_selection:
        user = User.get_by_id(s.user1_id)
        data = {
            "name" : user.username,
            "is_online": user.is_online
        }
        results.append(data)
    
    return jsonify({ "data" : results })


@friends_api_blueprint.route("/check/<id>", methods=["GET"])
@jwt_required()
def check_friend(id):
    current_user = User.get_by_id(get_jwt_identity())

    check_friend = User.get_by_id(id)

    check = Friend.get_or_none(user1_id=current_user.id, user2_id=check_friend.id)
    check2 = Friend.get_or_none(user1_id=check_friend.id, user2_id=current_user.id)

    if check or check2:
        return jsonify({ "is_friend" : True})
    else:
        return jsonify({ "is_friend" : False})
