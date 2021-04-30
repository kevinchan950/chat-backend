import peewee as pw
from models.base_model import BaseModel
from models.user import User

class follower(BaseModel):
    fan = pw.ForeignKeyField(User,on_delete="CASCADE", null=False)
    idol = pw.ForeignKeyField(User, on_delete="CASCADE", null=False)
    is_accepted = pw.BooleanField(null=False, default=False)
