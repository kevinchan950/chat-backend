import peewee as pw
from models.base_model import BaseModel
from models.user import User

class FriendRequest(BaseModel):
    sender = pw.ForeignKeyField(User, backref="requests", on_delete="CASCADE")
    recipient = pw.ForeignKeyField(User, backref="requests", on_delete="CASCADE")