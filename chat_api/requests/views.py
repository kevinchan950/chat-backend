from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.friend_request import FriendRequest

requests_api_blueprint = Blueprint('requests_api', __name__)

@requests_api_blueprint.route("/new", methods=["POST"])
@jwt_required()
def new_request():
    current_user = User.get_by_id(get_jwt_identity())
    recipient = User.get_by_id(request.form.get("id"))

    requests = FriendRequest(sender_id=current_user.id, recipient_id=recipient.id)
    
    if requests.save():
        return jsonify({ "successful" : True, "message" : "Friend request has been sent!"})
    else:
        return jsonify({ "error" : "Something went wrong!"})


@requests_api_blueprint.route("/check/<id>", methods=["GET"])
@jwt_required()
def check_request(id):

    current_user = User.get_by_id(get_jwt_identity())
    recipient = User.get_by_id(id)

    check = FriendRequest.select().where(FriendRequest.sender_id==current_user.id, FriendRequest.recipient_id == recipient.id)
    check2 = FriendRequest.select().where(FriendRequest.sender_id==recipient.id, FriendRequest.recipient_id== current_user.id)

    if check or check2:
        return jsonify({ "exist" : True})
    else:
        return jsonify({ "exist" : False})


@requests_api_blueprint.route("/show/me", methods=["GET"])
@jwt_required()
def show_request():
    current_user = User.get_by_id(get_jwt_identity())

    friend_request = FriendRequest.select().where(FriendRequest.recipient_id==current_user.id)

    results = []
    for f in friend_request:
        sender = User.get_by_id(f.sender_id)
        data = {
            "id" : sender.id,
            "name" : sender.username
        }
        results.append(data)
    
    return jsonify({ "data" : results })


@requests_api_blueprint.route("/delete", methods=["POST"])
@jwt_required()
def delete_request():
    current_user = User.get_by_id(get_jwt_identity())

    sender = User.get_by_id(request.form.get("id"))

    delete = FriendRequest.delete().where(FriendRequest.sender_id==sender.id, FriendRequest.recipient_id==current_user.id)
    
    if delete.execute():
        return jsonify({ "message" : "Friend request has been declined!"})
    else:
        return jsonify({ "error" : "Something went wrong!"})