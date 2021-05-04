import peewee as pw
from models.base_model import BaseModel
from models.user import User

class Friend(BaseModel):
    user1 = pw.ForeignKeyField(User,on_delete="CASCADE", null=False)
    user2 = pw.ForeignKeyField(User, on_delete="CASCADE", null=False)